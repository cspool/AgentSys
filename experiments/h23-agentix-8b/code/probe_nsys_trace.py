#!/usr/bin/env python3
"""Inventory an nsys sqlite: processes, NVTX name families, GPU activity counts.

Run this first on a fresh capture so the serving-adapted AutoTrace analyzers are
written against what the trace actually contains rather than an assumption.
"""

from __future__ import annotations

import argparse
import sqlite3
from collections import Counter
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sqlite", type=Path, required=True)
    ap.add_argument("--top", type=int, default=25)
    a = ap.parse_args()
    db = sqlite3.connect(str(a.sqlite))
    strings = dict(db.execute("select id, value from StringIds"))

    rows = db.execute("select start, end, textId, globalTid from NVTX_EVENTS where textId is not null").fetchall()
    procs = Counter(r[3] for r in rows)
    print(f"NVTX events: {len(rows)}  over {len(procs)} globalTid")
    for tid, n in procs.most_common(6):
        print(f"  globalTid={tid} events={n}")

    fam = Counter()
    for _, _, text_id, _ in rows:
        text = strings.get(text_id, "")
        head = text.split("::")[0] if "::" in text else text.split("(")[0][:60]
        fam[head] += 1
    print("\nNVTX name families:")
    for name, n in fam.most_common(a.top):
        print(f"  {n:6d}  {name[:110]}")

    print("\nsample texts per family:")
    seen: dict[str, int] = {}
    for _, _, text_id, _ in rows:
        text = strings.get(text_id, "")
        head = text.split("::")[0] if "::" in text else text.split("(")[0][:60]
        if seen.get(head, 0) < 3:
            seen[head] = seen.get(head, 0) + 1
            print(f"  [{head[:40]}] {text[:150]}")

    for table, cols in (("CUPTI_ACTIVITY_KIND_KERNEL", "count(*)"),
                        ("CUPTI_ACTIVITY_KIND_MEMCPY", "count(*)"),
                        ("CUPTI_ACTIVITY_KIND_RUNTIME", "count(*)")):
        try:
            print(f"\n{table}: {db.execute(f'select {cols} from {table}').fetchone()[0]} rows")
        except sqlite3.Error as exc:
            print(f"\n{table}: n/a ({exc})")
    db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
