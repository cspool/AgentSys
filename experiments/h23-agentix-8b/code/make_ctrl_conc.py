#!/usr/bin/env python3
"""Controlled-concurrency workload for the R10_PROCESS (Doc B) batch trace.

batch8/16-style acquisition: instead of a Poisson stream, concurrency phases
are CONSTRUCTED so each Agentix mechanism has a dedicated, findable window:

  W  warmup            t=0      1 program, excluded from analysis windows
  P1 steady decode     t=5 s    16 fresh 1-call programs, output < Q0 quantum
                                -> full 16-slot decode batch, no preemption:
                                the clean step/kernel-universe baseline
  P2 history build     t=12 s   4 "aged" programs run 3 medium calls each,
                                accumulating attained service past the Q2/Q3
                                bounds (the process table fills)
  P3 admission storm   t=30 s   the aged programs' 4th (long) calls arrive
                                TOGETHER with 8 fresh short programs:
                                admission spread Q0 vs Q2/Q3 in one window,
                                quantum exhaustion -> demote/requeue/re-prefill
  P4 drain             tail     queue empties; completion tail

Phase boundaries are written into the JSON (analysis windows are constructed,
not searched). Token lengths are chosen against the client MLFQ quanta
(32/64/128/256) and bounds (2/8/32 s attained).
"""
import argparse
import hashlib
import json
import random
from pathlib import Path


def prog(pid, cls, arrival_s, calls, width=1):
    return {"program_id": pid, "class": cls, "arrival_ns": int(arrival_s * 1e9),
            "llm_calls": [
                {"index": i, "wave": c.get("wave", i), "parents": [],
                 "prompt_tokens": c["p"], "output_tokens": c["o"],
                 "tool_delay_ns": int(c.get("d", 0) * 1e9)}
                for i, c in enumerate(calls)],
            "waves": max(c.get("wave", i) for i, c in enumerate(calls)) + 1,
            "width": width,
            "total_prompt_tokens": sum(c["p"] for c in calls),
            "total_output_tokens": sum(c["o"] for c in calls)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    rng = random.Random(23)
    P = []
    # W: warmup
    P.append(prog("w0000", "bfcl", 0.0, [{"p": 64, "o": 16}, {"p": 96, "o": 16, "d": 0.2}]))
    # P1: steady full-batch decode, one quantum per call (no chunking)
    for i in range(16):
        P.append(prog(f"st{i:02d}", "sharegpt", 5.0 + 0.01 * i,
                      [{"p": 256 + rng.randrange(64), "o": 28}]))
    # P2: aged programs accumulate attained service (3 medium calls each)
    for i in range(4):
        P.append(prog(f"ag{i:02d}", "lats", 12.0 + 0.05 * i,
                      [{"p": 512, "o": 300, "d": 0.2},
                       {"p": 640, "o": 300, "d": 0.2},
                       {"p": 768, "o": 300, "d": 0.2},
                       # the long 4th call lands in P3 via the tool delay chain
                       {"p": 1024, "o": 512}]))
    # P3: fresh short burst arriving into the storm
    for i in range(8):
        P.append(prog(f"fr{i:02d}", "bfcl", 30.0 + 0.01 * i,
                      [{"p": 128, "o": 48, "d": 0.3},
                       {"p": 160, "o": 48, "d": 0.3},
                       {"p": 192, "o": 48}]))
    spec = {
        "schema_version": 1,
        "protocol": "ctrl_conc16: constructed concurrency phases (batch8/16-style) "
                    "for the process-hierarchy trace; phases W/P1/P2/P3/P4",
        "provenance": {"generator": "make_ctrl_conc.py", "seed": 23},
        "config": {"workload_class": "ctrl_conc16", "arrival_rate_programs_per_s": 0.0,
                   "seed": 23, "max_num_seqs": 16, "quanta_tokens": [32, 64, 128, 256],
                   "mlfq_bounds_s": [0, 2, 8, 32]},
        "phases": {"W": [0, 5], "P1": [5, 11], "P2": [12, 27],
                   "P3": [27, 38], "P4": [38, None]},
        "summary": {"programs": len(P),
                    "llm_calls": sum(len(p["llm_calls"]) for p in P),
                    "total_output_tokens": sum(p["total_output_tokens"] for p in P)},
        "programs": P,
    }
    txt = json.dumps(spec, indent=1)
    a.out.write_text(txt)
    print(json.dumps({"out": str(a.out), "sha256": hashlib.sha256(txt.encode()).hexdigest()[:16],
                      **spec["summary"]}))


if __name__ == "__main__":
    main()
