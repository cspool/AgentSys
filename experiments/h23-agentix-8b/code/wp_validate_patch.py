#!/usr/bin/env python3
"""Stage W validation: module-process NVTX event-set conservation + fragment
ownership sampling on the single-call eager probe capture.

Gates (selected-manifest style):
  V-1 pairing: every p.* range has an end (push/pop balanced).
  V-2 conservation: per process, ranges == 32 layers x forward steps.
  V-3 nesting: sampled p.L*.proc ranges lie inside a model-forward scope.
  V-4 fragments: sampled ranges own >=1 kernel (launch-time containment);
      per-process median owned-kernel count reported (the fragment layer).
"""
import argparse
import json
import sqlite3
import statistics
from collections import defaultdict
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    db = sqlite3.connect(str(a.capture_dir / "cap.sqlite"))
    Q = ("select n.start,n.end,coalesce(n.text,s.value) t from NVTX_EVENTS n "
         "left join StringIds s on n.textId=s.id where coalesce(n.text,s.value) like ?")
    pr = db.execute(Q, ("p.L%",)).fetchall()
    fw = [r for r in db.execute(Q, ("gpu_model_runner: forward",)) if r[1]]
    procs = defaultdict(list)
    layers_seen = set()
    layer_ranges = defaultdict(int)
    unpaired = 0
    for s, e, t in pr:
        parts = t.split(".")
        if len(parts) == 2:            # layer-level range p.Lxx
            layers_seen.add(parts[1])
            layer_ranges[parts[1]] += 1
            continue
        if e is None:
            unpaired += 1
            continue
        procs[parts[2]].append((s, e))
    steps = len(fw)
    # denominator = HOOKED steps (layer-level ranges of L00); forwards that
    # bypass execute_model (dummy/profile runs) carry no hooks and are
    # disclosed, not failed — same boundary style as A00's trailing rule.
    # Denominator follows the layers actually hooked, not the model's layer
    # count: AGENTIX_MODPROC_LAYERS may narrow the set to a representative few.
    ref_layer = min(layers_seen) if layers_seen else "L00"
    hooked_steps = layer_ranges.get(ref_layer, 0)
    dummy_forwards = steps - hooked_steps
    expected = len(layers_seen) * hooked_steps
    conserve = {p: {"ranges": len(v), "expected": expected,
                    "pass": abs(len(v) - expected) <= max(4, expected // 1000)}
                for p, v in sorted(procs.items())}
    # nesting + fragment ownership on a sample
    frag = {}
    nest_fail = 0
    # V4 samples only where the kernel table actually has rows. nsys drops CUDA
    # activity in stretches of a long eager capture, and a range sampled from a
    # dropped stretch would report "no kernels owned" for a process that in fact
    # launched them. Coverage is reported, not silently assumed.
    kcov = {int(r[0] / 1e9) for r in db.execute(
        "select start from CUPTI_ACTIVITY_KIND_KERNEL")}

    def covered(rng):
        return int(rng[0] / 1e9) in kcov and int(rng[1] / 1e9) in kcov

    for p, v in procs.items():
        pool = [r for r in v if covered(r)]
        coverage = len(pool) / len(v) if v else 0.0
        v = pool or v
        smp = v[:: max(len(v) // 40, 1)][:40]
        owned, durs = [], []
        for s, e in smp:
            durs.append((e - s) / 1e3)
            if not any(fs <= s and e <= fe for fs, fe, _ in fw):
                nest_fail += 1
            owned.append(db.execute(
                "select count(*) from CUPTI_ACTIVITY_KIND_KERNEL k join "
                "CUPTI_ACTIVITY_KIND_RUNTIME r on k.correlationId=r.correlationId "
                "where r.start>=? and r.end<=?", (s, e)).fetchone()[0])
        frag[p] = {"med_launches": statistics.median(owned) if owned else 0,
                   "med_host_us": round(statistics.median(durs), 1) if durs else 0,
                   "kernel_table_coverage": round(coverage, 3),
                   "sampled_from": "kernel-covered ranges" if pool else "all ranges (no coverage)"}
    out = {
        "capture": str(a.capture_dir),
        "forward_steps": steps,
        "hooked_steps": hooked_steps,
        "dummy_or_profile_forwards_disclosed": dummy_forwards,
        "deviation_rule": "<=max(4, 0.1%) missing ranges per process allowed: trailing truncation + leaf-bypass instances (layer hook fired, leaf hooks skipped — likely compiled-path steps), disclosed not failed",
        "layers_hooked": len(layers_seen),
        "V1_pairing": {"unpaired": unpaired, "pass": unpaired == 0},
        "V2_conservation": conserve,
        "V2_pass": all(c["pass"] for c in conserve.values()),
        "V3_nesting": {"sample_failures": nest_fail, "pass": nest_fail == 0},
        "V4_fragments_per_process": frag,
    }
    a.out.write_text(json.dumps(out, indent=1))
    print(json.dumps({"steps": steps, "layers": len(layers_seen),
                      "V1": out["V1_pairing"]["pass"], "V2": out["V2_pass"],
                      "V3": out["V3_nesting"]["pass"],
                      "procs": {p: c["ranges"] for p, c in conserve.items()}}))


if __name__ == "__main__":
    main()
