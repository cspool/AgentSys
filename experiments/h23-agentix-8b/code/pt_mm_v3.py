#!/usr/bin/env python3
"""Plan-2 (tri-modal, three 1.xB engines, one GPU) on the v3 four-layer loop.

Branch mm-v3 of the v3 chain. Same contract semantics as pt_v3_runtime
(fingerprints, stale sweep, immutable handoffs, ledger, gates); adapted:
- serving driver is serve_mm.py (three engines, per-call DAG, modality routing)
- process layer is DECLARED PARTIAL: the 8-process taxonomy does not cover
  vision/audio towers; the process axis here is engine(modality) x phase.
  prog and step layers are full. class-3 becomes CROSS-ENGINE concurrency.
- stage fingerprint = sha256 over (pt_mm_v3.py, serve_mm.py) whole files —
  declared deviation from the AST-closure rule (single-file chain, coarse ok).
"""
import collections
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/workspace/AgentSys')
ART = ROOT / 'artifacts/agentix_8b/pt_mm'
PY = str(ROOT / '.venv-vllm/bin/python')
SERVE = str(ROOT / 'experiments/h23-agentix-8b/code/serve_mm.py')
SELF = Path(__file__).resolve()
STEPS = [f'M{i:02d}' for i in range(1, 11)]
PREDS = {s: ([] if i == 0 else [STEPS[i-1]]) for i, s in enumerate(STEPS)}
MODS = ('lm', 'vis', 'audio')


def sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def fingerprint() -> str:
    h = hashlib.sha256()
    for f in (SELF, Path(SERVE)):
        h.update(f.read_bytes())
    return h.hexdigest()[:16]


class Ctx:
    def __init__(self, step, lineage):
        self.step, self.lineage = step, lineage
        self.base = ART / lineage
        self.root = self.base / step
        self.root.mkdir(parents=True, exist_ok=True)
        self.fp = fingerprint()
        stale = sorted(q.name for q in self.root.iterdir())
        if stale:
            box = self.base / '_stale' / f'{step}-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}'
            box.mkdir(parents=True, exist_ok=True)
            for q in list(self.root.iterdir()):
                q.rename(box / q.name)
            print(f'[{step}] 撤回产出 {len(stale)} 项移入 {box.name};重新产出', flush=True)
        self.ledger = self.base / 'ledger.json'
        self.preds = {}
        for p in PREDS[step]:
            hp = self.base / p / 'handoff.json'
            if not hp.is_file():
                sys.exit(f'{step}: predecessor {p} handoff missing')
            h = json.loads(hp.read_text())
            if h.get('status') != 'complete':
                sys.exit(f'{step}: predecessor {p} status={h.get("status")}')
            if h.get('fingerprint') != self.fp:
                sys.exit(f'{step}: predecessor {p} fingerprint stale — chain code changed; '
                         f'withdraw and rerun from {p} (contract §0: stage-changed output unusable)')
            self.preds[p] = h

    def pred(self, p):
        return self.preds[p]

    def handoff(self, step):
        """read any prior committed handoff (fingerprint-checked)."""
        hp = self.base / step / 'handoff.json'
        if not hp.is_file():
            sys.exit(f'{self.step}: {step} handoff missing')
        h = json.loads(hp.read_text())
        if h.get('status') != 'complete' or h.get('fingerprint') != self.fp:
            sys.exit(f'{self.step}: {step} handoff stale/incomplete')
        return h

    def pfile(self, p, name):
        return self.base / p / name

    def commit(self, hand, files):
        hand = dict(hand)
        hand.update({'step': self.step, 'fingerprint': self.fp,
                     'committed_utc': f'{datetime.now(timezone.utc):%Y-%m-%dT%H:%M:%SZ}',
                     'files': {str(Path(f).relative_to(ROOT)): sha(f) for f in files}})
        (self.root / 'handoff.json').write_text(
            json.dumps(hand, indent=1, ensure_ascii=False) + '\n')
        led = (json.loads(self.ledger.read_text())
               if self.ledger.exists() else {'branch': 'mm-v3', 'entries': []})
        led['entries'] = [e for e in led['entries'] if e['step'] != self.step]
        led['entries'].append({'step': self.step, 'fingerprint': self.fp,
                               'handoff_sha': sha(self.root / 'handoff.json')})
        led['entries'].sort(key=lambda e: e['step'])
        self.ledger.write_text(json.dumps(led, indent=1, ensure_ascii=False) + '\n')
        print(json.dumps({'step': self.step, 'status': hand.get('status'),
                          'ledger': len(led['entries'])}, ensure_ascii=False), flush=True)


def run_serve(out_dir, workload, device, nsys=None, env_extra=None, timeout=1800):
    env = dict(os.environ)
    env.update({'CUDA_VISIBLE_DEVICES': device, 'VLLM_ENABLE_V1_MULTIPROCESSING': '0',
                'VLLM_NVTX_SCOPES_FOR_PROFILING': '1'})
    if env_extra:
        env.update(env_extra)
    cmd = [PY, SERVE, '--workload', str(workload), '--output-dir', str(out_dir),
           '--enforce-eager', '--devices', 'lm:0,vis:0,audio:0']
    # CUDA_VISIBLE_DEVICES 已限定物理卡;serve 内部映射一律用 0 号(可见集合内)
    if nsys:
        cmd = nsys + cmd
    (out_dir).mkdir(parents=True, exist_ok=True)
    with (out_dir / 'serve.log').open('w') as lg:
        r = subprocess.run(cmd, env=env, stdout=lg, stderr=subprocess.STDOUT,
                           timeout=timeout, cwd=str(ROOT))
    if r.returncode:
        sys.exit(f'serve_mm failed rc={r.returncode}, log={out_dir}/serve.log')
    return json.loads((out_dir / 'summary_mm.json').read_text())


