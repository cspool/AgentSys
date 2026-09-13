#!/usr/bin/env python3
"""Compare FCFS vs PLAS across arrival rates with the Agentix paper's metrics.

Reads ``artifacts/agentix_8b/r<rate>/<policy>/{summary,programs}_<policy>.json(l)``
and writes a comparison table plus a Markdown report. The paper's headline is
"throughput at the same latency", so the report also reports, for every latency
pair, which policy delivers more programs/s.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path
from typing import Any


def _read_programs(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _pct(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    return s[min(len(s) - 1, int(q * (len(s) - 1)))]


def summarise(root: Path, rate: int, policy: str) -> dict[str, Any] | None:
    return summarise_dir(root / f"r{rate}" / policy, rate, policy)


def summarise_dir(d: Path, rate: int, policy: str) -> dict[str, Any] | None:
    summary_path, programs_path = d / f"summary_{policy}.json", d / f"programs_{policy}.jsonl"
    if not summary_path.exists() or not programs_path.exists():
        return None
    summary = json.loads(summary_path.read_text())
    programs = _read_programs(programs_path)
    by_class: dict[str, list[float]] = {}
    for p in programs:
        by_class.setdefault(p["class"], []).append(p["program_token_latency_ms"])
    return {
        "arrival_rate": rate, "policy": policy,
        "programs": summary["observed"]["programs"], "llm_calls": summary["observed"]["llm_calls"],
        "wall_s": summary["observed"]["wall_s"],
        "throughput_programs_per_s": summary["observed"]["throughput_programs_per_s"],
        "throughput_tokens_per_s": summary["observed"]["throughput_tokens_per_s"],
        "ptl_mean_ms": summary["observed"]["program_token_latency_ms"]["mean"],
        "ptl_p50_ms": _pct([p["program_token_latency_ms"] for p in programs], 0.5),
        "ptl_p90_ms": summary["observed"]["program_token_latency_ms"]["p90"],
        "ptl_p99_ms": summary["observed"]["program_token_latency_ms"]["p99"],
        "response_mean_ms": summary["observed"]["program_response_time_ms"]["mean"],
        "response_p90_ms": summary["observed"]["program_response_time_ms"]["p90"],
        "response_p99_ms": summary["observed"]["program_response_time_ms"]["p99"],
        "call_latency_mean_ms": summary["observed"]["call_latency_ms"]["mean"],
        "call_latency_p90_ms": summary["observed"]["call_latency_ms"]["p90"],
        "ptl_by_class": {c: round(statistics.mean(v), 2) for c, v in sorted(by_class.items()) if v},
        "workload_sha256": summary["workload"]["sha256"],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Compare FCFS vs PLAS on the Agentix metrics")
    ap.add_argument("--artifact-root", type=Path, required=True)
    ap.add_argument("--rates", nargs="+", type=int, default=[1, 2, 4])
    ap.add_argument("--seqs", nargs="+", type=int, default=[],
                    help="saturated layout: read sat_r<rate>_seq<N>/<policy> instead of r<rate>/<policy>")
    ap.add_argument("--policies", nargs="+", default=["fcfs", "plas"])
    ap.add_argument("--output-dir", type=Path, required=True)
    a = ap.parse_args()
    a.output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    if a.seqs:
        for rate in a.rates:
            for ms in a.seqs:
                for policy in a.policies:
                    d = a.artifact_root / f"sat_r{rate}_seq{ms}" / policy
                    s = summarise_dir(d, rate, policy) if d.exists() else None
                    if s:
                        s["max_num_seqs"] = ms
                        rows.append(s)
    else:
        for rate in a.rates:
            for policy in a.policies:
                s = summarise(a.artifact_root, rate, policy)
                if s:
                    rows.append(s)
    if not rows:
        raise SystemExit(f"no summaries found under {a.artifact_root}")
    _write_csv(a.output_dir / "policy_comparison.csv", rows)

    L = ["# Agentix-protocol reproduction on one RTX 4090 — FCFS vs PLAS", "",
         "Single GPU, LLaMA-3.1-8B bf16, vLLM 0.29.0, synthesised program workload (three classes + Mixed, Poisson arrivals).",
         "The paper's testbed is 8×A100-80GB; absolute numbers are not comparable, the comparison here is between policies on the same machine and workload.", "",
         "| arrival rate (prog/s) | batch cap | policy | programs | wall (s) | throughput (prog/s) | throughput (tok/s) | program-token latency mean / p90 (ms) | program response p90 (ms) | call latency mean (ms) |",
         "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in sorted(rows, key=lambda x: (x["arrival_rate"], x.get("max_num_seqs", 0), x["policy"])):
        cap = r.get("max_num_seqs", "none")
        L.append(f"| {r['arrival_rate']} | {cap} | {r['policy']} | {r['programs']} | {r['wall_s']:.1f} | "
                 f"{r['throughput_programs_per_s']:.3f} | {r['throughput_tokens_per_s']:.0f} | "
                 f"{r['ptl_mean_ms']:.1f} / {r['ptl_p90_ms']:.1f} | {r['response_p90_ms']:.0f} | {r['call_latency_mean_ms']:.0f} |")
    L += ["", "## Per-class program-token latency (mean ms)", "",
          "| arrival rate | policy | " + " | ".join(sorted({c for r in rows for c in r["ptl_by_class"]})) + " |",
          "|---:|---|" + "---:|" * len({c for r in rows for c in r["ptl_by_class"]})]
    for r in sorted(rows, key=lambda x: (x["arrival_rate"], x["policy"])):
        classes = sorted(r["ptl_by_class"])
        L.append(f"| {r['arrival_rate']} | {r['policy']} | " + " | ".join(f"{r['ptl_by_class'][c]:.1f}" for c in classes) + " |")
    L += ["", "## Policy comparison (PLAS / FCFS)", "",
          "| arrival rate | batch cap | throughput ratio | program-token latency ratio (mean) | latency ratio (p90) |",
          "|---:|---|---:|---:|---:|"]
    keys = sorted({(r["arrival_rate"], r.get("max_num_seqs")) for r in rows})
    for rate, cap in keys:
        f = next((r for r in rows if r["arrival_rate"] == rate and r.get("max_num_seqs") == cap and r["policy"] == "fcfs"), None)
        p = next((r for r in rows if r["arrival_rate"] == rate and r.get("max_num_seqs") == cap and r["policy"] == "plas"), None)
        if not f or not p:
            continue
        L.append(f"| {rate} | {cap if cap is not None else 'none'} | {p['throughput_programs_per_s'] / f['throughput_programs_per_s']:.2f}× | "
                 f"{p['ptl_mean_ms'] / f['ptl_mean_ms']:.2f}× | {p['ptl_p90_ms'] / f['ptl_p90_ms']:.2f}× |")
    (a.output_dir / "AGENTIX_8B_REPORT.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))
    return 0


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    flat = [{k: (json.dumps(v) if isinstance(v, dict) else v) for k, v in r.items()} for r in rows]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(flat[0].keys()))
        w.writeheader()
        w.writerows(flat)


if __name__ == "__main__":
    raise SystemExit(main())
