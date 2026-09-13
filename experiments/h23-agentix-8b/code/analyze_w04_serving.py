#!/usr/bin/env python3
"""w04'' / G05 adapted: full-workload estimate via a concurrency-conditioned step model.

Goal unchanged from h22 w04: build a cost template from a *representative*
observation, predict a *target* workload from structure alone, then score the
prediction against the target's own measurement.

Serving adaptation (protocol.md): under continuous batching a kernel belongs to
the dynamic batch, not to a call, so the per-(call, op) template is undefined.
The template here is the relation

    gpu_busy_fraction(t)  ~  f(concurrent_requests(t))

fitted as per-bucket means over fixed time slices of the representative capture.
Prediction for the target: apply f to the target's own concurrency timeline
(client marks only — no GPU data needed for the prediction), integrate, and
score against the target's measured GPU busy inside its captured span.
"""

from __future__ import annotations

import argparse
import bisect
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "h22-gpu-autotrace" / "code"))
from analyze_w01_operator_trace import _sha256, _union_busy, _write_csv  # noqa: E402

CALL_BEGIN = "agentix.call_begin::"
CALL_END = "agentix.call_end::"
BUCKETS = [(0, 0, "0"), (1, 1, "1"), (2, 3, "2-3"), (4, 7, "4-7"), (8, 15, "8-15"), (16, 31, "16-31"), (32, 10**9, "32+")]
SLICE_NS = 100_000_000  # 100 ms


def load(path: Path):
    db = sqlite3.connect(str(path))
    strings = dict(db.execute("select id, value from StringIds"))
    begins, ends = [], []
    for start, text, text_id in db.execute("select start, text, textId from NVTX_EVENTS"):
        name = text if text else strings.get(text_id, "")
        if name.startswith(CALL_BEGIN):
            begins.append(start)
        elif name.startswith(CALL_END):
            ends.append(start)
    work = [(s, e) for s, e in db.execute("select start, end from CUPTI_ACTIVITY_KIND_KERNEL")]
    work += [(s, e) for s, e in db.execute("select start, end from CUPTI_ACTIVITY_KIND_MEMCPY")]
    db.close()
    return sorted(begins), sorted(ends), sorted(work)


def slices(path: Path):
    """(bucket, busy_fraction) per 100 ms slice inside the captured CUDA span."""
    begins, ends, work = load(path)
    span = (work[0][0], max(e for _, e in work))
    out = []
    t = span[0]
    while t + SLICE_NS <= span[1]:
        busy = _union_busy([(max(s, t), min(e, t + SLICE_NS)) for s, e in work if e > t and s < t + SLICE_NS])
        mid = t + SLICE_NS // 2
        conc = bisect.bisect_right(begins, mid) - bisect.bisect_right(ends, mid)
        label = next(n for lo, hi, n in BUCKETS if lo <= conc <= hi)
        out.append({"t_rel_s": round((t - span[0]) / 1e9, 1), "concurrency": conc, "bucket": label,
                    "busy_frac": busy / SLICE_NS})
        t += SLICE_NS
    return out, span