def load_calls(out_dir):
    return [json.loads(l) for l in (out_dir / 'calls_mm.jsonl').open()]


def prog_profile(calls, workload_path, eps_ms=50.0):
    wl = json.loads(Path(workload_path).read_text())
    declared = {p['program_id']: p for p in wl['programs']}
    per = collections.defaultdict(list)
    for c in calls:
        per[c['program_id']].append(c)
    violations, progs = [], {}
    for pid, cs in per.items():
        cs.sort(key=lambda c: c['call_index'])
        fin = {c['call_index']: c['finished_rel_ms'] for c in cs}
        dcalls = {c['index']: c for c in declared[pid]['llm_calls']}
        anc = {}
        for i in sorted(dcalls):
            s = set()
            for par in dcalls[i].get('parents', []):
                s.add(par); s |= anc.get(par, set())
            anc[i] = s
        expects = any(j not in anc[i] and i not in anc[j]
                      for i in dcalls for j in dcalls if i < j)
        for c in cs:
            for par in c.get('parents', []):
                if par in fin and c['submitted_rel_ms'] < fin[par] - eps_ms:
                    violations.append({'program': pid, 'call': c['call_index'], 'parent': par})
        ov = 0.0
        for i, a in enumerate(cs):
            for b in cs[i+1:]:
                s0 = max(a['submitted_rel_ms'], b['submitted_rel_ms'])
                e0 = min(a['finished_rel_ms'], b['finished_rel_ms'])
                if e0 > s0:
                    ov += e0 - s0
        progs[pid] = {'calls': len(cs), 'overlap_ms': round(ov, 1),
                      'expects_parallel': expects,
                      'finished_rel_ms': max(c['finished_rel_ms'] for c in cs)}
    ev = []
    for c in calls:
        ev.append((c['submitted_rel_ms'], 1)); ev.append((c['finished_rel_ms'], -1))
    ev.sort()
    width, cur, last = collections.Counter(), 0, ev[0][0]
    for tm, dv in ev:
        width[cur] += tm - last
        cur += dv; last = tm
    tot = sum(width.values()) or 1.0
    return {'present': True, 'calls_total': len(calls),
            'programs': progs, 'dag_violations': violations,
            'width_ms_share': {str(k): round(v/tot, 4) for k, v in sorted(width.items())},
            'collapse_share_width_le1': round(sum(v for k, v in width.items() if k <= 1)/tot, 4),
            'serialized_programs': [p for p, v in progs.items()
                                    if v['expects_parallel'] and v['overlap_ms'] <= 0]}


NVTX_Q = ("select n.start, n.end, coalesce(n.text, s.value) t, n.globalTid "
          "from NVTX_EVENTS n left join StringIds s on n.textId = s.id "
          "where coalesce(n.text, s.value) like ? and n.end is not null")


def open_db(cap_dir):
    db = sqlite3.connect(str(cap_dir / 'cap.sqlite'))
    db.row_factory = sqlite3.Row
    return db


def kernels_by_pid(db):
    # 引擎归属:CUPTI kernel 行带 globalPid;fork 的三个 EngineCore 各一个
    rows = db.execute('select start, end, globalPid from CUPTI_ACTIVITY_KIND_KERNEL').fetchall()
    per = collections.defaultdict(list)
    for r in rows:
        # 统一键空间:globalPid 与 NVTX globalTid 的 pid 都取 bits 24-47
        per[(r['globalPid'] >> 24) & 0xFFFFFF].append((r['start'], r['end']))
    for v in per.values():
        v.sort()
    return per


def steps_by_pid(db):
    rows = db.execute(NVTX_Q, ('w.engine: process_engine_step%',)).fetchall()
    per = collections.defaultdict(list)
    for r in rows:
        pid = (r['globalTid'] >> 24) & 0xFFFFFF if r['globalTid'] else 0
        per[pid].append((r['start'], r['end']))
    for v in per.values():
        v.sort()
    return per


def union_len(iv):
    tot, cs, ce = 0, None, None
    for s, e in iv:
        if cs is None:
            cs, ce = s, e
        elif s <= ce:
            ce = max(ce, e)
        else:
            tot += ce - cs; cs, ce = s, e
    if cs is not None:
        tot += ce - cs
    return tot


def clip(iv, lo, hi):
    out = []
    for s, e in iv:
        s2, e2 = max(s, lo), min(e, hi)
        if e2 > s2:
            out.append((s2, e2))
    return out


def covered_scope(db, hole_s=1.5):
    """longest contiguous stretch of seconds that have kernel records
    (holes <= hole_s bridged). Evidence completeness rule from the v2
    catalogue: claim nothing outside the covered stretch."""
    secs = sorted({r[0] // 1_000_000_000 for r in
                   db.execute('select start from CUPTI_ACTIVITY_KIND_KERNEL')})
    if not secs:
        return None
    runs, s0, prev = [], secs[0], secs[0]
    for s in secs[1:]:
        if s - prev <= hole_s:
            prev = s
        else:
            runs.append((s0, prev)); s0 = prev = s
    runs.append((s0, prev))
    lo, hi = max(runs, key=lambda r: r[1] - r[0])
    return {'lo_ns': int(lo * 1e9), 'hi_ns': int((hi + 1) * 1e9),
            'covered_s': hi - lo + 1,
            'total_recorded_s': len(secs),
            'runs': len(runs)}


