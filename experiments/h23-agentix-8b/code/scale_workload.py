#!/usr/bin/env python3
"""Scale a workload's offered load while holding its composition fixed.

Replicates the program set and compresses arrivals to a target rate. Class mix,
per-call token counts and wave structure are copied verbatim, so a comparison
across the resulting ladder varies offered load and nothing else.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=Path, required=True)
    ap.add_argument("--factor", type=int, required=True, help="replication factor")
    ap.add_argument("--arrival-rate", type=float, required=True, help="programs/s")
    ap.add_argument("--class-mix", default="",
                    help='re-weight the class mix, e.g. "sharegpt=0.6,bfcl=0.25,lats=0.15"; '
                         'programs are drawn from the base set of that class, so per-call '
                         'token counts and wave structure still come from the base workload')
    ap.add_argument("--seed", type=int, default=23)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()

    base = json.loads(a.base.read_text())
    src = base["programs"]
    rng = random.Random(a.seed)
    progs = []
    gap = 1e9 / a.arrival_rate
    t = 0.0
    total = a.factor * len(src)
    if a.class_mix:
        mix = {}
        for part in a.class_mix.split(","):
            k, v = part.split("=")
            mix[k.strip()] = float(v)
        pool = {}
        for p in src:
            pool.setdefault(p["class"], []).append(p)
        missing = [k for k in mix if k not in pool]
        if missing:
            raise SystemExit(f"class not present in base workload: {missing}")
        # draw each program from its class's base programs, round-robin inside a
        # class so every base program is used evenly rather than sampled at random
        order, cursor = [], {k: 0 for k in mix}
        for k, w in mix.items():
            order += [k] * round(w * total)
        rng.shuffle(order)
        chosen = []
        for k in order:
            lst = pool[k]
            chosen.append(lst[cursor[k] % len(lst)])
            cursor[k] += 1
        src_seq = chosen
    else:
        src_seq = [p for _ in range(a.factor) for p in src]
    for p in src_seq:
        q = copy.deepcopy(p)
        q["program_id"] = f"p{len(progs):05d}"
        t += rng.expovariate(1.0 / gap)
        q["arrival_ns"] = int(t)
        progs.append(q)
    out = dict(base)
    out["programs"] = progs
    cfg = dict(base.get("config", {}))
    cfg.update({"arrival_rate_programs_per_s": a.arrival_rate,
                "scaled_from": str(a.base.name), "replication_factor": a.factor,
                "class_mix": a.class_mix or "unchanged from base",
                "note": ("offered-load ladder: composition copied verbatim from the base "
                         "workload, only the number of programs and their arrival rate change")})
    out["config"] = cfg
    out["summary"] = {
        "programs": len(progs),
        "llm_calls": sum(len(p["llm_calls"]) for p in progs),
        "prompt_tokens": sum(p["total_prompt_tokens"] for p in progs),
        "output_tokens": sum(p["total_output_tokens"] for p in progs),
        "arrival_span_s": round(progs[-1]["arrival_ns"] / 1e9, 2),
        "by_class": {c: sum(1 for p in progs if p["class"] == c)
                     for c in sorted({p["class"] for p in progs})},
    }
    a.output.write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({"out": str(a.output), **out["summary"],
                      "sha256": hashlib.sha256(a.output.read_bytes()).hexdigest()[:16]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
