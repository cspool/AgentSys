"""Aggregate the four-arm end-to-end comparison + output-drift gate.

Token-id sequences are not persisted by serve_agentix; the drift gate uses
output_tokens counts per (program_id, call_index) as a coarse equivalence
signal (greedy decode: changed numerics => changed lengths shows up fast).
Declared as coarse — full token-id equivalence needs a rerun with dump.
"""
import json, sys, statistics as st
from pathlib import Path

ROOT = Path("/workspace/AgentSys/artifacts/agentix_8b/astra_e2e")
ARMS = ["ctrl", "a1_silu", "a2_rms", "b_graph"]

def load(arm):
    d = ROOT / arm
    s = json.load(open(d / "summary_agentix_core.json"))
    calls = [json.loads(l) for l in open(d / "calls_agentix_core.jsonl")]
    return s, calls

base_calls = None
rows = []
for arm in ARMS:
    try:
        s, calls = load(arm)
    except FileNotFoundError:
        rows.append((arm, None)); continue
    o = s["observed"]
    lat = sorted(c["call_latency_ms"] for c in calls)
    n = len(lat)
    row = {
        "tok_s": o.get("throughput_tokens_per_s"),
        "wall_s": o.get("wall_s"),
        "call_p50_ms": lat[n//2],
        "call_p90_ms": lat[int(n*0.9)],
        "ttft_p50_ms": sorted(c["ttft_ms"] for c in calls)[n//2],
    }
    key = {(c["program_id"], c["call_index"]): c["output_tokens"] for c in calls}
    if arm == "ctrl":
        base_calls = key
        row["drift"] = "-"
    elif base_calls:
        diff = sum(1 for k, v in key.items() if base_calls.get(k) != v)
        row["drift"] = f"{diff}/{len(key)} calls"
    rows.append((arm, row))

hdr = ["arm", "tok/s", "wall_s", "call_p50", "call_p90", "ttft_p50", "outdrift"]
print(" | ".join(f"{h:>9}" for h in hdr))
for arm, r in rows:
    if r is None:
        print(f"{arm:>9} | (缺)"); continue
    print(f"{arm:>9} | {r['tok_s']:>9.1f} | {r['wall_s']:>7.1f} | "
          f"{r['call_p50_ms']:>8.0f} | {r['call_p90_ms']:>8.0f} | "
          f"{r['ttft_p50_ms']:>8.0f} | {r['drift']}")
