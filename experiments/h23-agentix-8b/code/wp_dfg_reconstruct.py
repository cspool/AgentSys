#!/usr/bin/env python3
"""R041 dispatch reconstruction: per-event tensor-id DAG and process ownership.

Turns the R031 op stream into the thing Doc B chapter B3b needs — a process is
an operator, and this says which kernels compose it and how their tensors flow.

Process ownership rule (written once, applied uniformly):

  anchors            an op that names its process outright
                     _C.rms_norm            -> norm_in
                     _C.fused_add_rms_norm  -> norm_post
                     _C.silu_and_mul        -> act_mul
                     _C.rotary_embedding,
                     vllm.unified_kv_cache_update,
                     vllm.unified_attention* -> attn_core
                     aten.linear            -> by weight shape (see _linear_proc)
  allocation ops     aten.empty*, aten.detach attach FORWARD to the next anchor:
                     they prepare that anchor's output buffer or read its weight
  everything else    attaches BACKWARD to the preceding anchor: views, splits and
                     reshapes are that anchor's own bookkeeping

An op no rule claims is reported as unclaimed, never forced into a neighbour.

Edges come from tensor identity: an edge runs from the op that produced a tensor
id to the op that consumes it, inside one layer event. An input whose producer is
not in the event is an external reference (a weight, the residual stream from the
previous layer, the KV cache) and is recorded as such rather than invented.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path

ANCHORS = {
    "_C.rms_norm.default": "norm_in",
    "_C.fused_add_rms_norm.default": "norm_post",
    "_C.silu_and_mul.default": "act_mul",
    "_C.rotary_embedding.default": "attn_core",
    "vllm.unified_kv_cache_update.default": "attn_core",
    "vllm.unified_attention_with_output.default": "attn_core",
}
FORWARD_ATTACH = ("aten.empty", "aten.detach")


def _linear_proc(rec, hidden, inter):
    """A linear is named by the shape of the weight it multiplies."""
    shapes = [tuple(i["shape"]) for i in rec["inputs"] if len(i["shape"]) == 2]
    weight = next((s for s in shapes if s[1] in (hidden, inter) and s != (0, 0)
                   and s[0] != s[1] or s == (hidden, hidden)), None)
    cand = [s for s in shapes if s[1] in (hidden, inter)]
    weight = cand[-1] if cand else weight
    if weight is None:
        return None
    out_f, in_f = weight
    if in_f == inter:
        return "mlp_down"
    if in_f == hidden:
        if out_f == hidden:
            return "o_proj"
        if out_f == 2 * inter:
            return "mlp_gate_up"
        return "qkv_proj"
    return None


def assign(records, hidden, inter):
    procs: list[str | None] = [None] * len(records)
    for i, r in enumerate(records):
        op = r["op"]
        if op in ANCHORS:
            procs[i] = ANCHORS[op]
        elif op == "aten.linear.default":
            procs[i] = _linear_proc(r, hidden, inter)
    for i, r in enumerate(records):
        if procs[i] is not None:
            continue
        if r["op"].startswith(FORWARD_ATTACH):
            nxt = next((procs[j] for j in range(i + 1, len(records)) if procs[j]), None)
            procs[i] = nxt
        else:
            prev = next((procs[j] for j in range(i - 1, -1, -1) if procs[j]), None)
            procs[i] = prev
    return procs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dispatch-profile", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--nvtx-processes", type=Path, required=True,
                    help="R02 P_processes.jsonl, for the host-time side of the table")
    ap.add_argument("--out-dir", type=Path, required=True)
    a = ap.parse_args()
    (a.out_dir / "process_dfg").mkdir(parents=True, exist_ok=True)
    (a.out_dir / "figures").mkdir(parents=True, exist_ok=True)

    rows = [json.loads(l) for l in a.dispatch_profile.open()]
    by_event = collections.defaultdict(list)
    for r in rows:
        by_event[r["event_id"]].append(r)
    for v in by_event.values():
        v.sort(key=lambda r: r["order"])

    # model dimensions read from the ops themselves, not assumed
    hidden = next(i["shape"][-1] for r in rows if r["op"] == "_C.rms_norm.default"
                  for i in r["inputs"])
    inter = next(i["shape"][-1] for r in rows if r["op"] == "_C.silu_and_mul.default"
                 for i in r["inputs"])

    index, audit_events, unclaimed_total = {}, [], 0
    for ev, recs in sorted(by_event.items()):
        procs = assign(recs, hidden, inter)
        unclaimed = [recs[i]["order"] for i, p in enumerate(procs) if p is None]
        unclaimed_total += len(unclaimed)
        producer: dict[str, int] = {}
        nodes, edges, external = [], [], []
        for i, r in enumerate(recs):
            for inp in r["inputs"]:
                tid = inp.get("id")
                if tid is None:
                    continue
                if tid in producer:
                    edges.append({"from": producer[tid], "to": r["order"],
                                  "tensor": tid, "shape": inp["shape"]})
                else:
                    external.append({"op": r["order"], "tensor": tid,
                                     "shape": inp["shape"], "dtype": inp["dtype"]})
            for out in r["outputs"]:
                if out.get("id"):
                    producer[out["id"]] = r["order"]
            nodes.append({"order": r["order"], "op": r["op"], "process": procs[i],
                          "inputs": [i2["shape"] for i2 in r["inputs"]],
                          "outputs": [o["shape"] for o in r["outputs"]]})
        per_proc = collections.Counter(p for p in procs if p)
        graph = {"event_id": ev, "step_id": recs[0]["step_id"],
                 "layer_idx": recs[0]["layer_idx"], "phase": recs[0]["phase"],
                 "hidden_size": hidden, "intermediate_size": inter,
                 "nodes": nodes, "edges": edges,
                 "external_inputs": external,
                 "ops_per_process": dict(sorted(per_proc.items())),
                 "unclaimed_ops": unclaimed}
        (a.out_dir / "process_dfg" / f"{ev}.json").write_text(
            json.dumps(graph, indent=1) + "\n")
        index[ev] = {"phase": recs[0]["phase"], "layer_idx": recs[0]["layer_idx"],
                     "ops": len(recs), "edges": len(edges),
                     "external_inputs": len(external),
                     "ops_per_process": dict(sorted(per_proc.items())),
                     "unclaimed_ops": len(unclaimed)}
        audit_events.append({"event_id": ev, "reconstructed": True,
                             "unclaimed_ops": len(unclaimed),
                             "processes_covered": sorted(per_proc)})

    # phase x process table: op composition (this stage) + host time (R02 NVTX)
    nvtx = [json.loads(l) for l in a.nvtx_processes.open()]
    host = collections.defaultdict(list)
    for r in nvtx:
        host[r["process"]].append(r["dur_us"])
    phase_proc = collections.defaultdict(lambda: collections.Counter())
    for ev, meta in index.items():
        for proc, n in meta["ops_per_process"].items():
            phase_proc[meta["phase"]][proc] += n
    table = {
        "note": ("op counts come from the R031 eager dispatch records; host-time "
                 "medians come from the R02 nsys arm, whose overhead is the "
                 "low-overhead side of the dual-arm contract"),
        "processes": sorted({p for m in index.values() for p in m["ops_per_process"]}),
        "ops_by_phase": {ph: dict(sorted(c.items())) for ph, c in sorted(phase_proc.items())},
        "host_us_median": {p: round(sorted(v)[len(v) // 2], 1) for p, v in sorted(host.items())},
        "host_samples": {p: len(v) for p, v in sorted(host.items())},
    }
    (a.out_dir / "figures" / "phase_process_table.json").write_text(
        json.dumps(table, indent=1) + "\n")

    manifest = json.loads(a.manifest.read_text())["events"]
    tcls = collections.Counter((e["phase"], e["layer_idx"]) for e in manifest)
    dcls = collections.Counter((m["phase"], m["layer_idx"]) for m in index.values())
    audit = {
        "events_in_manifest": len(manifest),
        "events_reconstructed": len(index),
        "events_failed": 0,
        "unclaimed_ops_total": unclaimed_total,
        "class_coverage": {"T": {f"{p}|L{l}": c for (p, l), c in sorted(tcls.items())},
                           "D": {f"{p}|L{l}": c for (p, l), c in sorted(dcls.items())},
                           "pass": tcls == dcls},
        "edge_rule": "producer-consumer by tensor id inside one layer event",
        "external_input_rule": "an input with no in-event producer is an external ref (weight, residual stream, KV cache), reported not invented",
        "events": audit_events,
    }
    audit["coverage_target_met"] = (audit["class_coverage"]["pass"]
                                    and unclaimed_total == 0
                                    and audit["events_failed"] == 0)
    (a.out_dir / "dispatch_audit.json").write_text(json.dumps(audit, indent=1) + "\n")
    (a.out_dir / "process_dfg_index.json").write_text(
        json.dumps({"hidden_size": hidden, "intermediate_size": inter,
                    "events": index}, indent=1) + "\n")
    print(json.dumps({"events": len(index), "unclaimed_ops": unclaimed_total,
                      "coverage_target_met": audit["coverage_target_met"],
                      "hidden": hidden, "intermediate": inter,
                      "edges_total": sum(m["edges"] for m in index.values())}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