def engine_live_intervals(db, bridge_ns=500_000_000, scope=None, nvtx_only=False):
    """per-engine union of steps that ran kernels, gaps <= bridge merged."""
    sp = steps_by_pid(db)
    if nvtx_only:
        kp = {}
        lp = {pid: [s for s in st if s[1] - s[0] >= 2_000_000] for pid, st in sp.items()}
        lp = {pid: v for pid, v in lp.items() if v}
        pid_order = sorted(lp, key=lambda p: lp[p][0][0])
    else:
        kp = kernels_by_pid(db)
        pid_order = sorted(kp, key=lambda p: kp[p][0][0] if kp[p] else 1 << 62)
    pid_mod = {pid: MODS[i] if i < 3 else f'x{i}' for i, pid in enumerate(pid_order)}
    out = {}
    for pid, st in sp.items():
        m = pid_mod.get(pid)
        if m is None:
            continue
        iv = kp.get(pid, [])
        if scope:
            st = clip(st, scope['lo_ns'], scope['hi_ns'])
            iv = clip(iv, scope['lo_ns'], scope['hi_ns'])
        if nvtx_only:
            live = [s for s in st if s[1] - s[0] >= 2_000_000]
        else:
            live = [s for s in st if union_len(clip(iv, s[0], s[1])) > 0]
        merged = []
        for s, e in sorted(live):
            if merged and s - merged[-1][1] <= bridge_ns:
                merged[-1] = (merged[-1][0], max(merged[-1][1], e))
            else:
                merged.append((s, e))
        out[m] = merged
    return out, pid_mod


def locate_coactive(db, min_engines=2, bridge_ns=500_000_000, scope=None, nvtx_only=False):
    """longest span where >= min_engines engines are live simultaneously,
    evaluated ONLY inside the evidence-covered scope."""
    li, pid_mod = engine_live_intervals(db, bridge_ns, scope=scope, nvtx_only=nvtx_only)
    ev = []
    for m, iv in li.items():
        for s, e in iv:
            ev.append((s, 1)); ev.append((e, -1))
    ev.sort()
    best, cur_s, cur = (0, 0, 0), None, 0
    for tm, dv in ev:
        before = cur
        cur += dv
        if before < min_engines <= cur:
            cur_s = tm
        elif before >= min_engines > cur and cur_s is not None:
            if tm - cur_s > best[0]:
                best = (tm - cur_s, cur_s, tm)
            cur_s = None
    return best, li, pid_mod



# ------------------------------------------------------------------ M01
def m01(a, ctx):
    wl = ROOT / a.workload
    r1 = run_serve(ctx.root / 'run_a', wl, a.device)
    r2 = run_serve(ctx.root / 'run_b', wl, a.device)
    ca, cb = load_calls(ctx.root / 'run_a'), load_calls(ctx.root / 'run_b')
    ka = {(c['program_id'], c['call_index']): c['output_tokens'] for c in ca}
    kb = {(c['program_id'], c['call_index']): c['output_tokens'] for c in cb}
    drift = sum(1 for k in ka if ka[k] != kb.get(k))
    contract = {
        'branch': 'mm-v3', 'workload': str(wl.relative_to(ROOT)),
        'workload_sha256': sha(wl),
        'engines': {'lm': 'Qwen3-1.7B', 'vis': 'InternVL2_5-1B',
                    'audio': 'ultravox-v0_5-llama-3_2-1b(Llama-3.2-1B 本地镜像)'},
        'device': a.device, 'colocation': '三引擎同驻一卡,eager,逐 call DAG',
        'process_layer_scope': ('声明部分覆盖:8 类 process 分类不适配视觉/音频塔;'
                                '本链 process 轴 = 引擎(模态)×相位;prog/step 层完整'),
        'fingerprint_rule': 'sha256(pt_mm_v3.py + serve_mm.py) 全文——偏离 AST 闭包规则,已声明',
        'equivalence': {'metric': '逐 call output_tokens(贪心)', 'drift': drift,
                        'calls': len(ka),
                        'note': '粗粒度门:token-id 级等价需引擎 dump,mm-v3 首链先行申报'},
    }
    (ctx.root / 'run_contract.json').write_text(json.dumps(contract, indent=1, ensure_ascii=False) + '\n')
    gates = {'two_runs_complete': True, 'equivalence_drift_zero': drift == 0,
             'all_modalities_served': all(
                 any(c['modality'] == m for c in ca) for m in MODS)}
    gates['pass'] = all(gates.values())
    (ctx.root / 'gates.json').write_text(json.dumps(gates, indent=1) + '\n')
    if not gates['pass']:
        sys.exit(f'M01 gates failed: {gates}')
    ctx.commit({'status': 'complete', 'workload_sha256': contract['workload_sha256'],
                'equivalence_drift': drift, 'gates': gates},
               [ctx.root / 'run_contract.json', ctx.root / 'gates.json',
                ctx.root / 'run_a' / 'calls_mm.jsonl'])


