#!/usr/bin/env python3
"""R042 FX reconstruction, per-process explanation and coverage audit.

Groups the fixed-input FX nodes into the eight process units of a decoder layer,
explains each process by what it reads, what it writes and which axis dominates
its cost, and audits coverage against the R02 manifest.

The grouping rule is the same anchor rule the dispatch branch used, restated for
FX targets. A node no rule claims is reported unclaimed, never folded into a
neighbour. The explanations carry no timing: a fixed-input DAG has none, and the
device-bound vs launch-bound split is cited from the R041/R01 evidence.
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
    # present only in the in-context graphs, and they must anchor: a get_attr for
    # the o_proj weight is hoisted right before them, so without an anchor of
    # their own they attach backward to o_proj and attention loses its own ops.
    "vllm.unified_kv_cache_update.default": "attn_core",
    "vllm.unified_attention_with_output.default": "attn_core",
}
FORWARD_ATTACH = ("aten.detach", "aten.empty", "get_attr", "placeholder")

# Which linear a matmul is, named by the weight it transposes.
def linear_proc(shape, hidden, inter):
    if shape is None or len(shape) != 2:
        return None
    a, b = shape
    out_f, in_f = (b, a) if a == hidden or a == inter else (a, b)
    if in_f == inter:
        return "mlp_down"
    if in_f == hidden and out_f == hidden:
        return "o_proj"
    if in_f == hidden and out_f == 2 * inter:
        return "mlp_gate_up"
    if in_f == hidden:
        return "qkv_proj"
    return None


AXIS = {
    "norm_in": ("hidden states of the step's tokens", "the normalized copy plus the residual it carries forward", "token count"),
    "qkv_proj": ("the normalized hidden states", "one fused q/k/v block", "hidden size x (q + 2 kv) — the widest weight before the MLP"),
    "attn_core": ("q/k/v plus the KV cache blocks of every resident request", "the attention output", "sequence length, and the number of resident requests"),
    "o_proj": ("the attention output", "the projected residual contribution", "hidden size squared"),
    "norm_post": ("the residual stream after attention", "the normalized MLP input", "token count"),
    "mlp_gate_up": ("the normalized hidden states", "the gate and up projections as one block", "hidden size x 2 x intermediate — the largest single weight in the layer"),
    "act_mul": ("the gate and up halves", "their gated product", "token count x intermediate"),
    "mlp_down": ("the gated intermediate activations", "the layer's output contribution", "intermediate x hidden"),
}
BOUNDNESS = {
    "qkv_proj": "device-bound", "mlp_gate_up": "device-bound", "mlp_down": "device-bound",
    "o_proj": "device-bound", "attn_core": "launch-bound",
    "norm_in": "launch-bound", "norm_post": "launch-bound", "act_mul": "launch-bound",
}


def assign(nodes, hidden, inter):
    procs: list[str | None] = [None] * len(nodes)
    for i, n in enumerate(nodes):
        tgt = n["target"]
        if tgt in ANCHORS:
            procs[i] = ANCHORS[tgt]
        elif tgt in ("aten.mm.default", "aten.addmm.default"):
            procs[i] = linear_proc(nodes[i - 1].get("shape"), hidden, inter)
    for i, n in enumerate(nodes):
        if procs[i] is not None or n["op"] == "output":
            continue
        if n["target"].startswith(FORWARD_ATTACH) or n["op"] in ("get_attr", "placeholder"):
            procs[i] = next((procs[j] for j in range(i + 1, len(nodes)) if procs[j]), None)
        else:
            procs[i] = next((procs[j] for j in range(i - 1, -1, -1) if procs[j]), None)
    return procs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fx-dir", type=Path, required=True)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--dispatch-index", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    a = ap.parse_args()
    (a.out_dir / "figures").mkdir(parents=True, exist_ok=True)
    disp = json.loads(a.dispatch_index.read_text())
    hidden, inter = disp["hidden_size"], disp["intermediate_size"]

    per_frag, unclaimed_total, axes = {}, 0, collections.defaultdict(list)
    sources = sorted((a.fx_dir / "fx_trace").glob("*.json"))
    # The in-context graphs carry the attention op and the KV cache update, which
    # no offline graph can hold; they complete attn_core's coverage.
    sources += sorted(q for q in (a.fx_dir / "fx_incontext").glob("*.json")
                      if q.name != "incontext_index.json")
    for path in sources:
        g = json.loads(path.read_text())
        nodes = g["nodes"]
        procs = assign(nodes, hidden, inter)
        unclaimed = [nodes[i]["name"] for i, p in enumerate(procs)
                     if p is None and nodes[i]["op"] != "output"]
        unclaimed_total += len(unclaimed)
        counts = collections.Counter(p for p in procs if p)
        for i, p in enumerate(procs):
            if p and nodes[i]["shape"]:
                axes[(p, g["phase"])].append(tuple(nodes[i]["shape"]))
        per_frag[path.stem] = {
            "phase": g["phase"], "layer_idx": g["layer_idx"],
            "fragment": g["fragment"], "tokens_in_step": g["tokens"],
            "reqs_in_step": g["reqs"],
            "input_shape": g["input_shapes"]["hidden_states"],
            "nodes": len(nodes), "nodes_per_process": dict(sorted(counts.items())),
            "unclaimed": unclaimed,
            "node_assignment": [{"name": nodes[i]["name"], "target": nodes[i]["target"],
                                 "process": procs[i], "shape": nodes[i]["shape"],
                                 "users": nodes[i]["users"]}
                                for i in range(len(nodes))],
        }

    claimed = sorted({p for f in per_frag.values() for p in f["nodes_per_process"]})
    all_procs = sorted(AXIS)
    # attn_core is claimed by its rotary-embedding anchor, but the attention op
    # itself never enters an offline graph. Reporting it as covered on the
    # strength of rope alone would overstate what this branch proves.
    attn_ops = {n["target"] for f in per_frag.values()
                for n in f["node_assignment"] if n["process"] == "attn_core"}
    attn_full = any("unified_attention" in t for t in attn_ops)
    partial = {} if attn_full else {
        "attn_core": {"present": sorted(attn_ops),
                      "missing": "vllm.unified_attention_with_output and the KV cache update"}}
    covered = [p for p in claimed if p not in partial]
    uncovered = [p for p in all_procs if p not in claimed]

    notes = []
    for proc in all_procs:
        shapes = sorted({s for (p, _ph), v in axes.items() if p == proc for s in v})
        reads, writes, axis = AXIS[proc]
        state = ("covered by the FX graphs" if proc in covered
                 else ("partially covered: " + partial[proc]["missing"] + " is absent"
                       if proc in partial
                       else "not covered here; its ops come from the dispatch branch"))
        notes.append({
            "process": proc, "coverage": state, "reads": reads, "writes": writes,
            "dominant_axis": axis, "boundness": BOUNDNESS[proc],
            "boundness_evidence": "R01 fragment ownership + R041 op composition; the FX graph itself carries no timing",
            "observed_shapes": [list(s) for s in shapes[:6]],
            "caption": (
                f"{proc} reads {reads} and writes {writes}, with cost set by {axis}. "
                f"It is {BOUNDNESS[proc]} in this engine, so the lever that moves it is "
                + ("more work per launch, not a faster kernel."
                   if BOUNDNESS[proc] == "launch-bound"
                   else "memory traffic and matmul shape, not launch count.")),
        })

    # tensor-axis figure data: shape by process and phase, with the step composition
    fig = collections.defaultdict(dict)
    for (proc, phase), shapes in sorted(axes.items()):
        widths = sorted({s[-1] for s in shapes if s})
        tokens = sorted({s[0] for s in shapes if len(s) == 2})
        fig[proc][phase] = {"widths": widths, "token_dims": tokens}
    steps = {f["phase"]: {"tokens_in_step": f["tokens_in_step"],
                          "reqs_in_step": f["reqs_in_step"],
                          "input_shape": f["input_shape"]}
             for f in per_frag.values()}
    (a.out_dir / "figures" / "tensor_axes.json").write_text(json.dumps(
        {"note": "shape only; the sampling step's composition is kept next to it so a "
                 "shape is never read without the batch it came from",
         "step_composition": steps, "by_process": dict(fig)}, indent=1) + "\n")

    manifest = json.loads(a.manifest.read_text())["events"]
    tcls = collections.Counter((e["phase"], e["layer_idx"]) for e in manifest)
    xcls = collections.Counter()
    for f in per_frag.values():
        xcls[(f["phase"], f["layer_idx"])] += 1
    # offline contributes two fragments per event, in-context one more
    xcls = collections.Counter({k: max(1, v // 3) for k, v in xcls.items()})
    audit = {
        "events_in_manifest": len(manifest),
        "fragments": len(per_frag),
        "class_coverage": {"T": {f"{p}|L{l}": c for (p, l), c in sorted(tcls.items())},
                           "X": {f"{p}|L{l}": c for (p, l), c in sorted(xcls.items())},
                           "note": ("T holds two picks per class, X holds one sampled event per "
                                    "class: the FX branch samples one live activation per class, "
                                    "so class coverage is complete while per-pick coverage is not"),
                           "classes_pass": set(tcls) == set(xcls)},
        "processes_covered": covered,
        "processes_partial": partial,
        "processes_uncovered": uncovered,
        "uncovered_reason": {p: "vLLM attention needs the engine forward context; covered by R031/R041 instead"
                             for p in list(uncovered) + list(partial)},
        "unclaimed_nodes_total": unclaimed_total,
        "evidence_boundary": ("a fixed-input FX DAG proves node args and users for the traced "
                              "shape; it is not eager runtime coverage and not module ownership"),
    }
    audit["coverage_target_met"] = (audit["class_coverage"]["classes_pass"]
                                    and unclaimed_total == 0
                                    and not uncovered and not partial)
    (a.out_dir / "fx_coverage_audit.json").write_text(json.dumps(audit, indent=1) + "\n")
    (a.out_dir / "fx_process_map.json").write_text(json.dumps(
        {"rule": {"anchors": ANCHORS,
                  "linear_named_by": "the weight shape it transposes",
                  "forward_attach": list(FORWARD_ATTACH),
                  "otherwise": "attach backward to the preceding anchor"},
         "hidden_size": hidden, "intermediate_size": inter,
         "fragments": per_frag}, indent=1) + "\n")
    lines = ["# 每个 process 的读写与主导轴（R042）", ""]
    for n in notes:
        lines += [f"## {n['process']}", "", n["caption"], "",
                  f"- 覆盖：{n['coverage']}",
                  f"- 观察到的形状：{n['observed_shapes']}",
                  f"- 归属证据：{n['boundness_evidence']}", ""]
    (a.out_dir / "fx_process_notes.md").write_text("\n".join(lines))
    print(json.dumps({"fragments": len(per_frag), "covered": len(covered),
                      "partial": sorted(partial), "uncovered": uncovered, "unclaimed_nodes": unclaimed_total,
                      "classes_pass": audit["class_coverage"]["classes_pass"],
                      "coverage_target_met": audit["coverage_target_met"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
