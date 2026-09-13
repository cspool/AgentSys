#!/usr/bin/env python3
"""Agentix-protocol program workload: three program classes + Mixed, Poisson arrivals.

The Agentix paper (KB: paper_secs/paper_20260824/Agentix .../§6.1-6.2) samples
*programs* — not LLM calls — from three workload classes plus a Mixed class, and
generates program arrivals with a Poisson process. Its traces are not public and
are not on this machine, so this module synthesises program DAGs with the same
structure classes and records that fact in the manifest:

  sharegpt — chatbot conversations: few calls, decode-heavy
  bfcl     — ReAct tool use: prefill-heavy calls with long tool gaps
  lats     — MCTS search: an order of magnitude more calls per program

Per-class call counts and prefill/decode token means are calibrated to the
paper's own reported statistics (§6.1, Fig. 11); the traces themselves are not
public, so the streams are synthesised, not replayed.

Everything is seeded, so a workload file is reproducible bit-for-bit and carries
its own sha256.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path
from typing import Any

# Program class parameters, set from the Agentix paper's own workload statistics
# (§6.1 and Fig. 11): per-program LLM-call counts are long-tailed, and each class
# has a characteristic prefill/decode shape.
#
#   ShareGPT (chatbot): mean 6.66 calls, max 80; prefill 255.65, decode 276.81 -> decode-heavy
#   BFCL (ReAct):       mean 10.75 calls, max 70; prefill 735.06, decode 34.14  -> prefill-heavy
#   LATS (MCTS):        mean 159.71 calls;        prefill 467.24, decode 72.64
#
# Call counts are drawn lognormal (long-tailed, per Fig. 11d) and clipped to the
# paper's maximum; token counts are drawn lognormal about the paper's mean.
# ``width`` is the program's intra-program parallelism: the paper marks ShareGPT and
# BFCL single-threaded and LATS multi-threaded ("many parallel LLM calls", §6.1), so
# only LATS fans out. A program executes as a sequence of waves; the calls inside a
# wave are issued concurrently and the next wave waits for the wave to finish.
CLASSES: dict[str, dict[str, Any]] = {
    "sharegpt": {"calls_mean": 6.66, "calls_sigma": 0.95, "calls_max": 80, "tool_ms": 20.0,
                 "prefill_mean": 255.65, "decode_mean": 276.81, "width": 1},
    "bfcl": {"calls_mean": 10.75, "calls_sigma": 0.80, "calls_max": 70, "tool_ms": 250.0,
             "prefill_mean": 735.06, "decode_mean": 34.14, "width": 1},
    "lats": {"calls_mean": 159.71, "calls_sigma": 0.55, "calls_max": 2000, "tool_ms": 120.0,
             "prefill_mean": 467.24, "decode_mean": 72.64, "width": 5},
}
TOKEN_SIGMA = 0.45  # spread of the per-call token lengths about each class mean


def _lognormal(rng: random.Random, mean: float, sigma: float) -> float:
    """Lognormal sample whose expectation is `mean`."""
    import math

    mu = math.log(mean) - sigma * sigma / 2.0
    return rng.lognormvariate(mu, sigma)


MIXED_WEIGHTS = {"sharegpt": 1.0, "bfcl": 1.0, "lats": 1.0}  # paper: sampled equally


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sample_class(rng: random.Random, workload_class: str) -> str:
    if workload_class != "mixed":
        return workload_class
    names = list(MIXED_WEIGHTS)
    return rng.choices(names, weights=[MIXED_WEIGHTS[n] for n in names], k=1)[0]


def build_program(rng: random.Random, program_id: str, workload_class: str, arrival_ns: int) -> dict[str, Any]:
    cls = _sample_class(rng, workload_class)
    p = CLASSES[cls]
    n_calls = max(1, min(int(round(_lognormal(rng, p["calls_mean"], p["calls_sigma"]))), p["calls_max"]))
    width = int(p.get("width", 1))
    calls = []
    index = 0
    wave = 0
    # Waves of `width` parallel calls (width == 1 gives the single-threaded chain).
    while index < n_calls:
        w = min(width, n_calls - index) if width > 1 else 1
        parents = [c["index"] for c in calls if c["wave"] == wave - 1] if wave else []
        for _ in range(w):
            prompt = max(8, int(round(_lognormal(rng, p["prefill_mean"], TOKEN_SIGMA))))
            out = max(1, int(round(_lognormal(rng, p["decode_mean"], TOKEN_SIGMA))))
            # interception: a wave becomes ready one tool/environment step after its parents
            calls.append({"index": index, "wave": wave, "parents": parents,
                          "prompt_tokens": prompt, "output_tokens": out,
                          "tool_delay_ns": 0 if wave == 0 else int(rng.expovariate(1.0 / p["tool_ms"]) * 1e6)})
            index += 1
        wave += 1
    return {"program_id": program_id, "class": cls, "arrival_ns": arrival_ns, "llm_calls": calls,
            "waves": wave, "width": width,
            "total_prompt_tokens": sum(c["prompt_tokens"] for c in calls),
            "total_output_tokens": sum(c["output_tokens"] for c in calls)}


def build(workload_class: str, arrival_rate: float, duration_s: float, seed: int, max_programs: int) -> dict[str, Any]:
    rng = random.Random(seed)
    programs: list[dict[str, Any]] = []
    t_ns = 0.0
    mean_gap_ns = 1e9 / arrival_rate
    while len(programs) < max_programs:
        t_ns += rng.expovariate(1.0 / mean_gap_ns)  # Poisson arrivals
        if t_ns > duration_s * 1e9:
            break
        programs.append(build_program(rng, f"p{len(programs):05d}", workload_class, int(t_ns)))
    return {
        "schema_version": 1,
        "protocol": "Agentix §6.1-6.2 (program-level, Poisson arrivals)",
        "provenance": {
            "source": "synthesised locally with the same program-class structure; the paper's traces are not public and not present on this machine",
            "class_parameters": CLASSES,
            "calibrated_to": "Agentix paper §6.1 / Fig. 11 per-class means (calls, prefill tokens, decode tokens)",
            "mixed_weights": MIXED_WEIGHTS,
            "interception_model": "exponential tool delay before each wave; calls inside a wave run concurrently",
            "threading": "paper §6.1: ShareGPT and BFCL single-threaded, LATS multi-threaded",
        },
        "config": {"workload_class": workload_class, "arrival_rate_programs_per_s": arrival_rate,
                   "duration_s": duration_s, "seed": seed, "max_programs": max_programs},
        "summary": {"programs": len(programs),
                    "llm_calls": sum(len(p["llm_calls"]) for p in programs),
                    "prompt_tokens": sum(p["total_prompt_tokens"] for p in programs),
                    "output_tokens": sum(p["total_output_tokens"] for p in programs),
                    "by_class": {c: sum(1 for p in programs if p["class"] == c) for c in CLASSES},
                    "multi_threaded_programs": sum(1 for p in programs if p.get("width", 1) > 1)},
        "programs": programs,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Build an Agentix-protocol program workload")
    ap.add_argument("--workload-class", default="mixed", choices=["sharegpt", "bfcl", "lats", "mixed"])
    ap.add_argument("--arrival-rate", type=float, required=True, help="programs per second")
    ap.add_argument("--duration-s", type=float, default=60.0)
    ap.add_argument("--seed", type=int, default=20260913)
    ap.add_argument("--max-programs", type=int, default=5000)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()
    a.output.parent.mkdir(parents=True, exist_ok=True)
    doc = build(a.workload_class, a.arrival_rate, a.duration_s, a.seed, a.max_programs)
    a.output.write_text(json.dumps(doc, indent=2) + "\n")
    doc["sha256"] = _sha256(a.output)
    print(json.dumps({"output": str(a.output), "sha256": doc["sha256"], **doc["summary"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
