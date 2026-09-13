#!/usr/bin/env python3
"""w03 / G04: Nsight Compute hardware attributes projected onto w02 rows.

Row unit is the w02 (call, process, kernel family) launch-owned target; NCU
kernel instances that match the same NVTX operator range are grouped by
family under it. NCU replay durations are reported as `ncu_replay_us` for
context only and never replace the w01/w02 timing denominator.

Non-GPU processes (host RNG, CPU matmul, DAG gaps) have no counters and are
listed with `ncu_status = not_collected_cpu_process` rather than zero-filled.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_w01_operator_trace import _kernel_family, _sha256, _write_csv  # noqa: E402

RTX4090_PEAK_DRAM_BYTES_S = 1_008_096_000_000  # from nsys TARGET_INFO_GPU.memoryBandwidth
# GEMM throughput is reported as TFLOPS from the NCU replay only. The cuBLAS kernel here is
# `cutlass_80_tensorop_f16_s16816gemm_f16_*` (FP16 accumulate, 330 TFLOPS dense peak at boost),
# and NCU locks clocks to base, so no single "% of peak" is well defined; use tensor_pipe_active_pct.

METRICS = {
    "ncu_replay_us": "gpu__time_duration.sum",
    "sm_throughput_pct": "sm__throughput.avg.pct_of_peak_sustained_elapsed",
    "compute_memory_throughput_pct": "gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed",
    "tensor_pipe_active_pct": "sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active",
    "dram_cycles_active_pct": "dram__cycles_active.avg.pct_of_peak_sustained_elapsed",
    "dram_bytes_per_s": "dram__bytes.sum.per_second",
    "dram_read_bytes": "dram__bytes_read.sum",
    "dram_write_bytes": "dram__bytes_write.sum",
    "l2_throughput_pct": "lts__throughput.avg.pct_of_peak_sustained_elapsed",
    "l2_hit_rate_pct": "lts__t_sector_hit_rate.pct",
    "l1_throughput_pct": "l1tex__throughput.avg.pct_of_peak_sustained_active",
    "achieved_occupancy_pct": "sm__warps_active.avg.pct_of_peak_sustained_active",
    "theoretical_occupancy_pct": "sm__maximum_warps_per_active_cycle_pct",
    "waves_per_sm": "launch__waves_per_multiprocessor",
    "registers_per_thread": "launch__registers_per_thread",
    "inst_executed": "smsp__inst_executed.sum",
    "tensor_inst": "sm__inst_executed_pipe_tensor.sum",
}
UNIT_SCALE = {"us": 1.0, "ms": 1e3, "ns": 1e-3, "byte": 1.0, "Kbyte": 1e3, "Mbyte": 1e6, "Gbyte": 1e9, "byte/second": 1.0, "Kbyte/second": 1e3, "Mbyte/second": 1e6, "Gbyte/second": 1e9, "Tbyte/second": 1e12}
NVTX_RE = re.compile(r"agentsys\.mllm::([^:]+)::(\d+)::(\w+)")


def read_ncu_raw(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="") as handle:
        rows = list(csv.reader(handle))
    hdr, units, data = rows[0], rows[1], rows[2:]
    idx = {h: i for i, h in enumerate(hdr)}
    nvtx_col = next(h for h in hdr if h.startswith("thread Domain:Push/Pop_Range"))
    stall_cols = [h for h in hdr if "issue_stalled" in h and h.endswith("per_issue_active.ratio")]
    out = []
    for d in data:
        rec: dict[str, Any] = {"ncu_id": int(d[idx["ID"]]), "kernel_name": d[idx["Kernel Name"]], "block": d[idx["Block Size"]], "grid": d[idx["Grid Size"]]}
        m = NVTX_RE.search(d[idx[nvtx_col]])
        rec["call_id"], rec["op_index"], rec["op_type"] = (m.group(1), int(m.group(2)), m.group(3)) if m else (None, None, None)
        for key, col in METRICS.items():
            if col in idx and d[idx[col]] not in ("", "n/a"):
                val = float(d[idx[col]].replace(",", ""))
                unit = units[idx[col]]
                if key in ("ncu_replay_us", "dram_read_bytes", "dram_write_bytes", "dram_bytes_per_s"):
                    val *= UNIT_SCALE.get(unit, 1.0)
                rec[key] = val
            else:
                rec[key] = None
        stalls = {}
        for c in stall_cols:
            try:
                stalls[c.split("issue_stalled_")[1].split("_per_issue")[0]] = float(d[idx[c]])
            except (ValueError, IndexError):
                pass
        top = sorted(stalls.items(), key=lambda kv: -kv[1])[:3]
        rec["dominant_stalls"] = "; ".join(f"{k}={v:.2f}" for k, v in top)
        rec["family"] = _kernel_family(rec["kernel_name"])
        out.append(rec)
    return out


def interpret(r: dict[str, Any]) -> str:
    sm = r.get("sm_throughput_pct") or 0
    dram = r.get("dram_cycles_active_pct") or 0
    l2 = r.get("l2_throughput_pct") or 0
    tensor = r.get("tensor_pipe_active_pct") or 0
    occ = r.get("achieved_occupancy_pct") or 0
    waves = r.get("waves_per_sm")
    if waves is not None and waves < 1.0 and max(sm, dram, l2) < 30:
        return f"latency/launch-bound: {waves:.2f} waves per SM, no unit above 30 % of peak"
    if tensor >= 40:
        return "tensor-core compute-bound"
    if dram >= 60:
        return "DRAM-bandwidth-bound"
    if l2 >= 60 and dram < 60:
        return "L2-bandwidth-bound (working set in L2)"
    if sm >= 60:
        return "SM-issue-bound"
    return f"underutilised: SM {sm:.0f} %, DRAM {dram:.0f} %, L2 {l2:.0f} %, occ {occ:.0f} %"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="w03 ncu hardware attributes over w02 rows")
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--workloads", nargs="+", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--matrix-of", type=Path, help="plan root to look up matrix sizes", required=True)
    args = parser.parse_args(argv)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict[str, Any]] = []
    family_rows: list[dict[str, Any]] = []
    provenance = {}
    for w in args.workloads:
        raw = args.artifact_root / "g04_ncu_hardware" / w / f"{w}_ncu_raw.csv"
        rep = args.artifact_root / "g04_ncu_hardware" / w / f"{w}_measured_iter0.ncu-rep"
        plan = json.loads((args.matrix_of / w / "hybrid-plan.json").read_text())
        size_of = {c["call_id"]: c["native"]["matrix_size"] for c in plan["calls"]}
        w02 = json.loads((args.artifact_root / "g02_g03_call_process" / w / "summary.json").read_text())
        if not w02["pass"]:
            raise SystemExit(f"w02 for {w} did not pass; w03 admission refused")
        launch = list(csv.DictReader((args.artifact_root / "g02_g03_call_process" / w / "kernel_launch_order_representative_iteration.csv").open()))
        kernels_w02 = [r for r in launch if r["kind"] == "kernel"]
        recs = read_ncu_raw(raw)
        provenance[w] = {"ncu_rep_sha256": _sha256(rep), "ncu_raw_sha256": _sha256(raw), "ncu_kernels": len(recs), "w02_kernels_in_representative_iteration": len(kernels_w02)}
        # Join each NCU kernel to its w02 launch row by NVTX operator range (call, op_index) and
        # ordinal inside that range; kernels outside any operator range fall back to position.
        by_range: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
        for k in kernels_w02:
            by_range[(k["call_id"], str(k["op_index"]))].append(k)
        seen: dict[tuple[str, str], int] = defaultdict(int)
        matched = 0
        for i, r in enumerate(recs):
            w02row: dict[str, Any] = {}
            if r["op_index"] is not None:
                key = (r["call_id"], str(r["op_index"]))
                rows_in_range = by_range.get(key, [])
                j = seen[key]
                if j < len(rows_in_range) and rows_in_range[j]["family"] == r["family"]:
                    w02row = rows_in_range[j]
                    matched += 1
                seen[key] += 1
            elif len(recs) == len(kernels_w02) and i < len(kernels_w02) and kernels_w02[i]["family"] == r["family"]:
                w02row = kernels_w02[i]
                matched += 1
            call = r["call_id"] or w02row.get("call_id")
            proc = w02row.get("process", f"mir_operator:{r['op_type']}" if r["op_type"] else "")
            ratio = None
            if r.get("dram_bytes_per_s"):
                ratio = 100 * r["dram_bytes_per_s"] / RTX4090_PEAK_DRAM_BYTES_S
            tflops = None
            if r["op_type"] == "LinearOp" and r.get("ncu_replay_us"):
                n = size_of.get(call, 0)
                tflops = 2 * n ** 3 / (r["ncu_replay_us"] * 1e-6) / 1e12
            row = {"workload": w, "launch_order": w02row.get("launch_order", i + 1), "call_id": call, "matrix_size": size_of.get(call, ""), "process": proc,
                   "op_index": r["op_index"] if r["op_index"] is not None else "", "op_type": r["op_type"] or "", "family": r["family"], "kernel_name": r["kernel_name"][:100],
                   "grid": r["grid"], "block": r["block"], "ncu_status": "profiled", "ncu_replay_us": r["ncu_replay_us"], "nsys_gpu_us": round(float(w02row["gpu_ns"]) / 1e3, 2) if w02row else "",
                   "sm_throughput_pct": r["sm_throughput_pct"], "tensor_pipe_active_pct": r["tensor_pipe_active_pct"], "dram_cycles_active_pct": r["dram_cycles_active_pct"],
                   "dram_bw_pct_of_peak": round(ratio, 2) if ratio is not None else "", "dram_read_bytes": r["dram_read_bytes"], "dram_write_bytes": r["dram_write_bytes"],
                   "l2_throughput_pct": r["l2_throughput_pct"], "l2_hit_rate_pct": r["l2_hit_rate_pct"], "l1_throughput_pct": r["l1_throughput_pct"],
                   "achieved_occupancy_pct": r["achieved_occupancy_pct"], "theoretical_occupancy_pct": r["theoretical_occupancy_pct"], "waves_per_sm": r["waves_per_sm"],
                   "registers_per_thread": r["registers_per_thread"], "gemm_tflops_from_replay": round(tflops, 1) if tflops else "",
                   "dominant_stalls": r["dominant_stalls"], "hardware_bottleneck_interpretation": interpret(r)}
            all_rows.append(row)
        in_range = sum(1 for r in recs if r["op_index"] is not None)
        provenance[w]["ncu_kernels_joined_to_w02"] = matched
        provenance[w]["ncu_kernels_in_operator_ranges"] = in_range
        provenance[w]["ncu_kernels_outside_operator_ranges"] = len(recs) - in_range
        # Kernels outside any operator NVTX range (e.g. rotary-embedding
        # precompute between stages) are reported but carry no w02 row; the
        # order contract applies to the in-range kernels.
        provenance[w]["order_match"] = matched >= in_range
    _write_csv(out / "ncu_kernel_hardware_attributes.csv", all_rows)

    # ---- family-level projection over w02 rows: (workload, matrix, process, family)
    grp: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for r in all_rows:
        grp[(r["workload"], r["matrix_size"], r["process"], r["family"])].append(r)

    def med(rows: list[dict[str, Any]], k: str) -> Any:
        vals = [float(r[k]) for r in rows if r[k] not in ("", None)]
        return round(statistics.median(vals), 2) if vals else ""

    for key, rows in sorted(grp.items(), key=lambda kv: (kv[0][0], str(kv[0][1]), min(int(r["launch_order"]) for r in kv[1]))):
        family_rows.append({"workload": key[0], "matrix_size": key[1], "process": key[2], "matched_kernel_family": key[3], "kernel_family_instance_count": len(rows),
                            "ncu_status": "profiled", "ncu_profiled_kernel_names": rows[0]["kernel_name"][:60], "first_launch_order": min(int(r["launch_order"]) for r in rows),
                            "sm_throughput_pct": med(rows, "sm_throughput_pct"), "tensor_pipe_active_pct": med(rows, "tensor_pipe_active_pct"), "dram_cycles_active_pct": med(rows, "dram_cycles_active_pct"),
                            "dram_bw_pct_of_peak": med(rows, "dram_bw_pct_of_peak"), "l2_throughput_pct": med(rows, "l2_throughput_pct"), "l2_hit_rate_pct": med(rows, "l2_hit_rate_pct"),
                            "achieved_occupancy_pct": med(rows, "achieved_occupancy_pct"), "waves_per_sm": med(rows, "waves_per_sm"), "gemm_tflops_from_replay": med(rows, "gemm_tflops_from_replay"),
                            "dominant_stalls": rows[0]["dominant_stalls"], "hardware_bottleneck_interpretation": rows[0]["hardware_bottleneck_interpretation"]})
    # CPU-only processes: listed explicitly as not collected
    for w in args.workloads:
        for r in csv.DictReader((args.artifact_root / "g02_g03_call_process" / w / "process_type_breakdown.csv").open()):
            if r["process"] in ("h2d_stage", "d2h_stage"):
                family_rows.append({"workload": w, "matrix_size": "", "process": r["process"], "matched_kernel_family": "memcpy", "kernel_family_instance_count": int(r["instances"]), "ncu_status": "not_collected_memcpy",
                                    "ncu_profiled_kernel_names": "", "first_launch_order": "", "sm_throughput_pct": "", "tensor_pipe_active_pct": "", "dram_cycles_active_pct": "", "dram_bw_pct_of_peak": "",
                                    "l2_throughput_pct": "", "l2_hit_rate_pct": "", "achieved_occupancy_pct": "", "waves_per_sm": "", "gemm_tflops_from_replay": "", "dominant_stalls": "", "hardware_bottleneck_interpretation": "PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms"})
            elif int(r["kernel_launches"]) == 0:
                family_rows.append({"workload": w, "matrix_size": "", "process": r["process"], "matched_kernel_family": "", "kernel_family_instance_count": 0, "ncu_status": "not_collected_cpu_process",
                                    "ncu_profiled_kernel_names": "", "first_launch_order": "", "sm_throughput_pct": "", "tensor_pipe_active_pct": "", "dram_cycles_active_pct": "", "dram_bw_pct_of_peak": "",
                                    "l2_throughput_pct": "", "l2_hit_rate_pct": "", "achieved_occupancy_pct": "", "waves_per_sm": "", "gemm_tflops_from_replay": "", "dominant_stalls": "", "hardware_bottleneck_interpretation": "host-side process; no GPU counters"})
    _write_csv(out / "ncu_process_family_hardware_report.csv", family_rows)

    summary = {"schema_version": 1, "lineage": "h22-gpu-autotrace", "goal": "G04", "workloads": args.workloads, "provenance": provenance, "kernels_profiled": len(all_rows),
               "peak_assumptions": {"dram_bytes_per_s": RTX4090_PEAK_DRAM_BYTES_S, "gemm_note": "TFLOPS from NCU replay at locked base clock; utilisation reference is tensor_pipe_active_pct"},
               "pass": all(p["order_match"] for p in provenance.values())}
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    L = ["# G04 kernel-family hardware attributes by representative operator", "", "Lineage `h22-gpu-autotrace`, workflow w03. Rows are w02 launch-owned targets grouped by matched kernel family;",
         "NCU metrics come from a separate single-iteration replay run and `ncu_replay_us` is not latency. Peak DRAM 1008 GB/s is the RTX 4090 reference;",
         "GEMM TFLOPS is computed from replay time at NCU's locked base clock and is context only, the utilisation reference is Tensor % (pipe active).", "",
         "| workload | matrix | process | family | n | SM % | Tensor % | DRAM active % | DRAM BW % peak | L2 % | L2 hit % | occupancy % | waves/SM | GEMM TFLOPS (replay) | dominant stalls | interpretation |",
         "|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|"]
    for r in family_rows:
        L.append(f"| {r['workload']} | {r['matrix_size']} | {r['process']} | {r['matched_kernel_family']} | {r['kernel_family_instance_count']} | {r['sm_throughput_pct']} | {r['tensor_pipe_active_pct']} | {r['dram_cycles_active_pct']} | {r['dram_bw_pct_of_peak']} | {r['l2_throughput_pct']} | {r['l2_hit_rate_pct']} | {r['achieved_occupancy_pct']} | {r['waves_per_sm']} | {r['gemm_tflops_from_replay']} | {r['dominant_stalls']} | {r['hardware_bottleneck_interpretation']} |")
    L += ["", "## Provenance", "", "```json", json.dumps(provenance, indent=2), "```", ""]
    (out / "G04_NCU_HARDWARE_REPORT.md").write_text("\n".join(L))
    print(json.dumps({"pass": summary["pass"], "kernels": len(all_rows), "provenance": provenance}, indent=2))
    return 0 if summary["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