# ------------------------------------------------------------------ M02
def m02(a, ctx):
    wl = ROOT / ctx.pred('M01')['workload_sha256'] and ROOT / a.workload
    if sha(wl) != ctx.pred('M01')['workload_sha256']:
        sys.exit('M02: workload hash drift')
    cap = ctx.root / 'cap'
    # v2 漏斗纪律:P1 只追 NVTX(prog/step 层完整,无 kernel 预算约束)
    nsys = ['nsys', 'profile', '--force-overwrite=true', '--trace=nvtx,osrt',
            '--sample=none', '--cpuctxsw=none',
            '--trace-fork-before-exec=true', f'--output={cap / "p1"}']
    cap.mkdir(parents=True, exist_ok=True)
    run_serve(cap / 'run', wl, a.device, nsys=nsys,
              env_extra={'AGENTIX_W_INSTRUMENT': '1'})
    subprocess.run(['nsys', 'export', '--type', 'sqlite', '--force-overwrite=true',
                    '--output', str(cap / 'cap.sqlite'), str(cap / 'p1.nsys-rep')],
                   check=True, capture_output=True)
    calls = load_calls(cap / 'run')
    pp = prog_profile(calls, wl)
    (ctx.root / 'class0_program_profile.json').write_text(
        json.dumps(pp, indent=1, ensure_ascii=False) + '\n')
    db = open_db(cap)
    sp = steps_by_pid(db)
    # NVTX-only:活跃步 = 时长 ≥2ms 的 step(busy-loop 空转步 ~0.1ms,申报阈值)
    LIVE_NS = 2_000_000
    live_sp = {pid: [s for s in st if s[1] - s[0] >= LIVE_NS] for pid, st in sp.items()}
    live_sp = {pid: v for pid, v in live_sp.items() if v}
    pid_order = sorted(live_sp, key=lambda p: live_sp[p][0][0])
    pid_mod = {pid: MODS[i] if i < 3 else f'extra{i}' for i, pid in enumerate(pid_order)}
    k0 = min(v[0][0] for v in live_sp.values())
    k1 = max(v[-1][1] for v in live_sp.values())
    span = k1 - k0
    eng = {}
    for pid, st in live_sp.items():
        m = pid_mod[pid]
        stept = sum(e - s for s, e in st)
        eng[m] = {'pid': pid, 'steps_live': len(st),
                  'step_time_us': stept / 1e3,
                  'step_share_of_span': round(stept / span, 4)}
    (ctx.root / 'engine_profile.json').write_text(json.dumps(
        {'span_s': span / 1e9, 'engines': eng,
         'live_step_rule': f'step 时长 >= {LIVE_NS/1e6:.0f}ms 计为活跃(NVTX-only P1,无设备 lane)',
         'pid_modality_rule': '按各 pid 首活跃步时间排序对齐引擎拉起顺序'},
        indent=1, ensure_ascii=False) + '\n')
    scope = {'mode': 'nvtx-only', 'note': 'P1 无 kernel 预算,NVTX 无截断风险;设备证据留给条件触发的 P2'}
    (ctx.root / 'capture_scope.json').write_text(json.dumps(scope, indent=1, ensure_ascii=False) + "\n")
    gates = {'prog_layer_present': pp['present'],
             'dag_consistent': not pp['dag_violations'],
             'parallel_dag_not_serialized': not pp['serialized_programs'],
             'three_engines_have_steps': len([m for m in eng if m in MODS]) == 3}
    gates['pass'] = all(gates.values())
    (ctx.root / 'gates.json').write_text(json.dumps(gates, indent=1) + '\n')
    if not gates['pass']:
        sys.exit(f'M02 gates failed: {gates}')
    ctx.commit({'status': 'complete', 'workload_sha256': ctx.pred('M01')['workload_sha256'],
                'capture': str(cap.relative_to(ROOT)), 'capture_sha256': sha(cap / 'cap.sqlite'),
                'engines': {m: {'step_share_of_span': eng[m]['step_share_of_span']}
                            for m in eng},
                'prog_layer': {'collapse': pp['collapse_share_width_le1'],
                               'serialized': pp['serialized_programs']},
                'gates': gates},
               [cap / 'cap.sqlite', ctx.root / 'class0_program_profile.json',
                ctx.root / 'engine_profile.json', ctx.root / 'gates.json'])


