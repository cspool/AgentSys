"""Valve scoring: online TTFT/TPOT vs standalone; offline throughput measured
over the ALIGNED window (the online run's span), not over completed calls."""
import json, sys, os

VR = os.path.dirname(os.path.abspath(__file__))

def on_stats(d):
    calls = [json.loads(l) for l in open(f"{VR}/{d}/calls_atlas.jsonl")]
    tt = sorted(c['ttft_ms'] for c in calls)
    tp = sorted((c['call_latency_ms'] - c['ttft_ms']) / max(c['produced_tokens'] - 1, 1)
                for c in calls)
    n = len(tt)
    return {'ttft_p50': tt[n//2], 'ttft_p99': tt[int(n*.99)],
            'tpot_p50': tp[n//2], 'n': n,
            'span': (min(c['submitted_rel_ms'] for c in calls),
                     max(c['finished_rel_ms'] for c in calls))}

def off_tokens_in_window(d, lo_ms, hi_ms):
    """tokens produced by offline inside [lo,hi] of ITS OWN clock, assuming
    linear generation within each call (declared approximation)."""
    calls = [json.loads(l) for l in open(f"{VR}/{d}/calls_fcfs.jsonl")]
    tot = 0.0
    for c in calls:
        s, e = c['submitted_rel_ms'], c['finished_rel_ms']
        ov = max(0.0, min(e, hi_ms) - max(s, lo_ms))
        if ov > 0 and e > s:
            tot += c['produced_tokens'] * ov / (e - s)
    return tot / ((hi_ms - lo_ms) / 1000)

if __name__ == '__main__':
    OFFSET = float(sys.argv[1]) if len(sys.argv) > 1 else 45.0   # offline 提前启动秒数
    solo = on_stats('v3_on_solo')
    print(f"online solo: TTFT_p50={solo['ttft_p50']:.0f}ms p99={solo['ttft_p99']:.0f}ms "
          f"TPOT_p50={solo['tpot_p50']:.2f}ms (n={solo['n']})")
    w_lo, w_hi = solo['span'][0] + OFFSET*1000, solo['span'][1] + OFFSET*1000
    base_off = off_tokens_in_window('v3_off_solo', w_lo - OFFSET*1000, w_hi - OFFSET*1000)
    print(f"offline solo(同长窗口): {base_off:.1f} tok/s\n")
    print(f"{'臂':>9} {'TTFT p50':>9} {'Δ':>7} {'TTFT p99':>9} {'TPOT p50':>9} {'Δ':>7} "
          f"{'off tok/s':>10} {'保留':>6} {'抢占次数':>7}")
    for arm, ev in (('naive', None), ('channel', 'v3_channel_events.json'),
                    ('iter', 'v3_iter_events.json')):
        try:
            o = on_stats(f'v3_on_{arm}')
            off = off_tokens_in_window(f'v3_off_{arm}', w_lo, w_hi)
        except FileNotFoundError as e:
            print(f"{arm:>9}  缺 {os.path.basename(e.filename)}"); continue
        k = ''
        if ev and os.path.isfile(f"{VR}/{ev}"):
            k = json.load(open(f"{VR}/{ev}"))['preemptions']
        print(f"{arm:>9} {o['ttft_p50']:>8.0f}ms {(o['ttft_p50']-solo['ttft_p50'])/solo['ttft_p50']:>+6.0%} "
              f"{o['ttft_p99']:>8.0f}ms {o['tpot_p50']:>8.2f}ms "
              f"{(o['tpot_p50']-solo['tpot_p50'])/solo['tpot_p50']:>+6.0%} "
              f"{off:>10.1f} {off/base_off:>5.0%} {str(k):>7}")
