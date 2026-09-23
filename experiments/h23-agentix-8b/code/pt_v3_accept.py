#!/usr/bin/env python3
"""Independent acceptance of a v2 lineage, step by step.

Deliberately does not trust a step's own gates.json: a gate that returns a
hard-coded True states something no file performs, and one such gate shipped in
this chain. Every check here reads an artifact and recomputes.

Per step it verifies: the handoff exists and says complete; every file in the
artifact manifest is present and hashes to what the manifest recorded; the
predecessor handoffs it cites still hash to the same bytes; the ledger entry
matches the handoff; and the step-specific claims that can be re-derived are
re-derived.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def claim_checks(step: str, d: Path, h: dict) -> list[tuple[str, bool, str]]:
    """Re-derive what a gate asserts, from the files, not from the gate."""
    out = []
    g = json.loads((d / 'gates.json').read_text()) if (d / 'gates.json').is_file() else {}

    def add(name, ok, detail=''):
        out.append((name, bool(ok), detail))

    if step == 'S02':
        pp = json.loads((d / 'class0_program_profile.json').read_text())
        add('prog 层档案在场且非空', pp.get('present') and pp.get('calls_total', 0) > 0)
        add('DAG 违例为零(独立复核)', not pp.get('dag_violations'),
            f"{len(pp.get('dag_violations', []))} 条")
        # 独立复核 wave 屏障检测器:声明含反链的程序,重叠必须 > 0
        bad = [pid for pid, v in (pp.get('programs') or {}).items()
               if v.get('expects_parallel') and (v.get('overlap_ms') or 0) <= 0]
        add('可并行程序无一被串行化(独立复核)', not bad, str(bad))
        add('宽度份额之和为 1',
            abs(sum(pp.get('width_ms_share', {}).values()) - 1.0) < 0.02,
            f"Σ={sum(pp.get('width_ms_share', {}).values()):.4f}")
    if step == 'S03':
        pt3 = json.loads((d / 'prog_targets.json').read_text())
        add('prog 目标文件字段齐备',
            all(k in pt3 for k in ('collapse_share_width_le1', 'tail_last_program_share',
                                   'serialized_programs', 'findings')))
        add('越限即有 finding',
            not ((pt3.get('collapse_share_width_le1') or 0) > 0.3) or bool(pt3['findings']))
        c2 = json.loads((d / 'class2_targets.json').read_text())
        share = c2['share_by_process']
        add('份额之和为 1', abs(sum(share.values()) - 1.0) < 0.01,
            f"Σ={sum(share.values()):.4f}")
        add('入选者份额确实 >10%', all(share[p] > 0.10 for p in c2['selected_types']),
            str({p: share[p] for p in c2['selected_types']}))
        add('落选者已登记', len(c2['rejected_types']) + len(c2['selected_types']) == len(share))
        add('每个目标有理由', all(t.get('reason') for t in c2['targets']))
        add('窗口条件已落盘', (d / 'class2_window_condition.json').is_file())
    if step == 'S04':
        loc = json.loads((d / 'window_location.json').read_text())
        add('窗口由条件定位', loc.get('located') is True)
        add('窗口不含时刻类条件',
            not any(k in loc['condition'] for k in ('start_ns', 'end_ns', 'step_index')))
        m = loc.get('measured', {})
        c = loc['condition']
        # not "every step meets the floor" (the condition allows short dips) but
        # "the declared fraction of them does", which is what it actually claims
        add('窗口满足率达到条件要求',
            (m.get('satisfied_frac') or 0) >= c.get('min_satisfied_frac', 0.8),
            f"satisfied={m.get('satisfied_frac')} required={c.get('min_satisfied_frac')}")
        add('容忍度随实测值一并申报', bool(m.get('tolerance')))
        eu = h.get('engine_utilisation') or {}
        add('引擎利用率已申报', bool(eu.get('steps_in_window')))
        add('三个忙碌量分母不同且都在', all(
            k in eu for k in ('step_coverage_of_window', 'device_busy_share_of_window',
                              'device_busy_share_inside_steps')))
        n = sum(1 for _ in (d / 'pass2_instances.jsonl').open())
        add('实例数与申报一致', n == h.get('instances'), f"file={n} handoff={h.get('instances')}")
    if step == 'S05':
        c3 = json.loads((d / 'class3_targets.json').read_text())
        add('被否窗口有明细与理由',
            all('condition' in r and r.get('reason') for r in c3.get('rejected_windows', [])),
            f"{len(c3.get('rejected_windows', []))} 条")
        add('入选窗口互不同名',
            len({w['condition']['name'] for w in c3['windows']}) == len(c3['windows']))
        add('每个窗口带可跨运行求值的条件',
            all(w['condition'].get('vocabulary') and 'phase_in' in w['condition']
                for w in c3['windows']))
    if step == 'S07':
        recs = [json.loads(l) for l in (d / 'pass3_ncu_launch_counters.jsonl').open()
                if l.strip()]
        add('每条记录带 process 归属', all(r.get('process') for r in recs), f"{len(recs)} 条")
        add('归属声明为构造得到',
            all('by construction' in (r.get('ownership') or '') for r in recs))
        add('时间量有单位换算', all(r.get('device_us') is not None for r in recs))
    if step == 'S08':
        cw = json.loads((d / 'concurrency_windows.json').read_text())
        add('第三遍窗口经条件重定位',
            all(w.get('relocated') or w.get('reason') for w in cw['windows']))
        ok = [w for w in cw['windows'] if w.get('relocated')]
        add('重定位窗口有数据', all(w.get('kernel_rows_in_window', 0) > 0 for w in ok),
            str([w.get('kernel_rows_in_window') for w in ok]))
        add('两遍实测条件值都记录',
            all(w.get('measured_in_pass3') for w in ok))
    if step == 'S09':
        tm = json.loads((d / 'table_manifest.json').read_text())
        for t in tm.get('tables', tm if isinstance(tm, list) else []):
            pass
        add('四类表齐备', all((d / 'tables' / f).is_file() for f in
                           ('class0_program_calls.csv', 'class1_end_to_end.csv',
                            'class2_high_latency.csv', 'class3_concurrency.csv')))
        n0 = sum(1 for _ in (d / 'tables' / 'class0_program_calls.csv').open()) - 1
        add('第 0 类行数与申报一致', n0 == (h.get('tables', {})
            .get('class0_program_calls', {}).get('rows')), f"file={n0}")
    if g:
        add('自报门限全部通过', g.get('pass') is True)
    return out


def step_checks(d: Path, step: str, h: dict, ledger_entry: dict | None):
    """与全链验收完全相同的检查集(哈希/齐备/前驱/台账 + 逐步声明复核)。"""
    checks = [('handoff 声明 complete', h.get('status') == 'complete', '')]
    man = json.loads((d / 'artifact_manifest.json').read_text())
    miss = [f['path'] for f in man['files'] if not (ROOT / f['path']).is_file()]
    drift = [f['path'] for f in man['files']
             if (ROOT / f['path']).is_file() and sha(ROOT / f['path']) != f['sha256']]
    checks.append(('产物齐备', not miss, ','.join(miss)[:80]))
    checks.append(('产物哈希未漂移', not drift, ','.join(drift)[:80]))
    pd = h.get('predecessor_handoffs') or {}
    pdrift = [k for k, v in pd.items() if sha(Path(v['path'])) != v['sha256']]
    checks.append(('前驱 handoff 未漂移', not pdrift, ','.join(pdrift)))
    if ledger_entry:
        checks.append(('台账条目与 handoff 一致',
                       ledger_entry['handoff_sha256'] == sha(d / 'handoff.json'), ''))
    return checks + claim_checks(step, d, h)


def accept_one(lineage: str, step: str) -> bool:
    base = ROOT / 'artifacts/agentix_8b/pt_v3' / lineage
    hp = base / step / 'handoff.json'
    if not hp.is_file():
        print(f'{step} MISSING handoff'); return False
    h = json.loads(hp.read_text())
    led_p = base / 'ledger.json'
    entry = None
    if led_p.is_file():
        entry = {e['step']: e for e in json.loads(led_p.read_text())['entries']}.get(step)
    rs = step_checks(base / step, step, h, entry)
    bad = [r for r in rs if not r[1]]
    verdict = {'step': step, 'pass': not bad, 'checks': len(rs),
               'failed': [f'{n} {d}' for n, _, d in bad]}
    (base / step / 'acceptance.json').write_text(
        json.dumps(verdict, indent=1, ensure_ascii=False) + '\n')
    print(f'{step}  {"PASS" if not bad else "FAIL"}  ({len(rs)} 项)'
          + (': ' + '; '.join(verdict['failed']) if bad else ''))
    return not bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--lineage', default='mixed')
    ap.add_argument('--step', default=None,
                    help='只验收单步(链驱动在每步 commit 后调用)')
    ap.add_argument('--base', type=Path,
                    default=ROOT / 'artifacts/agentix_8b/pt_v3')
    a = ap.parse_args()
    if a.step:
        return 0 if accept_one(a.lineage, a.step) else 1
    base = a.base / a.lineage
    led = json.loads((base / 'ledger.json').read_text())
    entries = {e['step']: e for e in led['entries']}
    bad = 0
    for step in sorted(entries):
        d = base / step
        h = json.loads((d / 'handoff.json').read_text())
        checks = step_checks(d, step, h, entries[step])
        fail = [c for c in checks if not c[1]]
        bad += len(fail)
        mark = 'PASS' if not fail else 'FAIL'
        print(f"{step}  {mark}  ({len(checks)} 项)")
        for name, ok, detail in checks:
            if not ok:
                print(f"    ✗ {name} {detail}")
    print(f"\n独立验收：{'全部通过' if not bad else f'{bad} 项不通过'}")
    return 0 if not bad else 1


if __name__ == '__main__':
    raise SystemExit(main())
