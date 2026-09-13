#!/usr/bin/env python3
"""Agentix-protocol serving run on one GPU: FCFS vs program-level (PLAS) scheduling.

Replays a synthesised program workload (``workload.py``) against a vLLM engine.
Each program is an async task that submits its LLM calls as they become ready and
sleeps for the modelled interception (tool) delay in between — the paper's
program abstraction.

Scheduling policies:
  fcfs  — vLLM's default arrival-order policy (the paper's primary baseline).
  plas  — Program-Level Attained Service (paper §3): a call's priority is the sum of
          the runtimes of its program's prior completed calls, so programs that have
          consumed least service win the queue.
  atlas — Adaptive Thread-Level Attained Service (paper §3): for multi-threaded
          programs the priority comes from the parents' priorities plus their
          completed service, i.e. service along the program's critical path. It
          coincides with PLAS on single-threaded programs.

Per-call and per-program timings are written as JSONL; the summary carries the
paper's metrics: program-level token latency, throughput, and latency tails.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import platform
import socket
import time
from pathlib import Path
from typing import Any


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _pct(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    return s[min(len(s) - 1, int(q * (len(s) - 1)))]


async def run(args: argparse.Namespace) -> dict[str, Any]:
    from vllm import SamplingParams
    from vllm.engine.arg_utils import AsyncEngineArgs
    from vllm.v1.engine.async_llm import AsyncLLM

    workload = json.loads(args.workload.read_text())
    program_list = workload["programs"]

    engine_kwargs = dict(
        model=str(args.model_dir),
        dtype="bfloat16",
        gpu_memory_utilization=args.gpu_memory_utilization,
        max_model_len=args.max_model_len,
        enforce_eager=args.enforce_eager,
        disable_log_stats=True,
        scheduling_policy="priority" if args.policy in ("plas", "atlas") else "fcfs",
        max_num_seqs=args.max_num_seqs,
        enable_layerwise_nvtx_tracing=args.enable_layerwise_nvtx_tracing,
        seed=0,
    )
    if args.no_cudagraph:
        engine_kwargs["compilation_config"] = {"cudagraph_mode": "NONE"}
    engine_args = AsyncEngineArgs(**engine_kwargs)
    engine = AsyncLLM.from_engine_args(engine_args)
    try:
        # warm-up: one short call so weight load / graph capture is not billed to a program
        warm = SamplingParams(max_tokens=4, ignore_eos=True, temperature=0.0)
        async for _ in engine.generate({"prompt_token_ids": [1] * 32}, warm, request_id="warmup"):
            pass

        t0 = time.monotonic_ns()
        call_rows: list[dict[str, Any]] = []
        program_rows: list[dict[str, Any]] = []
        lock = asyncio.Lock()

        # AutoTrace adaptation. Client-side marks (not ranges: asyncio interleaves
        # coroutines, so push/pop pairs would not nest) give the per-call request
        # windows on the nsys timeline and let w02 fit the host->nsys clock offset
        # exactly as the h22 chain does. The measured window itself is a range,
        # pushed once by this single coroutine around the gather.
        def _nvtx_mark(name: str) -> None:
            if args.nvtx:
                import torch

                torch.cuda.nvtx.mark(name)

        filler = [args.filler_token_id] * args.max_model_len  # prompt token ids are sliced per call

        async def run_call(program: dict[str, Any], call: dict[str, Any], priority: int,
                           ready_ns: int) -> tuple[int, int]:
            """Issue one LLM call; returns (finished_ns, runtime_us)."""
            now = time.monotonic_ns()
            if ready_ns > now:
                await asyncio.sleep((ready_ns - now) / 1e9)
            params = SamplingParams(max_tokens=int(call["output_tokens"]), ignore_eos=True, temperature=0.0)
            rid = f"{program['program_id']}-{call['index']}"
            submitted = time.monotonic_ns()
            _nvtx_mark(f"agentix.call_begin::{program['program_id']}::{call['index']}::{program['class']}")
            first_token = None
            produced = 0
            # vLLM sorts the waiting queue by (priority, arrival_time) ascending, so a
            # lower value is served first.
            async for out in engine.generate(
                {"prompt_token_ids": filler[: int(call["prompt_tokens"])]},
                params, request_id=rid,
                priority=priority if args.policy in ("plas", "atlas") else 0,
            ):
                if first_token is None:
                    first_token = time.monotonic_ns()
                produced = len(out.outputs[0].token_ids)
            finished = time.monotonic_ns()
            _nvtx_mark(f"agentix.call_end::{program['program_id']}::{call['index']}::{program['class']}")
            async with lock:
                call_rows.append({
                    "program_id": program["program_id"], "class": program["class"], "call_index": call["index"],
                    "wave": call.get("wave", 0), "parents": call.get("parents", []),
                    "prompt_tokens": int(call["prompt_tokens"]), "output_tokens": int(call["output_tokens"]),
                    "submitted_rel_ms": (submitted - t0) / 1e6,
                    "first_token_rel_ms": ((first_token or finished) - t0) / 1e6,
                    "finished_rel_ms": (finished - t0) / 1e6,
                    "ttft_ms": ((first_token or finished) - submitted) / 1e6,
                    "call_latency_ms": (finished - submitted) / 1e6, "priority": priority,
                    "policy": args.policy, "produced_tokens": produced,
                })
            return finished, (finished - submitted) // 1000

        async def run_program(program: dict[str, Any]) -> None:
            arrived = t0 + program["arrival_ns"]
            now = time.monotonic_ns()
            if arrived > now:
                await asyncio.sleep((arrived - now) / 1e9)

            calls = program["llm_calls"]
            waves: dict[int, list[dict[str, Any]]] = {}
            for c in calls:
                waves.setdefault(c.get("wave", c["index"]), []).append(c)

            attained_us = 0                       # PLAS: total service of the program
            prio_of: dict[int, int] = {}          # ATLAS: per-call critical-path priority
            runtime_of: dict[int, int] = {}
            finished_of: dict[int, int] = {}

            for wave in sorted(waves):
                members = waves[wave]
                # a wave becomes ready one tool step after its parents finished
                ready_base = max((finished_of[i] for c in members for i in c.get("parents", [])), default=t0 + program["arrival_ns"])
                jobs = []
                for c in members:
                    if args.policy == "atlas":
                        # ATLAS (paper §3): priority from the parents' priorities plus
                        # their completed service, i.e. service along the critical path.
                        prio = max((prio_of[i] + runtime_of[i] for i in c.get("parents", [])), default=0)
                    else:
                        prio = attained_us       # PLAS: whole-program attained service
                    prio_of[c["index"]] = prio
                    jobs.append(run_call(program, c, prio, ready_base + int(c.get("tool_delay_ns", 0))))
                results = await asyncio.gather(*jobs)
                for c, (fin, rt_us) in zip(members, results):
                    finished_of[c["index"]] = fin
                    runtime_of[c["index"]] = rt_us
                    attained_us += rt_us

        tasks = [asyncio.create_task(run_program(p)) for p in program_list]
        started = time.monotonic_ns()
        if args.nvtx:
            import torch

            torch.cuda.nvtx.range_push("agentix.window::measured")
        await asyncio.gather(*tasks)
        ended = time.monotonic_ns()
        if args.nvtx:
            import torch

            torch.cuda.nvtx.range_pop()

        by_program: dict[str, list[dict[str, Any]]] = {}
        for r in call_rows:
            by_program.setdefault(r["program_id"], []).append(r)
        for program in program_list:
            rows = by_program.get(program["program_id"], [])
            if not rows:
                continue
            finish = max(r["finished_rel_ms"] for r in rows)
            gen = sum(r["produced_tokens"] for r in rows)
            program_rows.append({
                "program_id": program["program_id"], "class": program["class"], "policy": args.policy,
                "llm_calls": len(rows), "arrival_rel_ms": program["arrival_ns"] / 1e6,
                "finish_rel_ms": finish, "response_time_ms": finish - program["arrival_ns"] / 1e6,
                "generated_tokens": gen,
                "program_token_latency_ms": ((finish - program["arrival_ns"] / 1e6) / gen) if gen else 0.0,
            })

        out_dir = args.output_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"calls_{args.policy}.jsonl").write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in call_rows))
        (out_dir / f"programs_{args.policy}.jsonl").write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in program_rows))

        lat = [r["response_time_ms"] for r in program_rows]
        ptl = [r["program_token_latency_ms"] for r in program_rows]
        wall_s = (ended - started) / 1e9
        summary = {
            "schema_version": 1, "goal": "Agentix-8B single-GPU reproduction", "policy": args.policy,
            "workload": {"path": str(args.workload), "sha256": _sha256(args.workload), "class": workload["config"]["workload_class"],
                         "arrival_rate": workload["config"]["arrival_rate_programs_per_s"], "seed": workload["config"]["seed"]},
            "engine": {"model": str(args.model_dir), "dtype": "bfloat16", "gpu_memory_utilization": args.gpu_memory_utilization,
                       "max_model_len": args.max_model_len, "enforce_eager": args.enforce_eager, "scheduling_policy": args.policy},
            "observed": {
                "programs": len(program_rows), "llm_calls": len(call_rows), "generated_tokens": sum(r["produced_tokens"] for r in call_rows),
                "wall_s": wall_s, "throughput_programs_per_s": len(program_rows) / wall_s if wall_s else 0.0,
                "throughput_tokens_per_s": sum(r["produced_tokens"] for r in call_rows) / wall_s if wall_s else 0.0,
                "program_response_time_ms": {"mean": sum(lat) / len(lat) if lat else 0.0, "p50": _pct(lat, 0.5), "p90": _pct(lat, 0.9), "p99": _pct(lat, 0.99)},
                "program_token_latency_ms": {"mean": sum(ptl) / len(ptl) if ptl else 0.0, "p90": _pct(ptl, 0.9), "p99": _pct(ptl, 0.99)},
                "call_latency_ms": {"mean": sum(r["call_latency_ms"] for r in call_rows) / len(call_rows) if call_rows else 0.0,
                                    "p90": _pct([r["call_latency_ms"] for r in call_rows], 0.9), "p99": _pct([r["call_latency_ms"] for r in call_rows], 0.99)},
            },
            "environment": {"host": socket.gethostname(), "python": platform.python_version(),
                            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", "")},
            "timing_ns": {"t0": t0, "started": started, "ended": ended},
            "pass": len(program_rows) > 0 and len(call_rows) > 0,
        }
        (out_dir / f"summary_{args.policy}.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
        print(json.dumps({k: summary[k] for k in ("policy", "observed", "pass")}, indent=2))
        return summary
    finally:
        engine.shutdown()


def main() -> int:
    ap = argparse.ArgumentParser(description="Agentix-protocol serving run on one GPU")
    ap.add_argument("--workload", type=Path, required=True)
    ap.add_argument("--model-dir", type=Path, default=Path("/data3/docker_model/AgentSys/Llama-3.1-8B"))
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--policy", choices=["fcfs", "plas", "atlas"], required=True)
    ap.add_argument("--gpu-memory-utilization", type=float, default=0.90)
    ap.add_argument("--max-model-len", type=int, default=4096)
    ap.add_argument("--max-num-seqs", type=int, default=None,
                    help="cap the resident batch to force request queueing (the regime program-level scheduling targets)")
    ap.add_argument("--enforce-eager", action="store_true")
    ap.add_argument("--nvtx", action="store_true", help="emit client-side NVTX windows for AutoTrace")
    ap.add_argument("--enable-layerwise-nvtx-tracing", action="store_true",
                    help="vLLM worker emits per-module NVTX ranges (operator-level attribution for w01')")
    ap.add_argument("--no-cudagraph", action="store_true",
                    help="keep torch.compile but disable CUDA graphs, so the compile wrapper (and its NVTX markers) executes per forward")
    ap.add_argument("--filler-token-id", type=int, default=970)
    args = ap.parse_args()
    asyncio.run(run(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
