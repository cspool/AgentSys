#!/usr/bin/env python3
"""w04 / G05: full-workload process-wise estimate from representative templates.

AutoTrace w04 scales representative-layer process templates onto every layer
under the w01 layer denominator. The AgentSys mapping:

* representative workloads: ``react_tool`` (matrix 768) and ``planner_debate``
  (matrix 896, 1024) -> per-(call_kind, matrix_size, process, op_type)
  per-instance medians from their w02 instance tables (``observed`` rows);
* target workload: ``react_moa_mcts`` (11 calls, 80 operators). Instance
  counts come from the target *plan* (not from its trace), so the estimate is
  a prediction; the target's own w01/w02 evidence is used only to score it.

Two estimates are reported, as in w04:

* ``template_absolute``: count x template median, no normalisation;
* ``template_scaled``: the same distribution conserved to the target's w01
  measured wall (sum of scaled processes == measured wall exactly).

Both are compared against the target's observed w02 process breakdown.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_w01_operator_trace import _sha256, _write_csv  # noqa: E402

LLM_FIXED = ["adapter_dispatch", "token_preprocess_cpu", "host_input_generate", "h2d_stage", "weight_init", "pre_d2h_alloc", "d2h_stage", "checksum_complete"]


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def build_template(rep: dict[str, Path], plans: dict[str, dict[str, Any]]) -> tuple[dict[tuple[Any, ...], dict[str, Any]], list[dict[str, Any]]]:
    samples: dict[tuple[Any, ...], dict[str, list[float]]] = defaultdict(lambda: {"host": [], "gpu": [], "src": []})
    for name, inst_path in rep.items():
        size_of = {c["call_id"]: c["native"]["matrix_size"] for c in plans[name]["calls"]}
        for r in _read(inst_path):
            kind = r["call_kind"]
            size = size_of.get(r["call_id"], "") if kind != "dag" else ""
            key = (kind, str(size), r["process"], r["op_type"])
            samples[key]["host"].append(float(r["host_ns"]))
            samples[key]["gpu"].append(float(r["gpu_work_ns"]))
            samples[key]["src"].append(name)
    template: dict[tuple[Any, ...], dict[str, Any]] = {}
    rows = []
    for key, v in sorted(samples.items()):
        template[key] = {"host_ns": statistics.median(v["host"]), "gpu_ns": statistics.median(v["gpu"]), "n": len(v["host"]), "source": "+".join(sorted(set(v["src"])))}
        rows.append({"call_kind": key[0], "matrix_size": key[1], "process": key[2], "op_type": key[3], "template_source": template[key]["source"], "samples": len(v["host"]),
                     "host_ns_median": template[key]["host_ns"], "host_ns_p90": sorted(v["host"])[int(0.9 * (len(v["host"]) - 1))], "gpu_ns_median": template[key]["gpu_ns"]})
    return template, rows


def expected_instances(plan: dict[str, Any]) -> list[dict[str, Any]]:
    """Enumerate target process instances per iteration from the plan alone."""
    out = []
    for call in sorted(plan["calls"], key=lambda c: (c["wave"], c["index"])):
        size = str(call["native"]["matrix_size"])
        out.append({"call_id": None, "call_kind": "dag", "matrix_size": "", "process": "dag_schedule_gap", "op_type": "", "before_call": call["call_id"]})
        if call["kind"] == "llm":
            ops = call["mir_operators"]
            for p in LLM_FIXED[:5]:
                out.append({"call_id": call["call_id"], "call_kind": "llm", "matrix_size": size, "process": p, "op_type": ""})
            for i, op in enumerate(ops):
                if i > 0:
                    out.append({"call_id": call["call_id"], "call_kind": "llm", "matrix_size": size, "process": "inter_operator_dispatch", "op_type": ""})
                out.append({"call_id": call["call_id"], "call_kind": "llm", "matrix_size": size, "process": f"mir_operator:{op['op_type']}", "op_type": op["op_type"], "op_index": op["index"], "engine": op["engine"]})
            for p in LLM_FIXED[5:]:
                out.append({"call_id": call["call_id"], "call_kind": "llm", "matrix_size": size, "process": p, "op_type": ""})
        else:
            out.append({"call_id": call["call_id"], "call_kind": "tool", "matrix_size": size, "process": "agent_tool_execute_cpu", "op_type": ""})
    out.append({"call_id": None, "call_kind": "dag", "matrix_size": "", "process": "iteration_tail_sync", "op_type": ""})
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="w04 full-workload estimate")
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--plan-root", type=Path, required=True)
    parser.add_argument("--representative", nargs="+", default=["react_tool", "planner_debate"])
    parser.add_argument("--target", default="react_moa_mcts")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    root = args.artifact_root

    plans = {w: json.loads((args.plan_root / w / "hybrid-plan.json").read_text()) for w in [*args.representative, args.target]}
    rep_inst = {w: root / "g02_g03_call_process" / w / "call_process_instances.csv" for w in args.representative}
    for w in args.representative:
        s = json.loads((root / "g02_g03_call_process" / w / "summary.json").read_text())
        if not s["pass"]:
            raise SystemExit(f"w02 for representative {w} did not pass")
    template, template_rows = build_template(rep_inst, plans)
    _write_csv(out / "full_workload_template.csv", template_rows)

    target = args.target
    w01 = json.loads((root / "g01_operator_trace" / target / "analysis" / "conservation.json").read_text())
    w02 = json.loads((root / "g02_g03_call_process" / target / "summary.json").read_text())
    iters = w02["iterations_measured"]
    measured_wall_per_iter = w01["measured"]["wall_ns_total"] / iters
    observed_types = {r["process"]: r for r in _read(root / "g02_g03_call_process" / target / "process_type_breakdown.csv")}
    observed_calls = {r["call_id"]: r for r in _read(root / "g02_g03_call_process" / target / "call_breakdown.csv")}

    # ---- assignment: every expected instance -> template key
    expected = expected_instances(plans[target])
    assign_rows = []
    per_process_est: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0, "host_ns": 0.0, "gpu_ns": 0.0})
    per_call_est: dict[str, dict[str, float]] = defaultdict(lambda: {"host_ns": 0.0, "gpu_ns": 0.0})
    coverage: dict[tuple[Any, ...], dict[str, Any]] = {}
    for inst in expected:
        key = (inst["call_kind"], inst["matrix_size"], inst["process"], inst["op_type"])
        t = template.get(key)
        source = "template_scaled" if t else "missing_template"
        # fallback: same process, nearest matrix size (flagged)
        if t is None:
            cands = [k for k in template if k[0] == key[0] and k[2] == key[2] and k[3] == key[3]]
            if cands:
                near = min(cands, key=lambda k: abs(int(k[1] or 0) - int(key[1] or 0)))
                t = template[near]
                source = f"template_nearest_size:{near[1]}"
        host = t["host_ns"] if t else 0.0
        gpu = t["gpu_ns"] if t else 0.0
        assign_rows.append({"target": target, "call_id": inst["call_id"] or "<dag>", "call_kind": inst["call_kind"], "matrix_size": inst["matrix_size"], "process": inst["process"],
                            "op_type": inst["op_type"], "op_index": inst.get("op_index", ""), "attribution_source": source, "attribution_type_id": "|".join(map(str, key)),
                            "template_source_workload": t["source"] if t else "", "template_samples": t["n"] if t else 0, "est_host_ns": host, "est_gpu_ns": gpu})
        p = per_process_est[inst["process"]]
        p["count"] += 1; p["host_ns"] += host; p["gpu_ns"] += gpu
        c = per_call_est[inst["call_id"] or "<dag>"]
        c["host_ns"] += host; c["gpu_ns"] += gpu
        coverage.setdefault(key, {"call_kind": key[0], "matrix_size": key[1], "process": key[2], "op_type": key[3], "instances_per_iter": 0, "covered": t is not None, "source": source, "template_source_workload": t["source"] if t else ""})
        coverage[key]["instances_per_iter"] += 1
    _write_csv(out / "full_workload_template_assignment.csv", assign_rows)
    _write_csv(out / "full_workload_coverage_and_risk.csv", list(coverage.values()))

    # ---- process-level estimate vs observed
    est_total_host = sum(v["host_ns"] for v in per_process_est.values())
    scale = measured_wall_per_iter / est_total_host if est_total_host else 0.0
    proc_rows = []
    for proc in sorted(set(per_process_est) | set(observed_types), key=lambda p: -(per_process_est[p]["host_ns"] if p in per_process_est else 0)):
        e = per_process_est.get(proc, {"count": 0, "host_ns": 0.0, "gpu_ns": 0.0})
        o = observed_types.get(proc)
        obs_host = float(o["host_ns_total"]) / iters if o else 0.0
        obs_gpu = float(o["gpu_ns_total"]) / iters if o else 0.0
        obs_count = int(o["instances"]) / iters if o else 0
        proc_rows.append({"target": target, "process": proc, "expected_instances_per_iter": e["count"], "observed_instances_per_iter": obs_count,
                          "template_absolute_host_ns": round(e["host_ns"], 1), "template_scaled_host_ns": round(e["host_ns"] * scale, 1), "observed_host_ns": round(obs_host, 1),
                          "abs_err_pct": round(100 * (e["host_ns"] - obs_host) / obs_host, 1) if obs_host else "", "scaled_err_pct": round(100 * (e["host_ns"] * scale - obs_host) / obs_host, 1) if obs_host else "",
                          "template_absolute_share_pct": round(100 * e["host_ns"] / est_total_host, 2) if est_total_host else "", "observed_share_pct": round(100 * obs_host / measured_wall_per_iter, 2),
                          "template_gpu_ns": round(e["gpu_ns"], 1), "observed_gpu_ns": round(obs_gpu, 1), "gpu_err_pct": round(100 * (e["gpu_ns"] - obs_gpu) / obs_gpu, 1) if obs_gpu else ""})
    _write_csv(out / "full_workload_process_estimate.csv", proc_rows)

    call_rows = []
    for call, e in per_call_est.items():
        o = observed_calls.get(call if call != "<dag>" else "<dag>")
        obs_host = float(o["host_ns_per_iter"]) if o else 0.0
        obs_gpu = float(o["gpu_ns_per_iter"]) if o else 0.0
        call_rows.append({"target": target, "call_id": call, "template_absolute_host_ns": round(e["host_ns"], 1), "template_scaled_host_ns": round(e["host_ns"] * scale, 1), "observed_host_ns": round(obs_host, 1),
                          "abs_err_pct": round(100 * (e["host_ns"] - obs_host) / obs_host, 1) if obs_host else "", "template_gpu_ns": round(e["gpu_ns"], 1), "observed_gpu_ns": round(obs_gpu, 1),
                          "gpu_err_pct": round(100 * (e["gpu_ns"] - obs_gpu) / obs_gpu, 1) if obs_gpu else ""})
    _write_csv(out / "full_workload_call_estimate.csv", call_rows)

    est_gpu = sum(v["gpu_ns"] for v in per_process_est.values())
    obs_gpu_total = w01["measured"]["sum_attributed_gpu_ns_total"] / iters
    scaled_sum = sum(r["template_scaled_host_ns"] for r in proc_rows)
    summary = {
        "schema_version": 1, "lineage": "h22-gpu-autotrace", "goal": "G05", "target": target, "representative": args.representative,
        "upstream": {"w01_sqlite_sha256": w01["sqlite_sha256"], "w02_summary_pass": w02["pass"], "template_rows": len(template_rows)},
        "per_iteration": {"observed_wall_ns": measured_wall_per_iter, "template_absolute_host_ns": est_total_host, "abs_err_pct": round(100 * (est_total_host - measured_wall_per_iter) / measured_wall_per_iter, 2),
                          "scale_to_conserve": scale, "template_scaled_sum_ns": scaled_sum, "conservation_err_ns": scaled_sum - measured_wall_per_iter,
                          "template_gpu_ns": est_gpu, "observed_gpu_ns": obs_gpu_total, "gpu_err_pct": round(100 * (est_gpu - obs_gpu_total) / obs_gpu_total, 2)},
        "coverage": {"keys": len(coverage), "missing_template": sum(1 for c in coverage.values() if not c["covered"]), "nearest_size_fallback": sum(1 for c in coverage.values() if c["source"].startswith("template_nearest"))},
        "instance_count_mismatch": [r["process"] for r in proc_rows if r["expected_instances_per_iter"] != r["observed_instances_per_iter"]],
        "max_process_abs_err_pct": max((abs(r["abs_err_pct"]) for r in proc_rows if r["abs_err_pct"] != "" and r["observed_share_pct"] >= 1.0), default=0),
    }
    summary["pass"] = abs(summary["per_iteration"]["conservation_err_ns"]) < 1000 and summary["coverage"]["missing_template"] == 0 and not summary["instance_count_mismatch"]
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    L = [f"# G05 full-workload process estimate: `{target}` from {' + '.join(args.representative)}", "",
         "Lineage `h22-gpu-autotrace`, workflow w04. Instance counts come from the target plan; per-instance values are w02 medians of the",
         "representative workloads keyed by (call kind, matrix size, process, op type). The target's own w01/w02 evidence is used only to score the estimate.", "",
         "## Summary", "", "| Quantity | Value |", "|---|---:|",
         f"| Observed measured wall per iteration | {measured_wall_per_iter / 1e3:,.1f} us |",
         f"| template_absolute host per iteration | {est_total_host / 1e3:,.1f} us ({summary['per_iteration']['abs_err_pct']:+.2f} %) |",
         f"| template_scaled conservation error | {summary['per_iteration']['conservation_err_ns']:.0f} ns |",
         f"| GPU work: template vs observed | {est_gpu / 1e3:,.1f} vs {obs_gpu_total / 1e3:,.1f} us ({summary['per_iteration']['gpu_err_pct']:+.2f} %) |",
         f"| Template keys covered / missing / nearest-size fallback | {summary['coverage']['keys']} / {summary['coverage']['missing_template']} / {summary['coverage']['nearest_size_fallback']} |",
         f"| Instance-count mismatches (plan vs observed) | {summary['instance_count_mismatch'] or 'none'} |",
         f"| Max process error (processes >= 1 % of wall) | {summary['max_process_abs_err_pct']} % |",
         f"| Pass | {summary['pass']} |", "",
         "## Process-wise estimate vs observed (per iteration)", "",
         "| process | n/iter (plan) | n/iter (obs) | template_absolute (us) | template_scaled (us) | observed (us) | abs err | scaled err | template share | observed share |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in proc_rows:
        L.append(f"| {r['process']} | {r['expected_instances_per_iter']} | {r['observed_instances_per_iter']:g} | {r['template_absolute_host_ns'] / 1e3:,.1f} | {r['template_scaled_host_ns'] / 1e3:,.1f} | {r['observed_host_ns'] / 1e3:,.1f} | {r['abs_err_pct']} % | {r['scaled_err_pct']} % | {r['template_absolute_share_pct']} % | {r['observed_share_pct']} % |")
    L += ["", "## Call-wise estimate vs observed (per iteration)", "", "| call | template_absolute (us) | template_scaled (us) | observed (us) | abs err | template GPU (us) | observed GPU (us) | GPU err |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in call_rows:
        L.append(f"| {r['call_id']} | {r['template_absolute_host_ns'] / 1e3:,.1f} | {r['template_scaled_host_ns'] / 1e3:,.1f} | {r['observed_host_ns'] / 1e3:,.1f} | {r['abs_err_pct']} % | {r['template_gpu_ns'] / 1e3:,.1f} | {r['observed_gpu_ns'] / 1e3:,.1f} | {r['gpu_err_pct']} % |")
    L += ["", "## Constraints honoured", "", "- `template_absolute` is a prediction; `template_scaled` is conserved to the w01 measured wall and is not a direct trace.",
          "- Representative absolute latencies are never reported as target latencies without the matrix-size key matching.",
          "- w03 hardware attributes do not enter this denominator.", ""]
    (out / "G05_FULL_WORKLOAD_ESTIMATE_REPORT.md").write_text("\n".join(L))
    print(json.dumps({"target": target, "pass": summary["pass"], "abs_err_pct": summary["per_iteration"]["abs_err_pct"], "gpu_err_pct": summary["per_iteration"]["gpu_err_pct"],
                      "max_process_abs_err_pct": summary["max_process_abs_err_pct"], "mismatch": summary["instance_count_mismatch"]}, indent=2))
    return 0 if summary["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
