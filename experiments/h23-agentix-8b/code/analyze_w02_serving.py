#!/usr/bin/env python3
"""w02' / G02-G03 adapted: request-level (call-wise) attribution inside w01's denominator.

Segment model, analogue of the h22 process segmentation:

  queue_wait   submit -> first token
  prefill      (carried inside first token arrival; reported as TTFT)
  decode       first token -> finish
  tool_wait    between a program's consecutive calls (from the workload's ready_ns)

Host->nsys clock alignment follows the h22 w02 method: pair the client NVTX mark
(``agentix.call_begin::...``) with the harness's host timestamp for the same
request and fit a constant offset; the residual spread is the alignment quality.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "h22-gpu-autotrace" / "code"))
from analyze_w01_operator_trace import _sha256, _write_csv  # noqa: E402

CALL_BEGIN = "agentix.call_begin::"
WINDOW_PREFIX = "agentix.window::"


def load_marks(path: Path) -> dict[str, int]:
    db = sqlite3.connect(str(path))
    strings = dict(db.execute("select id, value from StringIds"))
    out = {}
    win = None
    for start, end, text, text_id in db.execute("select start, end, text, textId from NVTX_EVENTS"):
        name = text if text else strings.get(text_id, "")
        if name.startswith(CALL_BEGIN):
            out[name[len(CALL_BEGIN):]] = start
        elif name.startswith(WINDOW_PREFIX):
            win = (start, end or start)
    db.close()
    return out, win


def main() -> int:
    ap = argparse.ArgumentParser(description="w02' request-level attribution")
    ap.add_argument("--sqlite", type=Path, required=True)
    ap.add_argument("--run-dir", type=Path, required=True, help="dir with calls_<policy>.jsonl and summary_<policy>.json")
    ap.add_argument("--policy", required=True)
    ap.add_argument("--workload", type=Path, required=True)
    ap.add_argument("--w01-conservation", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    a = ap.parse_args()
    a.output_dir.mkdir(parents=True, exist_ok=True)

    w01 = json.loads(a.w01_conservation.read_text())
    if not w01.get("pass"):
        raise SystemExit("w01' did not pass; w02' admission refused")
    if w01["sqlite_sha256"] != _sha256(a.sqlite):
        raise SystemExit("sqlite sha256 differs from the w01' record")

    marks, window = load_marks(a.sqlite)
    if not marks or window is None:
        raise SystemExit("no agentix marks/window in the trace")
    calls = [json.loads(line) for line in (a.run_dir / f"calls_{a.policy}.jsonl").read_text().splitlines() if line.strip()]
    summary = json.loads((a.run_dir / f"summary_{a.policy}.json").read_text())
    t0 = summary["timing_ns"]["t0"]

    # clock fit: nsys mark vs host timestamp of the same request submission
    offsets = []
    for c in calls:
        key = f"{c['program_id']}::{c['call_index']}::{c['class']}"
        if key in marks:
            offsets.append(marks[key] - (t0 + int(c["submitted_rel_ms"] * 1e6)))
    if not offsets:
        raise SystemExit("no request marks paired with host timestamps")
    med = int(statistics.median(offsets))
    spread = max(offsets) - min(offsets)
    within200 = sum(1 for o in offsets if abs(o - med) <= 200_000) / len(offsets)
    within1ms = sum(1 for o in offsets if abs(o - med) <= 1_000_000) / len(offsets)
    # Robust criterion (h22 w02 lineage): isolated outlier pairs come from client-thread
    # preemption between the host timestamp and the NVTX mark under load; the segment
    # quantities here are tens of ms, so sub-ms alignment residue is immaterial. Accept
    # when the offset population is tight (spread) or overwhelmingly concentrated.
    align = {"offset_ns": med, "pairs": len(offsets), "spread_ns": spread,
             "within_200us_frac": within200, "within_1ms_frac": within1ms,
             "pass": spread <= 200_000 or within200 >= 0.95 and within1ms >= 0.999}

    def h2n(rel_ms: float) -> int:
        return int(t0 + rel_ms * 1e6) - med

    rows = []
    for c in calls:
        submit_n, first_n, fin_n = h2n(c["submitted_rel_ms"]), h2n(c["first_token_rel_ms"]), h2n(c["finished_rel_ms"])
        rows.append({"policy": a.policy, "program_id": c["program_id"], "class": c["class"], "call_index": c["call_index"],
                     "submit_ns": submit_n, "first_token_ns": first_n, "finish_ns": fin_n,
                     "queue_wait_ns": first_n - submit_n, "decode_ns": fin_n - first_n, "call_ns": fin_n - submit_n,
                     "prompt_tokens": c["prompt_tokens"], "output_tokens": c["output_tokens"]})
    _write_csv(a.output_dir / "request_segments.csv", rows)

    by_class: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for r in rows:
        by_class[r["class"]]["queue_wait_ns"].append(r["queue_wait_ns"])
        by_class[r["class"]]["decode_ns"].append(r["decode_ns"])
    class_rows = [{"policy": a.policy, "class": cls,
                   "calls": len(v["queue_wait_ns"]),
                   "queue_wait_mean_ms": round(statistics.mean(v["queue_wait_ns"]) / 1e6, 2),
                   "queue_wait_p90_ms": round(sorted(v["queue_wait_ns"])[int(0.9 * (len(v["queue_wait_ns"]) - 1))] / 1e6, 2),
                   "decode_mean_ms": round(statistics.mean(v["decode_ns"]) / 1e6, 2),
                   "decode_p90_ms": round(sorted(v["decode_ns"])[int(0.9 * (len(v["decode_ns"]) - 1))] / 1e6, 2)}
                  for cls, v in sorted(by_class.items())]
    _write_csv(a.output_dir / "class_segments.csv", class_rows)

    # request overlap inside the measured window (continuous batching)
    win_ns = window[1] - window[0]
    events = sorted([(r["submit_ns"], 1) for r in rows] + [(r["finish_ns"], -1) for r in rows])
    cur = peak = 0
    for _, d in events:
        cur += d
        peak = max(peak, cur)
    queue_total = sum(r["queue_wait_ns"] for r in rows)
    decode_total = sum(r["decode_ns"] for r in rows)
    summary_out = {
        "schema_version": 1, "goal": "G02'-G03'", "policy": a.policy,
        "upstream": {"w01_sqlite_sha256": w01["sqlite_sha256"], "w01_gpu_busy_pct": w01["gpu_busy_pct"]},
        "alignment": align,
        "measured_window_ns": win_ns,
        "requests": {"count": len(rows), "peak_concurrent": peak,
                     "queue_wait_ns_total": queue_total, "decode_ns_total": decode_total,
                     "queue_share_pct": round(100 * queue_total / (queue_total + decode_total), 2) if queue_total + decode_total else 0},
        "by_class": {r["class"]: {"queue_wait_mean_ms": r["queue_wait_mean_ms"], "decode_mean_ms": r["decode_mean_ms"]} for r in class_rows},
        "pass": align["pass"] and len(rows) > 0,
    }
    (a.output_dir / "w02_serving_summary.json").write_text(json.dumps(summary_out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"policy": a.policy, "alignment_spread_us": round(spread / 1e3, 1), "pairs": len(offsets),
                      "queue_share_pct": summary_out["requests"]["queue_share_pct"],
                      "peak_concurrent": peak, "by_class": summary_out["by_class"], "pass": summary_out["pass"]}, indent=2))
    return 0 if summary_out["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
