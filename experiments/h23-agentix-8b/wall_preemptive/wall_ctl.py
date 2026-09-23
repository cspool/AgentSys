"""Preemption-timing policies on the wall_preemptive benchmark.

Both policies admit the SAME number of preemption events K with the SAME work.
The ONLY difference is WHEN each event fires:

  valve       — Valve (arXiv 2604.07874) rule, faithfully transplanted:
                fire as soon as the high-priority (online) side turns busy;
                after it goes idle, wait T_cool (= 2x max decode-iteration gap)
                before releasing the victim. The victim's resource state is
                NOT consulted (verified against the paper: "the runtime
                immediately issues channel-disable commands ... when the online
                workload transitions to busy"; no victim-state term exists).

  wall_aware  — ours: same K, but each event is deferred until the victim is in
                a WALL state (one axis saturated, another idle), capped by a
                deadline so the policy can never delay an event beyond one
                period (bounded latency, same as Valve's rate bound).

Both read the victim's published state; only wall_aware acts on it.
"""
import argparse, json, os, random, time

ap = argparse.ArgumentParser()
ap.add_argument('--mode', choices=['valve', 'wall_aware', 'random_defer'], required=True,
                help="random_defer = 公平性对照臂:与 wall_aware 花掉完全相同的推迟预算,"
                     "但推迟量与受害者状态无关(打乱顺序重放)。"
                     "若 wall_aware 胜过它,收益才确属'墙感知'而非'推迟'本身。")
ap.add_argument('--state-file', default='/tmp/wp_state.json')
ap.add_argument('--online-file', default='/tmp/wp_online.json',
                help='高优先级侧忙闲信号(Valve 规则的唯一输入)')
ap.add_argument('--k', type=int, default=40)
ap.add_argument('--period', type=float, default=2.0)
ap.add_argument('--cool', type=float, default=0.074)
ap.add_argument('--deadline-frac', type=float, default=0.9)
ap.add_argument('--trigger', default='/tmp/wp_trigger')
ap.add_argument('--seed', type=int, default=20260921,
                help='到达序列随机种子:两臂必须相同 —— 固定周期会与受害者相位周期混叠,使落点不再是随机采样(2026-09-21 实测 0/150)')
ap.add_argument('--delay-file', default=None,
                help='random_defer:读取 wall_aware 的实测推迟序列')
ap.add_argument('--out', required=True)
a = ap.parse_args()


def victim_phase():
    try:
        return json.load(open(a.state_file)).get('phase', '?')
    except Exception:
        return '?'


# 两臂共享同一"高优先级到达序列"(tick 即到达),因此 Valve 规则的输入完全相同:
#   Valve: 到达即抢占(不查受害者状态)
#   Ours : 同一到达,推迟到受害者进入墙态(截止期限封顶)


# 泊松式到达(指数间隔,均值=period),两臂同种子 → 同一到达序列,消除周期混叠
_rng = random.Random(a.seed)
_gaps = [_rng.expovariate(1.0 / a.period) for _ in range(a.k)]
_sched, _acc = [], 0.0
for g in _gaps:
    _acc += max(0.15, min(g, a.period * 3))
    _sched.append(_acc)

_defers = []
if a.mode == 'random_defer' and a.delay_file:
    _src = json.load(open(a.delay_file))
    _defers = [e['delay_ms'] for e in _src['events']]
    random.Random(a.seed + 1).shuffle(_defers)   # 同预算、打乱顺序 → 与状态无关

log, t0 = [], time.time()
for i in range(a.k):
    tick = t0 + _sched[i]
    while time.time() < tick:
        time.sleep(0.002)
    _budget = (_sched[i+1]-_sched[i]) if i+1 < len(_sched) else a.period
    deadline = tick + _budget * a.deadline_frac
    forced = False
    if a.mode == 'wall_aware':
        while victim_phase() != 'wall' and time.time() < deadline:
            time.sleep(0.003)
        forced = victim_phase() != 'wall'
    elif a.mode == 'random_defer':
        # 花掉与 wall_aware 相同的推迟预算,但与受害者状态无关
        d = _defers[i % len(_defers)] / 1000.0 if _defers else 0.0
        tgt = min(tick + d, deadline)
        while time.time() < tgt:
            time.sleep(0.003)
    ph = victim_phase()
    with open(a.trigger, 'w') as f:
        f.write(str(i))
    log.append({'i': i, 't': time.time() - t0, 'fired_phase': ph, 'forced': forced,
                'delay_ms': (time.time() - tick) * 1000})
    if a.mode == 'valve':
        time.sleep(a.cool)          # Valve 的冷却间隔(释放前等待)
json.dump({'mode': a.mode, 'k': a.k, 'events': log,
           'hit_wall': sum(1 for e in log if e['fired_phase'] == 'wall'),
           'forced': sum(1 for e in log if e['forced']),
           'mean_delay_ms': sum(e['delay_ms'] for e in log) / max(len(log), 1)},
          open(a.out, 'w'))
print(f"{a.mode}: K={a.k} 落墙态={sum(1 for e in log if e['fired_phase']=='wall')} "
      f"强发={sum(1 for e in log if e['forced'])} "
      f"平均延迟={sum(e['delay_ms'] for e in log)/max(len(log),1):.0f}ms")