def main() -> int:
    ap = argparse.ArgumentParser(description="w04'' concurrency-conditioned step model")
    ap.add_argument("--representative-sqlite", type=Path, required=True)
    ap.add_argument("--target-sqlite", type=Path, required=True)
    ap.add_argument("--rep-w01", type=Path, required=True)
    ap.add_argument("--target-w01", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    a = ap.parse_args()
    a.output_dir.mkdir(parents=True, exist_ok=True)

    for w01_path, sq in ((a.rep_w01, a.representative_sqlite), (a.target_w01, a.target_sqlite)):
        w01 = json.loads(w01_path.read_text())
        if not w01.get("pass"):
            raise SystemExit(f"admission refused: {w01_path} did not pass")
        if w01["sqlite_sha256"] != _sha256(sq):
            raise SystemExit(f"admission refused: sha mismatch for {sq}")

    rep_rows, rep_span = slices(a.representative_sqlite)
    tgt_rows, tgt_span = slices(a.target_sqlite)

    # template: mean busy fraction per concurrency bucket (representative)
    grp: dict[str, list[float]] = defaultdict(list)
    for r in rep_rows:
        grp[r["bucket"]].append(r["busy_frac"])
    template = {b: sum(v) / len(v) for b, v in grp.items()}
    order = [n for _, _, n in BUCKETS]
    _write_csv(a.output_dir / "step_model_template.csv",
               [{"bucket": b, "slices": len(grp[b]), "busy_frac_mean": round(template[b], 4)}
                for b in order if b in template])

    # predict the target from its concurrency timeline alone
    missing = sorted({r["bucket"] for r in tgt_rows} - set(template))
    fallback = {}
    for b in missing:
        # nearest covered bucket (flagged), as h22 w04 does for missing matrix sizes
        idx = order.index(b)
        near = min((o for o in template), key=lambda o: abs(order.index(o) - idx))
        fallback[b] = near
    pred_rows = []
    for r in tgt_rows:
        b = r["bucket"]
        src = "template" if b in template else f"nearest:{fallback[b]}"
        est = template.get(b, template[fallback.get(b, "0")])
        pred_rows.append({**r, "predicted_busy_frac": round(est, 4), "source": src})
    _write_csv(a.output_dir / "target_prediction.csv", pred_rows)

    pred_busy = sum(r["predicted_busy_frac"] for r in pred_rows) * SLICE_NS
    act_busy = sum(r["busy_frac"] for r in tgt_rows) * SLICE_NS
    err_pct = 100 * (pred_busy - act_busy) / act_busy if act_busy else None

    per_bucket = []
    for b in order:
        rows = [r for r in pred_rows if r["bucket"] == b]
        if not rows:
            continue
        pa = sum(r["busy_frac"] for r in rows) / len(rows)
        pp = sum(r["predicted_busy_frac"] for r in rows) / len(rows)
        per_bucket.append({"bucket": b, "target_slices": len(rows), "actual_busy_frac": round(pa, 4),
                           "predicted_busy_frac": round(pp, 4),
                           "err_pct": round(100 * (pp - pa) / pa, 1) if pa else ""})
    _write_csv(a.output_dir / "per_bucket_scoring.csv", per_bucket)

    summary = {
        "schema_version": 1, "lineage": "h23-agentix-8b/autotrace", "goal": "G05'",
        "method": "concurrency-conditioned step model (serving adaptation of the h22 w04 template)",
        "representative": {"sqlite": str(a.representative_sqlite), "sqlite_sha256": _sha256(a.representative_sqlite),
                           "slices": len(rep_rows), "span_s": round((rep_span[1] - rep_span[0]) / 1e9, 1)},
        "target": {"sqlite": str(a.target_sqlite), "sqlite_sha256": _sha256(a.target_sqlite),
                   "slices": len(tgt_rows), "span_s": round((tgt_span[1] - tgt_span[0]) / 1e9, 1)},
        "template_buckets": {b: round(v, 4) for b, v in sorted(template.items(), key=lambda kv: order.index(kv[0]))},
        "coverage": {"target_buckets": len({r['bucket'] for r in tgt_rows}),
                     "missing_template_buckets": missing, "nearest_fallbacks": fallback},
        "scoring": {"predicted_gpu_busy_s": round(pred_busy / 1e9, 3), "actual_gpu_busy_s": round(act_busy / 1e9, 3),
                    "total_err_pct": round(err_pct, 2) if err_pct is not None else None},
        "note": "prediction consumes only the target's client-side concurrency timeline; its GPU data is used only for scoring, mirroring h22 w04's plan-side enumeration + trace-side scoring",
        "pass": err_pct is not None and abs(err_pct) <= 25.0 and not missing,
    }
    (a.output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: summary[k] for k in ("template_buckets", "coverage", "scoring", "pass")}, indent=2))
    return 0 if summary["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
