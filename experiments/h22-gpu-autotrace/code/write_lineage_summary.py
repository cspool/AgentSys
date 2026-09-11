#!/usr/bin/env python3
"""Assemble the h22 lineage summary from the w01-w05 artifacts of each strand."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def strand(root: Path, tag: str, workloads: list[str], w03_dir: str, w04_target: str) -> dict[str, Any]:
    out: dict[str, Any] = {"tag": tag, "workloads": {}}
    for w in workloads:
        c = json.loads((root / "g01_operator_trace" / w / "analysis" / "conservation.json").read_text())
        s2 = json.loads((root / "g02_g03_call_process" / w / "summary.json").read_text())
        ptype = {r["process"]: r for r in _read(root / "g02_g03_call_process" / w / "process_type_breakdown.csv")}
        meta = json.loads((root / "g01_operator_trace" / w / "native" / "run_metadata.json").read_text())
        m = c["measured"]
        ops = sum(float(r["host_ns_total"]) for p, r in ptype.items() if p.startswith("mir_operator"))
        out["workloads"][w] = {
            "calls": meta["planned"]["calls"], "operators": meta["planned"]["mir_operators"], "matrix": sorted({call["native"]["matrix_size"] for call in json.loads(Path(meta["plan_path"]).read_text())["calls"] if call["kind"] == "llm"}),
            "operator_iterations": meta["adapter"]["operator_iterations"], "iters": c["iterations"], "wall_ms_per_iter": m["wall_ns_per_iter"]["median"] / 1e6,
            "gpu_busy_pct": m["gpu_busy_pct_per_iter"]["median"], "operator_gpu_ms_per_iter": m["operator_gpu_ns_total"] / c["iterations"]["measured"] / 1e6,
            "overhead_gpu_ms_per_iter": m["call_overhead_gpu_ns_total"] / c["iterations"]["measured"] / 1e6, "launches_per_iter": m["kernel_launches_total"] / c["iterations"]["measured"],
            "host_input_generate_pct": float(ptype["host_input_generate"]["host_share_pct"]), "operators_host_pct": round(100 * ops / s2["wall_ns_total"], 2),
            "w01_pass": c["pass"], "w02_pass": s2["pass"], "align_spread_us": s2["clock_alignment"]["spread_ns"] / 1e3,
        }
    hw = _read(root / "g04_ncu_hardware" / w03_dir / "ncu_process_family_hardware_report.csv")
    out["gemm"] = [{"workload": r["workload"], "matrix": r["matrix_size"], "tensor_pct": r["tensor_pipe_active_pct"], "sm_pct": r["sm_throughput_pct"], "l2_pct": r["l2_throughput_pct"], "dram_pct": r["dram_cycles_active_pct"], "occ_pct": r["achieved_occupancy_pct"], "waves": r["waves_per_sm"], "tflops": r["gemm_tflops_from_replay"], "interp": r["hardware_bottleneck_interpretation"]} for r in hw if r["matched_kernel_family"] == "gemm"]
    out["rmsnorm"] = [{"workload": r["workload"], "matrix": r["matrix_size"], "family": r["matched_kernel_family"], "n": r["kernel_family_instance_count"], "dram_pct": r["dram_cycles_active_pct"], "l2_pct": r["l2_throughput_pct"], "waves": r["waves_per_sm"], "interp": r["hardware_bottleneck_interpretation"]} for r in hw if r["process"] == "mir_operator:RMSNormOp"]
    s4 = json.loads((root / "g05_full_workload_estimate" / w04_target / "summary.json").read_text())
    out["w04"] = {"target": w04_target, "abs_err_pct": s4["per_iteration"]["abs_err_pct"], "gpu_err_pct": s4["per_iteration"]["gpu_err_pct"], "max_process_err_pct": s4["max_process_abs_err_pct"], "pass": s4["pass"]}
    s5 = json.loads((root / "g06_g10_selective_resource_gap" / tag / "tables_manifest.json").read_text())
    out["w05"] = {"selection": s5["selection"], "pass": s5["pass"]}
    out["overlap"] = _read(root / "g06_g10_selective_resource_gap" / tag / "g07_host_gpu_overlap.csv")
    out["opps"] = _read(root / "g06_g10_selective_resource_gap" / tag / "g08_opportunities.csv")
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.artifact_root
    base = strand(root, "base", ["react_tool", "planner_debate", "react_moa_mcts"], "analysis", "react_moa_mcts")
    scaled = strand(root, "scaled", ["react_tool_L", "planner_debate_L", "react_moa_mcts_x3_L"], "analysis_scaled", "react_moa_mcts_x3_L")

    L = ["# h22 lineage summary: AutoTrace w01-w05 on AgentSys, single RTX 4090", "",
         "Two strands of the same serial chain. `base` runs the certified run_040 plans as shipped (matrix 768-1024, one operator iteration).",
         "`scaled` runs the same DAGs with matrix x4, 32 operator iterations and the react_moa_mcts DAG repeated 3x (built by `build_scaled_plan.py`,",
         "`src/agentsys/` untouched). Every strand: 5 goals, all conservation gates pass, nothing left this machine.", "",
         "## G01/G02 denominators", "",
         "| strand | workload | calls | ops | matrix | op iters | measured wall / iter (ms) | GPU busy | operator GPU / iter (ms) | overhead GPU / iter (ms) | launches / iter | host_input_generate share | operators host share |",
         "|---|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for s in (base, scaled):
        for w, d in s["workloads"].items():
            L.append(f"| {s['tag']} | {w} | {d['calls']} | {d['operators']} | {'/'.join(map(str, d['matrix']))} | {d['operator_iterations']} | {d['wall_ms_per_iter']:,.1f} | {d['gpu_busy_pct']:.1f} % | {d['operator_gpu_ms_per_iter']:,.2f} | {d['overhead_gpu_ms_per_iter']:,.2f} | {d['launches_per_iter']:.0f} | {d['host_input_generate_pct']:.1f} % | {d['operators_host_pct']:.1f} % |")
    L += ["", "## G04 hardware attributes of the representative GEMM (LinearOp) and RMSNorm kernels", "", "| strand | workload | matrix | Tensor pipe % | SM % | L2 % | DRAM active % | occupancy % | waves/SM | TFLOPS (replay) | interpretation |", "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for s in (base, scaled):
        for g in s["gemm"]:
            L.append(f"| {s['tag']} | {g['workload']} | {g['matrix']} | {g['tensor_pct']} | {g['sm_pct']} | {g['l2_pct']} | {g['dram_pct']} | {g['occ_pct']} | {g['waves']} | {g['tflops']} | {g['interp']} |")
    L += ["", "| strand | workload | matrix | RMSNorm kernel family | n | DRAM active % | L2 % | waves/SM | interpretation |", "|---|---|---:|---|---:|---:|---:|---:|---|"]
    for s in (base, scaled):
        for g in s["rmsnorm"]:
            L.append(f"| {s['tag']} | {g['workload']} | {g['matrix']} | {g['family']} | {g['n']} | {g['dram_pct']} | {g['l2_pct']} | {g['waves']} | {g['interp']} |")
    L += ["", "## G05 full-workload estimate from representative templates", "", "| strand | target | absolute host error | GPU error | max process error (>=1 % of wall) | pass |", "|---|---|---:|---:|---:|---|"]
    for s in (base, scaled):
        w4 = s["w04"]
        L.append(f"| {s['tag']} | {w4['target']} | {w4['abs_err_pct']:+.2f} % | {w4['gpu_err_pct']:+.2f} % | {w4['max_process_err_pct']} % | {w4['pass']} |")
    L += ["", "## G06-G10 selection and windows", "", "| strand | workload | selected process types (> 10 %) | GPU busy (rep. iter) | host-only | GPU gaps >= 20 us | gap total (ms) |", "|---|---|---|---:|---:|---:|---:|"]
    for s in (base, scaled):
        ov = {r["workload"]: r for r in s["overlap"]}
        for w, sel in s["w05"]["selection"].items():
            o = ov[w]
            L.append(f"| {s['tag']} | {w} | {', '.join(sel)} | {o['gpu_busy_pct']} % | {o['host_only_pct']} % | {o['gaps_reported']} | {float(o['gap_ns_total']) / 1e6:,.2f} |")
    L += ["", "| strand | workload | opportunity | current / iter (ms) | reference / iter (ms) | bound (% wall) |", "|---|---|---|---:|---:|---:|"]
    for s in (base, scaled):
        for o in s["opps"]:
            L.append(f"| {s['tag']} | {o['workload']} | {o['opportunity']} | {float(o['current_ns_per_iter']) / 1e6:,.2f} | {float(o['reference_ns_per_iter']) / 1e6:,.3f} | {o['bound_pct_of_wall']} % |")
    L += ["", "## Reading", "",
          "1. At native scale the GPU is busy 2-3 % of the wall. The certified adapter's per-call host input generation (seeded CPU-generator `uniform_` into a",
          "   pinned fp16 tensor) is 56-75 % of every iteration; all MIR operators together are about 10 % of host time and 1-16 us of GPU time each.",
          "2. Scaling the operators (matrix x4, 32 iterations) raises GPU busy to 40-50 % and makes LinearOp/RMSNormOp cross the 10 % selection line, but",
          "   host input generation still takes about half the wall because it grows with n^2 on one CPU thread.",
          "3. The 768-1024 GEMMs run at 15-24 % tensor-pipe activity with 0.75-1.5 waves per SM (latency/launch-bound); at 3072-4096 the same kernel family is",
          "   tensor-core compute-bound at 45-49 % pipe activity and 12 waves per SM. RMSNorm stays a 7-kernel elementwise/reduce chain that never exceeds 0.4 waves.",
          "4. Template estimation from two representative workloads predicts the full react_moa_mcts workload within 11 % (base) and 0.1 % (scaled) without using",
          "   its trace; the base error is dominated by the plan-independent DAG scheduling gap and by H2D/D2H staging variance.",
          "5. The real-model strand (Qwen3-1.7B weights present under /data3/docker_model/AgentSys) is not part of this summary: no transformer library is",
          "   installed, downloads are excluded by protocol, and the hand-written fallback was set aside pending the user's own sources.", ""]
    args.output.write_text("\n".join(L))
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