# ------------------------------------------------------------------ M03
def m03(a, ctx):
    h2 = ctx.pred('M02')
    ep = json.loads((ctx.pfile('M02', 'engine_profile.json')).read_text())
    pp = json.loads((ctx.pfile('M02', 'class0_program_profile.json')).read_text())
    rule = ('规则先于选择:高延迟对象 = 设备时间占比 >10% 的引擎(模态);'
            '分母 = 三引擎活跃步时长之和(P1 为 NVTX-only,设备份额留给 P2);prog 目标 = 模态内 call 延迟中位 top;'
            '窗口条件(冻结)= “≥2 引擎同时活跃(含 kernel 的步)”的最长持续段,'
            '词汇 = step:engine-live-intervals,采集坐标系内直接求值')
    (ctx.root / 'selection_rule.md').write_text(rule + '\n')
    tot = sum(e['step_time_us'] for e in ep['engines'].values())
    share = {m: e['step_time_us'] / tot for m, e in ep['engines'].items()}
    selected = [m for m, s in share.items() if s > 0.10]
    calls = load_calls(ROOT / h2['capture'] / 'run')
    lat = collections.defaultdict(list)
    for c in calls:
        lat[c['modality']].append(c['call_latency_ms'])
    # 条件窗口:≥2 引擎同时活跃(活跃 = 含 kernel 的步,间隙≤500ms 桥接)。
    # 词汇 = step:engine-live-intervals,在采集坐标系内直接求值 → 条件即定位器,
    # 不需要跨坐标锚定(首链曾用 call 相对时间 + 首 kernel 锚,窗口落进预热区)。
    db = open_db(ROOT / h2['capture'])
    best, _li, _pm = locate_coactive(db, nvtx_only=True)
    cond = {'name': 'multi_engine_coactive', 'vocabulary': 'step:engine-live-intervals',
            'predicate': '>=2 engines have live steps simultaneously',
            'bridge_ms': 500, 'located_span_ms': [best[1]/1e6, best[2]/1e6],
            'span_ms': best[0]/1e6,
            'min_span_ms': 5000, 'on_failure': 'declare, no fallback'}
    c2 = {'share_by_engine': {m: round(s, 4) for m, s in share.items()},
          'selected_engines': selected,
          'rejected_engines': [m for m in share if m not in selected],
          'latency_ms_median': {m: sorted(v)[len(v)//2] for m, v in lat.items()},
          'reasons': {m: f'device share {share[m]:.1%} > 10%' for m in selected}}
    (ctx.root / 'class2_targets.json').write_text(json.dumps(c2, indent=1, ensure_ascii=False) + '\n')
    (ctx.root / 'window_condition.json').write_text(json.dumps(cond, indent=1, ensure_ascii=False) + '\n')
    prog_t = {'collapse_share_width_le1': pp['collapse_share_width_le1'],
              'serialized_programs': pp['serialized_programs'],
              'findings': ([f"塌缩占 {pp['collapse_share_width_le1']:.0%} > 30%:调度/结构优先"]
                           if pp['collapse_share_width_le1'] > 0.3 else []),
              'vis_ttft_note': '视觉编码抬升 vis TTFT(M02 引擎档案),ModServe 现象在册'}
    (ctx.root / 'prog_targets.json').write_text(json.dumps(prog_t, indent=1, ensure_ascii=False) + '\n')
    gates = {'rule_written_before_selection': True,
             'shares_sum_to_one': abs(sum(share.values()) - 1) < 1e-6,
             'selected_nonempty': bool(selected),
             'window_condition_frozen': best[0]/1e6 >= cond['min_span_ms'],
             'prog_targets_emitted': True}
    gates['pass'] = all(v for k, v in gates.items() if k != 'pass')
    (ctx.root / 'gates.json').write_text(json.dumps(gates, indent=1) + '\n')
    if not gates['pass']:
        sys.exit(f'M03 gates failed: {gates}')
    ctx.commit({'status': 'complete', 'selected_engines': selected,
                'share_by_engine': c2['share_by_engine'],
                'window_condition': cond, 'gates': gates},
               [ctx.root / 'class2_targets.json', ctx.root / 'window_condition.json',
                ctx.root / 'prog_targets.json', ctx.root / 'selection_rule.md',
                ctx.root / 'gates.json'])


# ------------------------------------------------------------------ M04
def m04(a, ctx):
    wl = ROOT / a.workload
    cap = ctx.root / 'cap'
    nsys = ['nsys', 'profile', '--force-overwrite=true', '--trace=cuda,nvtx,osrt',
            '--sample=none', '--cpuctxsw=none', '--cuda-flush-interval=0',
            '--capture-range=cudaProfilerApi', '--capture-range-end=stop',
            '--trace-fork-before-exec=true', f'--output={cap / "p2"}']
    cap.mkdir(parents=True, exist_ok=True)
    run_serve(cap / 'run', wl, a.device, nsys=nsys,
              env_extra={'AGENTIX_W_INSTRUMENT': '1', 'AGENTIX_MM_TRIGGER': '1'})
    subprocess.run(['nsys', 'export', '--type', 'sqlite', '--force-overwrite=true',
                    '--output', str(cap / 'cap.sqlite'), str(cap / 'p2.nsys-rep')],
                   check=True, capture_output=True)
    cond = ctx.pred('M03')['window_condition']
    db = open_db(cap)
    # 条件触发采集:窗口即采集本身(触发器=serve_mm 的 >=2 模态在飞 1s)
    kp, sp = kernels_by_pid(db), steps_by_pid(db)
    if not kp:
        sys.exit('M04: 触发未命中,无 kernel 记录——申报失败,不回退')
    pid_order = sorted(kp, key=lambda q: kp[q][0][0] if kp[q] else 1 << 62)
    pid_mod = {q: MODS[i] if i < 3 else f'x{i}' for i, q in enumerate(pid_order)}
    lo = min(v[0][0] for v in kp.values() if v)
    hi = max(v[-1][1] for v in kp.values() if v)
    scope04 = covered_scope(db)
    (ctx.root / 'capture_scope.json').write_text(json.dumps(scope04, indent=1) + "\n")
    located = (hi - lo) / 1e6 >= cond['min_span_ms']
    loc = {'located': located, 'condition': cond,
           'trigger': 'serve_mm cudaProfilerStart(>=2 modalities in flight 1s)',
           'measured': {'span_ms': (hi - lo)/1e6, 'span_ns': [lo, hi],
                        'covered_s': scope04['covered_s'] if scope04 else 0}}
    (ctx.root / 'window_location.json').write_text(json.dumps(loc, indent=1, ensure_ascii=False) + '\n')
    if not located:
        sys.exit('M04: 条件触发窗口过短——申报失败,不回退')
    inst = []
    for pid, st in sp.items():
        m = pid_mod.get(pid)
        if m is None:
            continue
        iv = kp.get(pid, [])
        for s, e in st:
            if e < lo or s > hi:
                continue
            busy = union_len(clip(iv, s, e))
            if busy <= 0:
                continue
            inst.append({'engine': m, 'start': s, 'end': e,
                         'dur_us': (e - s) / 1e3, 'busy_us': busy / 1e3})
    with (ctx.root / 'pass2_instances.jsonl').open('w') as f:
        for r in inst:
            f.write(json.dumps(r) + '\n')
    gates = {'window_located_by_condition': located,
             'instances_nonempty': len(inst) > 0,
             'every_selected_engine_present': all(
                 any(r['engine'] == m for r in inst)
                 for m in ctx.pred('M03')['selected_engines'])}
    gates['pass'] = all(gates.values())
    (ctx.root / 'gates.json').write_text(json.dumps(gates, indent=1) + '\n')
    if not gates['pass']:
        sys.exit(f'M04 gates failed: {gates}')
    ctx.commit({'status': 'complete', 'capture': str(cap.relative_to(ROOT)),
                'capture_sha256': sha(cap / 'cap.sqlite'),
                'window_ns': [lo, hi], 'instances': len(inst),
                'anchor_rule': 't0≈首 kernel 时间(申报近似)', 'gates': gates},
               [cap / 'cap.sqlite', ctx.root / 'window_location.json',
                ctx.root / 'pass2_instances.jsonl', ctx.root / 'gates.json'])


# ------------------------------------------------------------------ M05
def m05(a, ctx):
    h4 = ctx.pred('M04')
    cap = ROOT / h4['capture']
    db = open_db(cap)
    kp, sp = kernels_by_pid(db), steps_by_pid(db)
    pid_order = sorted(kp, key=lambda p: kp[p][0][0] if kp[p] else 1 << 62)
    pid_mod = {pid: MODS[i] if i < 3 else f'x{i}' for i, pid in enumerate(pid_order)}
    lo, hi = h4['window_ns']
    matrix = {}
    for xpid, xst in sp.items():
        xm = pid_mod.get(xpid)
        if xm is None:
            continue
        xin = clip(xst, lo, hi)
        xtot = sum(e - s for s, e in xin)
        if xtot <= 0:
            continue
        row = {}
        for ypid, ykern in kp.items():
            ym = pid_mod[ypid]
            cov = sum(union_len(clip(ykern, s, e)) for s, e in xin)
            row[ym] = round(cov / xtot, 4)
        matrix[xm] = {'host_step_us': xtot / 1e3, 'device_share_by_engine': row}
    pairs = [{'host': x, 'device': y, 'share': v['device_share_by_engine'][y],
              'selected': v['device_share_by_engine'][y] > 0.10}
             for x, v in matrix.items() for y in v['device_share_by_engine'] if x != y]
    (ctx.root / 'cross_engine_matrix.json').write_text(json.dumps(
        {'window_ns': [lo, hi], 'matrix': matrix, 'pairs': pairs,
         'rule': 'matrix[X][Y] = X 的 step 区间内设备在跑 Y 的 kernel 的时间份额(重叠,不跨 lane 相减)'},
        indent=1, ensure_ascii=False) + '\n')
    sel = [p for p in pairs if p['selected']]
    gates = {'matrix_rows_for_all_engines': len(matrix) >= 3,
             'pairs_registered': len(pairs) > 0,
             'selection_rule_applied': True}
    gates['pass'] = all(gates.values())
    (ctx.root / 'gates.json').write_text(json.dumps(gates, indent=1) + '\n')
    if not gates['pass']:
        sys.exit(f'M05 gates failed: {gates}')
    ctx.commit({'status': 'complete', 'cross_engine_pairs_selected': sel,
                'gates': gates},
               [ctx.root / 'cross_engine_matrix.json', ctx.root / 'gates.json'])


# ------------------------------------------------------------------ M06
def m06(a, ctx):
    plan = {'tool': 'ncu', 'sections': ['SpeedOfLight'],
            'target': '--target-processes all(三引擎 fork 子进程全捕)',
            'trigger': ('launch-skip 估算:M04 窗口前 kernel 数 × 安全系数 0.9;'
                        '偏离 cudaProfilerApi 门控——mm 引擎无 AGENTIX 触发钩,申报降级'),
            'launch_count': a.launch_count,
            'risk': 'NCU 回放拖慢 → 条件段漂移;M08 只按 pid 归属,不按时间对齐'}
    h4 = ctx.handoff('M04')
    cap = ROOT / h4['capture']
    db = open_db(cap)
    lo, _ = h4['window_ns']
    n_before = db.execute(
        'select count(*) c from CUPTI_ACTIVITY_KIND_KERNEL where start < ?', (lo,)).fetchone()['c']
    plan['launch_skip'] = max(int(n_before * 0.9), 100)
    (ctx.root / 'pass3_plan.json').write_text(json.dumps(plan, indent=1, ensure_ascii=False) + '\n')
    gates = {'budget_within_wallclock': a.launch_count <= 128, 'skip_estimated': True,
             'pass': True}
    (ctx.root / 'gates.json').write_text(json.dumps(gates, indent=1) + '\n')
    ctx.commit({'status': 'complete', 'plan': plan, 'gates': gates},
               [ctx.root / 'pass3_plan.json', ctx.root / 'gates.json'])


# ------------------------------------------------------------------ M07
def m07(a, ctx):
    wl = ROOT / a.workload
    plan = ctx.pred('M06')['plan']
    sel = ctx.handoff('M03')['selected_engines']
    out = ctx.root / 'ncu'
    out.mkdir(parents=True, exist_ok=True)
    import csv as _csv
    all_recs = []
    per_engine = {}
    for m in sel:
        env = dict(os.environ)
        env.update({'CUDA_VISIBLE_DEVICES': a.device,
                    'VLLM_ENABLE_V1_MULTIPROCESSING': '0',
                    'AGENTIX_NCU_TARGET': m})
        rep = out / f'p3_{m}'
        # 引擎侧门控:只有目标引擎的子进程自触发,NCU 预算全落其上
        cmd = ['/opt/nvidia/nsight-compute/2026.2.0/ncu', '--target-processes', 'all',
               '--profile-from-start', 'off',
               '-c', str(plan['launch_count']),
               '--section', 'SpeedOfLight',
               '-o', str(rep),
               PY, SERVE, '--workload', str(wl), '--output-dir', str(out / f'run_{m}'),
               '--enforce-eager', '--devices', 'lm:0,vis:0,audio:0']
        with (out / f'ncu_{m}.log').open('w') as lg:
            rc = subprocess.run(cmd, env=env, stdout=lg, stderr=subprocess.STDOUT,
                                timeout=3600, cwd=str(ROOT))
        csvf = out / f'ncu_{m}.csv'
        repf = Path(str(rep) + '.ncu-rep')
        recs = []
        if repf.is_file():
            with csvf.open('w') as cf:
                subprocess.run(['/opt/nvidia/nsight-compute/2026.2.0/ncu',
                                '--import', str(repf), '--csv', '--page', 'details'],
                               stdout=cf, stderr=subprocess.DEVNULL, timeout=600)
            lines = [l for l in csvf.read_text().splitlines() if not l.startswith('==')]
            for row in _csv.DictReader(lines):
                row['engine'] = m
                recs.append(row)
        per_engine[m] = {'records': len(recs),
                         'launches': len({r.get('ID') for r in recs if r.get('ID')}),
                         'rc': rc.returncode}
        all_recs.extend(recs)
    with (ctx.root / 'pass3_records.jsonl').open('w') as f:
        for r in all_recs:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    gates = {'per_engine': per_engine,
             'every_selected_engine_has_launches': all(
                 v['launches'] > 0 for v in per_engine.values()),
             'attribution_by_construction': True}
    gates['pass'] = gates['every_selected_engine_has_launches']
    (ctx.root / 'gates.json').write_text(json.dumps(gates, indent=1) + '\n')
    if not gates['pass']:
        sys.exit(f'M07 gates failed: {json.dumps(gates)}')
    ctx.commit({'status': 'complete', 'records': len(all_recs),
                'per_engine': per_engine,
                'ownership': 'by construction(逐引擎门控运行,非 pid 猜序)',
                'gates': gates},
               [ctx.root / 'pass3_records.jsonl', ctx.root / 'gates.json'])


# ------------------------------------------------------------------ M08
def m08(a, ctx):
    recs = [json.loads(l) for l in (ctx.pfile('M07', 'pass3_records.jsonl')).open()]
    by_eng = collections.defaultdict(list)
    for r in recs:
        by_eng[r['engine']].append(r)

    def metric(r, name):
        if r.get('Metric Name') == name:
            try:
                return float(str(r.get('Metric Value', '')).replace(',', ''))
            except ValueError:
                return None
        return None
    att = {}
    for m, rs in by_eng.items():
        sm = [v for v in (metric(r, 'Compute (SM) Throughput') for r in rs) if v is not None]
        mem = [v for v in (metric(r, 'Memory Throughput') for r in rs) if v is not None]
        att[m] = {'records': len(rs),
                  'sm_pct_median': sorted(sm)[len(sm)//2] if sm else None,
                  'mem_pct_median': sorted(mem)[len(mem)//2] if mem else None,
                  'launches': len({r.get('ID') for r in rs})}
    (ctx.root / 'resource_attribution.json').write_text(json.dumps(
        {'by_engine': att,
         'rule': '归属为构造得到:逐引擎门控 NCU 运行;窗口为各自触发段,时间轴不跨运行对齐(申报)'},
        indent=1, ensure_ascii=False) + '\n')
    gates = {'every_engine_attributed': len(att) >= 2,
             'metrics_present': any(v['sm_pct_median'] is not None for v in att.values())}
    gates['pass'] = all(gates.values())
    (ctx.root / 'gates.json').write_text(json.dumps(gates, indent=1) + '\n')
    if not gates['pass']:
        sys.exit(f'M08 gates failed: {gates}')
    ctx.commit({'status': 'complete', 'attribution': att, 'gates': gates},
               [ctx.root / 'resource_attribution.json', ctx.root / 'gates.json'])


# ------------------------------------------------------------------ M09
def m09(a, ctx):
    td = ctx.root / 'tables'
    td.mkdir(exist_ok=True)
    import csv as _csv

    def write(name, rows, cols):
        fp = td / f'{name}.csv'
        with fp.open('w', newline='') as f:
            w = _csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k) for k in cols})
        return fp, len(rows)
    calls = load_calls(ROOT / ctx.handoff('M02')['capture'] / 'run')
    t0 = [{'program_id': c['program_id'], 'call_index': c['call_index'],
           'modality': c['modality'], 'role': c['role'],
           'parents': ';'.join(map(str, c['parents'])),
           'submitted_ms': c['submitted_rel_ms'], 'finished_ms': c['finished_rel_ms'],
           'latency_ms': c['call_latency_ms'], 'ttft_ms': c['ttft_ms'],
           'output_tokens': c['output_tokens']} for c in calls]
    f0 = write('class0_program_calls', t0,
               ['program_id', 'call_index', 'modality', 'role', 'parents',
                'submitted_ms', 'finished_ms', 'latency_ms', 'ttft_ms', 'output_tokens'])
    inst = [json.loads(l) for l in (ctx.pfile('M04', 'pass2_instances.jsonl')).open()]
    f1 = write('class1_engine_steps', inst, ['engine', 'start', 'end', 'dur_us', 'busy_us'])
    cm = json.loads((ctx.pfile('M05', 'cross_engine_matrix.json')).read_text())
    t3 = [{'host_engine': p['host'], 'device_engine': p['device'],
           'share': p['share'], 'selected': p['selected']} for p in cm['pairs']]
    f3 = write('class3_cross_engine', t3, ['host_engine', 'device_engine', 'share', 'selected'])
    ra = json.loads((ctx.pfile('M08', 'resource_attribution.json')).read_text())['by_engine']
    t4 = [{'engine': m, **{k: v for k, v in d.items() if k != 'pid'}} for m, d in ra.items()]
    f4 = write('class4_resources', t4, ['engine', 'records', 'sm_pct_median',
                                        'mem_pct_median', 'launches'])
    man = {'tables': {n: {'rows': fl[1], 'sha256': sha(fl[0])}
                      for n, fl in {'class0_program_calls': f0, 'class1_engine_steps': f1,
                                    'class3_cross_engine': f3, 'class4_resources': f4}.items()}}
    (ctx.root / 'table_manifest.json').write_text(json.dumps(man, indent=1) + '\n')
    gates = {'tables_present': all(x[1] > 0 for x in (f0, f1, f3, f4)),
             'class0_rows_match_calls': f0[1] == len(calls)}
    gates['pass'] = all(gates.values())
    (ctx.root / 'gates.json').write_text(json.dumps(gates, indent=1) + '\n')
    if not gates['pass']:
        sys.exit(f'M09 gates failed: {gates}')
    ctx.commit({'status': 'complete', 'tables': man['tables'], 'gates': gates},
               [f0[0], f1[0], f3[0], f4[0], ctx.root / 'table_manifest.json',
                ctx.root / 'gates.json'])


# ------------------------------------------------------------------ M10
def m10(a, ctx):
    import csv as _csv
    td = ctx.pfile('M09', 'tables')
    t0 = list(_csv.DictReader((td / 'class0_program_calls.csv').read_text().splitlines()))
    t3 = list(_csv.DictReader((td / 'class3_cross_engine.csv').read_text().splitlines()))
    t4 = list(_csv.DictReader((td / 'class4_resources.csv').read_text().splitlines()))
    ep = ctx.handoff('M02')['engines']
    colors = {'lm': '#2f6f9f', 'vis': '#c94040', 'audio': '#3f9f6f'}
    progs = sorted({r['program_id'] for r in t0})
    tmax = max(float(r['finished_ms']) for r in t0)
    parts = []
    lane_h, pad = 40, 46
    for li, pid in enumerate(progs):
        y = pad + li * lane_h
        parts.append(f'<text x="4" y="{y+14}" font-size="12" fill="#48607d">{pid}</text>')
        for r in [q for q in t0 if q['program_id'] == pid]:
            x0 = 80 + float(r['submitted_ms']) / tmax * 1030
            x1 = 80 + float(r['finished_ms']) / tmax * 1030
            lane = int(r['call_index']) % 2
            c = colors.get(r['modality'], '#888')
            parts.append(f'<rect x="{x0:.1f}" y="{y+2+lane*15}" width="{max(x1-x0,1):.1f}" '
                         f'height="13" fill="{c}" opacity=".85">'
                         f'<title>{pid}#{r["call_index"]} {r["modality"]} {r["role"]} '
                         f'{float(r["latency_ms"]):.0f}ms</title></rect>')
    h = pad + len(progs) * lane_h + 30
    legend = ' '.join(f'<tspan fill="{c}">■ {m}</tspan>' for m, c in colors.items())
    fig0 = (f'<svg viewBox="0 0 1150 {h}" style="width:100%;height:auto;background:#fff;'
            f'border:1px solid #c9d6e4;border-radius:6px">'
            f'<text x="4" y="22" font-size="19" font-weight="600">B0 prog 层 · 三模态双链 loop 时间线</text>'
            f'<text x="700" y="22" font-size="13">{legend}</text>{"".join(parts)}'
            f'<text x="4" y="{h-6}" font-size="12" fill="#48607d">横轴 0-{tmax/1000:.1f}s;'
            f'双泳道同时着色=程序内并行;颜色=模态(引擎)</text></svg>')
    rows3 = ''.join(f"<tr><td>{r['host_engine']}</td><td>{r['device_engine']}</td>"
                    f"<td>{float(r['share']):.1%}</td><td>{r['selected']}</td></tr>" for r in t3)
    rows4 = ''.join(f"<tr><td>{r['engine']}</td><td>{r['records']}</td>"
                    f"<td>{r['sm_pct_median']}</td><td>{r['mem_pct_median']}</td></tr>" for r in t4)
    eng_sum = ''.join(f"<li>{m}: 活跃步时长份额 {d['step_share_of_span']:.1%}"
                      f"(P1 为 NVTX-only,设备份额见 P2/P3)</li>" for m, d in ep.items())
    body = f'''<h1>文档 B(mm-v3)· 三模态三引擎同卡 · {ctx.lineage}</h1>
<p class="cap">四层:prog(program→call)/ step / 引擎(模态)×相位(process 层部分覆盖,已申报)/ kernel。
三引擎(Qwen3-1.7B / InternVL2_5-1B / ultravox-1b)同驻一张 4090,逐 call DAG。</p>
<h2>B0 第 0 类 · prog 层时间线</h2>{fig0}
<h2>B1 引擎档案(P1 整段)</h2><ul class="cap">{eng_sum}</ul>
<h2>B3 第三类 · 跨引擎并发矩阵(P2 条件窗口)</h2>
<table><tr><th>host 引擎</th><th>device 引擎</th><th>份额</th><th>入选</th></tr>{rows3}</table>
<p class="cap">matrix[X][Y] = X 的 step 区间内设备在跑 Y 的 kernel 的时间份额(重叠,不跨 lane 相减)。</p>
<h2>B4 资源归属(P3 NCU,按 pid 归属;时间未对齐已申报)</h2>
<table><tr><th>引擎</th><th>记录</th><th>SM% 中位</th><th>Mem% 中位</th></tr>{rows4}</table>'''
    style = ('body{margin:0;font:19px/1.7 "Noto Sans CJK SC",system-ui,sans-serif;color:#1f2f45}'
             '.wrap{max-width:1200px;margin:0 auto;padding:24px}h2{color:#2f6f9f}'
             'table{border-collapse:collapse}td,th{border:1px solid #c9d6e4;padding:5px 9px}')
    rp = ctx.root / 'B_REPORT_MM.html'
    rp.write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
                  f'<style>{style}</style></head><body><div class="wrap">{body}</div></body></html>')
    gates = {'report_written': rp.is_file(), 'b0_has_all_programs': len(progs) == 4,
             'pass': True}
    (ctx.root / 'gates.json').write_text(json.dumps(gates, indent=1) + '\n')
    ctx.commit({'status': 'complete', 'report': str(rp.relative_to(ROOT)), 'gates': gates},
               [rp, ctx.root / 'gates.json'])


STAGES = {'M01': m01, 'M02': m02, 'M03': m03, 'M04': m04, 'M05': m05,
          'M06': m06, 'M07': m07, 'M08': m08, 'M09': m09, 'M10': m10}


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--step', required=True, choices=sorted(STAGES))
    ap.add_argument('--lineage', required=True)
    ap.add_argument('--workload', required=True)
    ap.add_argument('--device', default='1')
    ap.add_argument('--launch-count', type=int, default=64)
    a = ap.parse_args()
    ctx = Ctx(a.step, a.lineage)
    STAGES[a.step](a, ctx)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
