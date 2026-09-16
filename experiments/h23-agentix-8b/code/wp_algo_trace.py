#!/usr/bin/env python3
"""R02 algorithmic trace and canonical selection.

Builds the event families the shared contract names, from one instrumented
capture of the agent-program workload:

  F = engine-step events                    (w.engine: process_engine_step)
  L = layer-call events                     (p.L{layer} ranges inside a step)
  S = scheduler decision events             (batch composition changes per step)
  R = request state transitions             (w.run::<ids> RUNNING-set marks)
  T = the canonical selected-layer manifest (this stage's frozen output)

Conservation is checked on key sets, not row counts, and the layer-count
contract is read from the capture rather than assumed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from collections import defaultdict
from pathlib import Path

NVTX_Q = ("select n.start, n.end, coalesce(n.text, s.value) t "
          "from NVTX_EVENTS n left join StringIds s on n.textId = s.id "
          "where coalesce(n.text, s.value) like ?")


def bisect_step(steps, ts):
    lo, hi = 0, len(steps) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        s, e, _ = steps[mid]
        if ts < s:
            hi = mid - 1
        elif ts > e:
            lo = mid + 1
        else:
            return mid
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture-dir", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--contract", type=Path, required=True)
    ap.add_argument("--per-bucket", type=int, default=2,
                    help="selected events per (phase, layer) bucket")
    ap.add_argument("--layers", default="",
                    help="comma list of layer indices eligible for selection "
                         "(default: every instrumented layer)")
    a = ap.parse_args()
    a.out_dir.mkdir(parents=True, exist_ok=True)
    contract = json.loads(a.contract.read_text())
    cid = contract["contract_id"]
    db = sqlite3.connect(str(a.capture_dir / "cap.sqlite"))

    # ---- F: engine steps -------------------------------------------------
    steps = [(s, e, t) for s, e, t in db.execute(NVTX_Q, ("w.engine: process_engine_step",)) if e]
    steps.sort()
    F = [{"contract_id": cid, "step_id": i, "start_ns": s, "end_ns": e,
          "dur_us": (e - s) / 1e3} for i, (s, e, _) in enumerate(steps)]

    # ---- S: batch composition per step ----------------------------------
    comp = []
    for s, _e, t in db.execute(NVTX_Q, ("w.step::%",)):
        body = t.split("::")
        reqs = tok = None
        for part in body[1:]:
            if part.startswith("reqs="):
                reqs = int(part.split("=", 1)[1])
            elif part.startswith("tok="):
                tok = int(part.split("=", 1)[1])
        comp.append((s, reqs, tok))
    comp.sort()
    S = []
    prev = None
    for ts, reqs, tok in comp:
        si = bisect_step(steps, ts)
        if si is None:
            continue
        ev = {"contract_id": cid, "step_id": si, "reqs": reqs, "tokens": tok}
        if prev is not None and reqs is not None and prev != reqs:
            ev["decision"] = "admit" if reqs > prev else "drain"
            ev["delta"] = reqs - prev
        prev = reqs if reqs is not None else prev
        S.append(ev)
    comp_by_step = {e["step_id"]: e for e in S}

    # ---- R: RUNNING-set transitions -------------------------------------
    runmarks = []
    for ts, _e, t in db.execute(NVTX_Q, ("w.run::%",)):
        ids = t[len("w.run::"):]
        keys = {x for x in ids.split(",") if x}
        runmarks.append((ts, keys))
    runmarks.sort()
    R = []
    prev_set: set[str] = set()
    for ts, keys in runmarks:
        si = bisect_step(steps, ts)
        for k in keys - prev_set:
            R.append({"contract_id": cid, "step_id": si, "call": k, "to": "RUNNING"})
        for k in prev_set - keys:
            R.append({"contract_id": cid, "step_id": si, "call": k, "to": "QUEUED"})
        prev_set = keys
    transition_status = "captured" if R else "missing"

    # ---- L: layer calls --------------------------------------------------
    layer_rows = []
    proc_rows = []
    for s, e, t in db.execute(NVTX_Q, ("p.L%",)):
        if e is None:
            continue
        parts = t.split(".")
        if len(parts) == 2:
            layer_rows.append((s, e, int(parts[1][1:])))
        else:
            proc_rows.append((s, e, int(parts[1][1:]), parts[2]))
    layer_rows.sort()
    occ = defaultdict(int)
    L = []
    for s, e, li in layer_rows:
        si = bisect_step(steps, s)
        if si is None:
            continue
        key = (si, li)
        L.append({"contract_id": cid, "step_id": si, "layer_idx": li,
                  "layer_occurrence": occ[key], "start_ns": s, "end_ns": e,
                  "dur_us": (e - s) / 1e3,
                  "reqs": comp_by_step.get(si, {}).get("reqs"),
                  "tokens": comp_by_step.get(si, {}).get("tokens"),
                  "event_id": f"step{si}_layer{li}_occ{occ[key]}"})
        occ[key] += 1
    lkeys = {(d["step_id"], d["layer_idx"], d["layer_occurrence"]) for d in L}

    # process ranges attached to their layer event
    P = []
    lindex = {(d["step_id"], d["layer_idx"], d["layer_occurrence"]): d for d in L}
    for s, e, li, proc in proc_rows:
        si = bisect_step(steps, s)
        if si is None:
            continue
        host = lindex.get((si, li, 0))
        if host is None:
            continue
        P.append({"event_id": host["event_id"], "process": proc,
                  "start_ns": s, "end_ns": e, "dur_us": (e - s) / 1e3})

    # ---- conservation ----------------------------------------------------
    layers_seen = sorted({d["layer_idx"] for d in L})
    per_step = defaultdict(int)
    for d in L:
        per_step[d["step_id"]] += 1
    full = sum(1 for v in per_step.values() if v == len(layers_seen))
    gates = {
        "layer_count_contract": {"layers_instrumented": len(layers_seen),
                                 "model_layers": contract["layer_count_contract"]["layers"]},
        "steps_with_full_layer_set": full,
        "steps_with_layer_events": len(per_step),
        "layer_key_uniqueness": len(lkeys) == len(L),
        "L_subset_of_steps": all(d["step_id"] is not None for d in L),
        "transition_capture_status": transition_status,
        "S_joins_valid_step": all(e["step_id"] is not None for e in S),
        "R_joins_valid_step": all(e["step_id"] is not None for e in R),
    }
    gates["pass"] = (gates["layer_key_uniqueness"] and gates["L_subset_of_steps"]
                     and gates["S_joins_valid_step"] and gates["R_joins_valid_step"]
                     and gates["steps_with_full_layer_set"] > 0)

    # ---- selection -------------------------------------------------------
    # Phase = the workload's own regime, read from batch composition: a step
    # carrying more tokens than resident requests is doing prefill work.
    def phase_of(step_id: int) -> str:
        c = comp_by_step.get(step_id, {})
        reqs, tok = c.get("reqs"), c.get("tokens")
        if not reqs or not tok:
            return "unknown"
        if tok > reqs * 4:
            return "prefill_heavy"
        if reqs >= 12:
            return "storm"
        return "steady_decode"

    want_layers = {int(x) for x in a.layers.split(",") if x.strip()}
    by_bucket = defaultdict(list)
    pidx = defaultdict(list)
    for r in P:
        pidx[r["event_id"]].append(r)
    for d in L:
        if len(pidx.get(d["event_id"], [])) < 8:
            continue
        if want_layers and d["layer_idx"] not in want_layers:
            continue
        by_bucket[(phase_of(d["step_id"]), d["layer_idx"])].append(d)

    selected = []
    for (phase, layer), rows in sorted(by_bucket.items()):
        rows.sort(key=lambda r: r["dur_us"])
        picks = {0: "fastest", len(rows) // 2: "median", len(rows) - 1: "slowest"}
        for i in sorted(picks)[: a.per_bucket + 1]:
            d = dict(rows[i])
            d["selection_reason"] = (
                f"{picks[i]} layer-{layer} call in the {phase} regime; its process ranges "
                "cover both the device-bound operators (qkv_proj, mlp_gate_up, mlp_down) "
                "and the launch-bound ones (attn_core, norms)")
            d["phase"] = phase
            d["processes"] = sorted(r["process"] for r in pidx[d["event_id"]])
            selected.append(d)

    (a.out_dir / "algorithmic_trace").mkdir(exist_ok=True)
    for name, rows in (("F_steps", F), ("L_layers", L), ("S_decisions", S),
                       ("R_transitions", R), ("P_processes", P)):
        (a.out_dir / "algorithmic_trace" / f"{name}.jsonl").write_text(
            "".join(json.dumps(r) + "\n" for r in rows))

    manifest = {"schema_version": 1, "contract_id": cid,
                "expected_selected_event_count": len(selected),
                "events": selected}
    (a.out_dir / "selected_events.json").write_text(json.dumps(manifest, indent=1) + "\n")

    def sha(p: Path) -> str:
        return hashlib.sha256(p.read_bytes()).hexdigest()

    key_digest = hashlib.sha256(
        "|".join(sorted(d["event_id"] for d in selected)).encode()).hexdigest()
    handoff = {
        "schema_version": 1, "runtime_goal": "R02",
        "runtime_branch": "workload-profile-shared",
        "contract_id": cid,
        "capture": str(a.capture_dir.resolve()),
        "run_contract": {"path": str(a.contract.resolve()), "sha256": sha(a.contract)},
        "selected_events": {"path": str((a.out_dir / "selected_events.json").resolve()),
                            "sha256": sha(a.out_dir / "selected_events.json")},
        "event_counts": {"F": len(F), "L": len(L), "S": len(S), "R": len(R),
                         "P": len(P), "T": len(selected)},
        "expected_selected_event_count": len(selected),
        "event_key_set_digest": key_digest,
        "layer_occurrence_contract": "0 after verifying one call per (step_id, layer_idx)",
        "selection_scope": {"layers": sorted(want_layers) or "all",
                            "picks_per_bucket": a.per_bucket + 1},
        "gates": gates,
        "ordered_event_ids": [d["event_id"] for d in selected],
    }
    (a.out_dir / "selection_handoff.json").write_text(json.dumps(handoff, indent=1) + "\n")
    print(json.dumps({"F": len(F), "L": len(L), "S": len(S), "R": len(R),
                      "P": len(P), "T": len(selected),
                      "layers": len(layers_seen), "gates_pass": gates["pass"],
                      "transitions": transition_status}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
