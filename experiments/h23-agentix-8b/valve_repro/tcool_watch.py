import json, os, sys, time
"""T_cool = 2 x max gap BETWEEN DECODE ITERATIONS (paper §4.2).
Only counts inter-step gaps while the engine has running requests;
idle stretches between bursts are NOT decode-iteration gaps."""
flag, out = sys.argv[1], sys.argv[2]
gaps, last_m, last_busy = [], None, False
t_start = time.time()
while True:
    try:
        m = os.path.getmtime(flag)
        busy = json.load(open(flag)).get('n_running', 0) > 0
        if m != last_m:
            if last_m is not None and last_busy and busy:
                gaps.append(m - last_m)
            last_m, last_busy = m, busy
    except Exception:
        pass
    time.sleep(0.002)
    if last_m and time.time() - last_m > 5.0 and gaps:
        break
    if time.time() - t_start > 600:
        break
g = max(gaps) if gaps else 0.05
json.dump({'max_decode_gap_s': g, 't_cool_s': 2*g, 'n_gaps': len(gaps),
           'p99_gap_s': sorted(gaps)[int(len(gaps)*0.99)] if gaps else None},
          open(out, 'w'))
print(f"G={g*1000:.1f}ms T_cool={2*g*1000:.1f}ms n={len(gaps)}")
