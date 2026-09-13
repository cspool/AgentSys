#!/usr/bin/env python3
"""Execute an AgentSys hybrid plan with real Qwen3-1.7B inference on one GPU,
running on the user-supplied ``transformers`` library (the real-model strand
that was pending until those sources arrived).

Same DAG, same call structure and same event schema as
``single_gpu_agent_runtime.py`` / ``single_gpu_llm_agent_runtime.py``: every
LLM call runs actual prefill and greedy decode of the local ``Qwen3-1.7B``
weights for exactly the plan's ``input_tokens`` / ``output_tokens``; tool
calls keep the certified CPU matmul adapter from ``agentsys.hybrid_runtime``
(imported read-only).

Operator granularity: one NVTX range per forward stage
(``<phase>_embed``, ``<phase>_layerNN``, ``<phase>_head``, ``<phase>_sample``),
named ``agentsys.mllm::<call>::<index>::<op_type>`` so the w01/w02 analyzers
consume this trace unchanged. The only host sync per token is the greedy
``argmax`` in ``<phase>_sample``.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import socket
import sys
import time
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hf_qwen3_backend import HFQwen3Model, HFTokenizer, ensure_pynvml  # noqa: E402

ensure_pynvml()

from agentsys.hybrid_runtime import _base_event, _cpu_matrix_event, _cpus, _cuda_measure, _nvml_sample, _sha256  # noqa: E402

ADAPTER_NAME = "hf_transformers"
PHASE_RANGE = "agentsys.autotrace::phase={phase}::iter={iteration}"
FILLER = (
    "The agent system schedules language-model calls and tool calls as waves of a directed acyclic graph. "
    "Each node reads the outputs of its dependencies, reasons about the task, and writes a structured result. "
    "Measurements are taken on a single GPU with warmup iterations discarded and the measured window traced. "
)


def _build_prompt_ids(tok: HFTokenizer, call: dict[str, Any], workload: str, filler_ids: list[int]) -> list[int]:
    head = tok.encode(f"<|im_start|>system\nYou are the '{call['call_id']}' node of the '{workload}' agent workflow. Answer concisely.<|im_end|>\n<|im_start|>user\n")
    tail = tok.encode("<|im_end|>\n<|im_start|>assistant\n")
    target = int(call["input_tokens"])
    body_len = max(target - len(head) - len(tail), 0)
    body = (filler_ids * (body_len // len(filler_ids) + 1))[:body_len]
    ids = head + body + tail
    return ids[:target] if len(ids) > target else ids


def _run_llm(call: dict[str, Any], model: HFQwen3Model, tok: HFTokenizer, adapter: dict[str, Any], prompt_ids: list[int], device_index: int, collect: bool) -> tuple[list[dict[str, Any]], float]:
    import torch

    events: list[dict[str, Any]] = []
    started = time.monotonic_ns()
    base = _base_event(call, 0)
    events.append({**base, "layer": "mllm", "event": "mir_adapter_start", "resource": f"gpu{device_index}", "clock_domain": "host_monotonic_ns", "start_ns": started, "end_ns": started, "model": call["model"], "adapter": ADAPTER_NAME})
    # token preprocess: real tokenization of the prompt text (CPU)
    t0 = time.monotonic_ns()
    text = tok.decode(prompt_ids)
    ids = tok.encode(text)
    t1 = time.monotonic_ns()
    # The plan fixes the prompt length in tokens, so the prompt is cut at a token boundary that a
    # re-encode of the decoded text may merge differently; the timed encode is the real preprocessing
    # cost on the same text, while the plan-length ids stay authoritative for the forward pass.
    events.append({**base, "layer": "cpu", "event": "mllm_token_preprocess", "resource": f"cpu_numa{call['native']['numa_node']}", "clock_domain": "host_monotonic_ns", "start_ns": t0, "end_ns": t1, "duration_ms": (t1 - t0) / 1e6, "prompt_tokens": len(prompt_ids), "reencoded_tokens": len(ids), "reencode_identical": ids == prompt_ids, "checksum": float(sum(prompt_ids))})
    ids = prompt_ids

    host_ids = torch.tensor([ids], dtype=torch.int64).pin_memory()
    dev_ids = torch.empty_like(host_ids, device=model.device)
    _, cuda_ms, s, e = _cuda_measure(lambda: dev_ids.copy_(host_ids, non_blocking=True))
    events.append({**base, "layer": "cuda", "event": "h2d", "resource": f"gpu{device_index}", "clock_domain": "host_monotonic_ns", "start_ns": s, "end_ns": e, "cuda_ms": cuda_ms, "bytes": host_ids.numel() * 8})

    prefix = f"agentsys.mllm::{call['call_id']}"
    op_events: list[dict[str, Any]] = []

    def hook(index: int, op_type: str, start_ns: int, end_ns: int) -> None:
        if collect:
            op_events.append({**base, "layer": "gpu", "event": "mir_operator", "resource": f"gpu{device_index}", "clock_domain": "host_monotonic_ns", "start_ns": start_ns, "end_ns": end_ns,
                              "source_index": index, "op_type": op_type, "engine": "llm", "adapter": ADAPTER_NAME})

    # AGENTSYS_NVTX_MEASURED_ONLY=1 suppresses NVTX during warmup so an NCU
    # --nvtx-include on the operator ranges selects measured kernels only.
    nvtx_on = not (os.environ.get("AGENTSYS_NVTX_MEASURED_ONLY") == "1" and call.get("_phase") == "warmup")
    generated: list[int] = []
    n_out = int(call["output_tokens"])
    index = 0
    pos = 0
    x = dev_ids
    phase = "prefill"
    for step in range(n_out):
        logits, index = model.forward(x, pos, range_prefix=prefix if nvtx_on else None, index_base=index, phase=phase, op_hook=hook)
        pos += x.shape[1]
        s0 = time.monotonic_ns()
        if nvtx_on:
            torch.cuda.nvtx.range_push(f"{prefix}::{index}::{phase}_sample")
        try:
            nxt = int(logits.argmax())  # greedy; the only host sync per token
        finally:
            if nvtx_on:
                torch.cuda.nvtx.range_pop()
        hook(index, f"{phase}_sample", s0, time.monotonic_ns())
        index += 1
        generated.append(nxt)
        x = torch.tensor([[nxt]], device=model.device)
        phase = "decode"
    events.extend(op_events)

    dev_out = torch.tensor([generated], device=model.device)
    host_out = torch.empty_like(dev_out, device="cpu").pin_memory()
    _, cuda_ms, s, e = _cuda_measure(lambda: host_out.copy_(dev_out, non_blocking=True))
    checksum = float(host_out.sum())
    events.append({**base, "layer": "cuda", "event": "d2h", "resource": f"gpu{device_index}", "clock_domain": "host_monotonic_ns", "start_ns": s, "end_ns": e, "cuda_ms": cuda_ms, "bytes": host_out.numel() * 8, "checksum": checksum})
    finished = time.monotonic_ns()
    events.append({**base, "layer": "mllm", "event": "mir_adapter_complete", "resource": f"gpu{device_index}", "clock_domain": "host_monotonic_ns", "start_ns": finished, "end_ns": finished, "checksum": checksum, "generated_tokens": len(generated), "ops": index})
    return events, checksum


def run(*, plan_path: Path, model_dir: Path, output_dir: Path, device: int, numa_node: int, cpu_affinity: str, warmup_iters: int, measured_iters: int, attn_implementation: str) -> dict[str, Any]:
    import pynvml
    import torch
    import transformers

    plan_path = plan_path.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    plan = json.loads(plan_path.read_text())
    adapter = plan["configuration"]["adapter"]
    for call in plan["calls"]:
        call["native"]["rank"] = 0
        call["native"]["device"] = device
        call["native"]["numa_node"] = numa_node
    os.sched_setaffinity(0, _cpus(cpu_affinity))
    torch.set_num_threads(int(adapter["cpu_threads_per_rank"]))
    torch.set_num_interop_threads(1)
    torch.cuda.set_device(device)
    torch_device = torch.device("cuda", device)
    pynvml.nvmlInit()
    nvml_before = _nvml_sample(device)

    load_t0 = time.monotonic_ns()
    tok = HFTokenizer(model_dir)
    max_seq = max(int(c["input_tokens"]) + int(c["output_tokens"]) for c in plan["calls"] if c["kind"] == "llm") + 8
    model = HFQwen3Model(model_dir, torch_device, max_seq=max_seq, attn_implementation=attn_implementation)
    probe = model.probe(tok)
    if not probe["pass"]:
        raise SystemExit(f"model validation failed: {probe}")
    load_ms = (time.monotonic_ns() - load_t0) / 1e6
    filler_ids = tok.encode(FILLER)
    prompts = {c["call_id"]: _build_prompt_ids(tok, c, plan["workload"]["name"], filler_ids) for c in plan["calls"] if c["kind"] == "llm"}
    ops_per_forward = model.ops_per_forward() + 1  # + sample
    planned_ops = sum(ops_per_forward * int(c["output_tokens"]) for c in plan["calls"] if c["kind"] == "llm")

    def run_dag(phase: str, iteration: int, collect: bool) -> tuple[list[dict[str, Any]], dict[str, float]]:
        events: list[dict[str, Any]] = []
        checksums: dict[str, float] = {}
        torch.cuda.nvtx.range_push(PHASE_RANGE.format(phase=phase, iteration=iteration))
        try:
            for wave in range(max(c["wave"] for c in plan["calls"]) + 1):
                for call in sorted((c for c in plan["calls"] if c["wave"] == wave), key=lambda c: c["index"]):
                    if call["kind"] == "llm":
                        call["_phase"] = phase
                        ev, ck = _run_llm(call, model, tok, adapter, prompts[call["call_id"]], device, collect)
                        if collect:
                            events.extend(ev)
                    else:
                        ev1, ck = _cpu_matrix_event(call, 0, int(adapter["cpu_matrix_size"]), event_name="agent_tool_execute")
                        if collect:
                            events.append(ev1)
                    checksums[call["call_id"]] = ck
            torch.cuda.synchronize()
        finally:
            torch.cuda.nvtx.range_pop()
        for e in events:
            e["phase"] = phase
            e["iteration"] = iteration
        return events, checksums

    started = time.monotonic_ns()
    warm_ck: dict[str, float] = {}
    for it in range(warmup_iters):
        _, warm_ck = run_dag("warmup", it, False)
    warm_done = time.monotonic_ns()
    events: list[dict[str, Any]] = []
    cks: list[dict[str, float]] = []
    for it in range(measured_iters):
        ev, ck = run_dag("measured", it, True)
        events.extend(ev)
        cks.append(ck)
    finished = time.monotonic_ns()
    nvml_after = _nvml_sample(device)
    pynvml.nvmlShutdown()

    reference = cks[0] if cks else {}
    deterministic = all(c == reference for c in cks) and (not warm_ck or warm_ck == reference)
    events.sort(key=lambda e: (int(e["start_ns"]), str(e["event"])))
    with (output_dir / "native-trace.jsonl").open("w") as handle:
        for seq, e in enumerate(events):
            e["sequence"] = seq
            e["workload"] = plan["workload"]["name"]
            e["workload_sha256"] = plan["workload"]["sha256"]
            handle.write(json.dumps(e, sort_keys=True) + "\n")
    op_events = [e for e in events if e["event"] == "mir_operator"]
    sample_outputs = {}
    for c in plan["calls"]:
        if c["kind"] == "llm":
            sample_outputs[c["call_id"]] = {"prompt_tokens": len(prompts[c["call_id"]]), "output_tokens": int(c["output_tokens"]), "prompt_head": tok.decode(prompts[c["call_id"]][:24])}
    metadata = {
        "schema_version": 1, "lineage": "h22-gpu-autotrace/llm", "goal": "G01", "plan_path": str(plan_path), "plan_sha256": _sha256(plan_path),
        "workload": plan["workload"]["name"], "workload_sha256": plan["workload"]["sha256"],
        "model": {"dir": str(model_dir), "architecture": model.cfg["architectures"], "layers": len(model.layers), "hidden": model.cfg["hidden_size"], "param_bytes": model.param_bytes, "dtype": "bfloat16",
                  "runtime": f"transformers {transformers.__version__} ({model.attn_implementation} attention), user-supplied sources", "validation_probe": probe, "load_ms": load_ms,
                  "decode": "greedy, fixed output_tokens, EOS ignored", "ops_per_forward": ops_per_forward},
        "single_gpu": {"device": device, "name": torch.cuda.get_device_properties(device).name, "uuid": nvml_before["uuid"], "pci_bus_id": nvml_before["pci_bus_id"], "numa_node": numa_node, "observed_affinity": sorted(os.sched_getaffinity(0))},
        "iterations": {"warmup": warmup_iters, "measured": measured_iters}, "adapter": adapter,
        "planned": {"calls": int(plan["summary"]["calls"]), "llm_calls": int(plan["summary"]["llm_calls"]), "tool_calls": int(plan["summary"]["tool_calls"]), "mir_operators": planned_ops, "waves": int(plan["summary"]["waves"]),
                    "prompt_tokens_total": sum(len(v) for v in prompts.values()), "output_tokens_total": sum(int(c["output_tokens"]) for c in plan["calls"] if c["kind"] == "llm")},
        "observed": {"operator_events": len(op_events), "expected_operator_events": planned_ops * measured_iters, "total_events": len(events)},
        "timing_ns": {"started": started, "warmup_done": warm_done, "finished": finished, "warmup_wall_ms": (warm_done - started) / 1e6, "measured_wall_ms": (finished - warm_done) / 1e6},
        "determinism": {"checksums_match": deterministic, "reference_checksums": reference},
        "prompts": sample_outputs,
        "environment": {"host": socket.gethostname(), "python": platform.python_version(), "torch": torch.__version__, "cuda": torch.version.cuda, "transformers": transformers.__version__, "nvml_before": nvml_before, "nvml_after": nvml_after},
        "pass": deterministic and len(op_events) == planned_ops * measured_iters and measured_iters > 0,
    }
    (output_dir / "run_metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    return metadata


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Execute an AgentSys hybrid plan with real Qwen3 inference (transformers) on one GPU")
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, default=Path("/data3/docker_model/AgentSys/Qwen3-1.7B"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--device", type=int, default=1)
    parser.add_argument("--numa-node", type=int, default=1)
    parser.add_argument("--cpu-affinity", default="16-31,48-63")
    parser.add_argument("--warmup-iters", type=int, default=2)
    parser.add_argument("--measured-iters", type=int, default=3)
    parser.add_argument("--attn-implementation", default="sdpa", choices=["sdpa", "eager"])
    args = parser.parse_args(argv)
    m = run(plan_path=args.plan, model_dir=args.model_dir, output_dir=args.output_dir, device=args.device, numa_node=args.numa_node, cpu_affinity=args.cpu_affinity, warmup_iters=args.warmup_iters, measured_iters=args.measured_iters, attn_implementation=args.attn_implementation)
    print(json.dumps({"observed": m["observed"], "timing": m["timing_ns"], "pass": m["pass"], "probe": m["model"]["validation_probe"]["generated_text"]}, indent=2))
    return 0 if m["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
