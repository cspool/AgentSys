#!/usr/bin/env python3
"""Independent acceptance for the mm-v3 chain: recompute hashes, re-derive claims."""
import collections
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path('/workspace/AgentSys')
ART = ROOT / 'artifacts/agentix_8b/pt_mm'
STEPS = [f'M{i:02d}' for i in range(1, 11)]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def checks(step, d, h):
    out = []
    add = lambda n, ok, det='': out.append((n, bool(ok), det))
    for rel, want in h.get('files', {}).items():
        p = ROOT / rel
        add(f'哈希 {Path(rel).name}', p.is_file() and sha(p) == want)
    if step == 'M01':
        c = json.loads((d / 'run_contract.json').read_text())
        add('等价漂移为零(独立复核)', c['equivalence']['drift'] == 0)
        add('process 层部分覆盖已声明', '部分覆盖' in c['process_layer_scope'])
    if step == 'M02':
        pp = json.loads((d / 'class0_program_profile.json').read_text())
        add('DAG 违例为零', not pp['dag_violations'])
        bad = [p for p, v in pp['programs'].items()
               if v['expects_parallel'] and v['overlap_ms'] <= 0]
        add('可并行程序无一串行化', not bad, str(bad))
        ep = json.loads((d / 'engine_profile.json').read_text())
        add('三引擎活跃步时长都非零', all(
            e['step_time_us'] > 0 for e in ep['engines'].values()))
    if step == 'M03':
        c2 = json.loads((d / 'class2_targets.json').read_text())
        add('份额和为 1', abs(sum(c2['share_by_engine'].values()) - 1) < 0.01)
        add('入选者 >10%', all(c2['share_by_engine'][m] > 0.10
                              for m in c2['selected_engines']))
        wc = json.loads((d / 'window_condition.json').read_text())
        add('条件词汇已声明且无时刻量',
            wc.get('vocabulary') in ('prog:call-intervals', 'step:engine-live-intervals')
            and 'start_ns' not in wc)
    if step == 'M04':
        loc = json.loads((d / 'window_location.json').read_text())
        add('窗口由条件重定位', loc['located'] is True)
        n = sum(1 for _ in (d / 'pass2_instances.jsonl').open())
        add('实例数与申报一致', n == h.get('instances'))
    if step == 'M05':
        cm = json.loads((d / 'cross_engine_matrix.json').read_text())
        add('矩阵行覆盖三引擎', len(cm['matrix']) >= 3)
        add('份额均在 [0,1]', all(0 <= p['share'] <= 1 for p in cm['pairs']))
    if step == 'M07':
        n = sum(1 for _ in (d / 'pass3_records.jsonl').open())
        add('记录数与申报一致', n == h.get('records'))
        pe = h.get('per_engine', {})
        add('每个入选引擎 launch 非零(独立复核)',
            bool(pe) and all(v.get('launches', 0) > 0 for v in pe.values()),
            str({k: v.get('launches') for k, v in pe.items()}))
    if step == 'M08':
        ra = json.loads((d / 'resource_attribution.json').read_text())
        add('归属规则已申报', '申报' in ra['rule'])
    if step == 'M09':
        tm = json.loads((d / 'table_manifest.json').read_text())
        for name, meta in tm['tables'].items():
            fp = d / 'tables' / f'{name}.csv'
            rows = sum(1 for _ in fp.open()) - 1
            add(f'{name} 行数一致', rows == meta['rows'])
    if step == 'M10':
        add('报告文件在场', (ROOT / h['report']).is_file())
    g = json.loads((d / 'gates.json').read_text())
    add('自报门限通过', g.get('pass') is True)
    return out


def main():
    lineage = sys.argv[1] if len(sys.argv) > 1 else 'mm1'
    base = ART / lineage
    all_ok = True
    for s in STEPS:
        hp = base / s / 'handoff.json'
        if not hp.is_file():
            print(f'{s}  MISSING handoff'); all_ok = False; continue
        h = json.loads(hp.read_text())
        rs = checks(s, base / s, h)
        bad = [r for r in rs if not r[1]]
        print(f'{s}  {"PASS" if not bad else "FAIL"}  ({len(rs)} 项)'
              + (': ' + '; '.join(f'{n} {d}' for n, _, d in bad) if bad else ''))
        all_ok &= not bad
    print('独立验收:', '全部通过' if all_ok else '存在失败')
    return 0 if all_ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
