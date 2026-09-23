"""Wall-aware preemption controller (our method) vs Valve's busy-triggered rule.

Both admit the SAME number of preemption events K. The only difference is WHEN:
  valve      : fire as soon as the online side is busy (+ T_cool before release)
  wall_aware : same K, but defer each event until the victim is in a WALL state
               (one axis saturated, another idle), with a deadline cap.
Victim wall state is read from a phase file the victim writes each kernel.
"""
import argparse, json, os, time

ap = argparse.ArgumentParser()
ap.add_argument('--mode', choices=['valve', 'wall_aware'], required=True)
ap.add_argument('--state-file', default='/tmp/wp_state.json')
ap.add_argument('--k', type=int, default=40)
ap.add_argument('--period', type=float, default=2.0)
ap.add_argument('--deadline-frac', type=float, default=0.9)
ap.add_argument('--out', required=True)
a = ap.parse_args()


def state():
    try:
        return json.load(open(a.state_file))
    except Exception:
        return {'phase': '?'}


log, t0 = [], time.time()
for i in range(a.k):
    tick = t0 + (i + 1) * a.period
    while time.time() < tick:
        time.sleep(0.002)
    deadline = tick + a.period * a.deadline_frac
    forced = False
    if a.mode == 'wall_aware':
        while state().get('phase') != 'wall' and time.time() < deadline:
            time.sleep(0.003)
        forced = state().get('phase') != 'wall'
    ph = state().get('phase', '?')
    # 触发信号:写 trigger 文件,由 burst 进程消费(保证两臂 K 相同)
    with open('/tmp/wp_trigger', 'w') as f:
        f.write(str(i))
    log.append({'i': i, 't': time.time() - t0, 'fired_phase': ph, 'forced': forced})
json.dump({'mode': a.mode, 'k': a.k, 'events': log,
           'hit_wall': sum(1 for e in log if e['fired_phase'] == 'wall'),
           'forced': sum(1 for e in log if e['forced'])}, open(a.out, 'w'))
print(f"{a.mode}: K={a.k} 落在墙态={sum(1 for e in log if e['fired_phase']=='wall')} "
      f"强发={sum(1 for e in log if e['forced'])}")
