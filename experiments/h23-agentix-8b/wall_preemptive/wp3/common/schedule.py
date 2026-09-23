"""相位锁定事件表。

设计要点: 臂之间**只有**"事件落在哪个相位"不同。
  - 事件数 K 逐字相同
  - 每个 epoch-pair 的偏移多重集恒为 slot_offsets_ms
  - 总 BURST 时长相同 => duty 相同
因此无需任何 deferral 记账, 不存在 forced 事件, 不存在事件叠压,
"等功"由构造保证而非事后配平。
"""
from __future__ import annotations
import random
from dataclasses import dataclass, asdict

DRAM, TC = 0, 1

@dataclass
class Event:
    idx: int
    pair_idx: int
    epoch_kind: int        # 0=DRAM 相, 1=TC 相
    offset_ms: int
    t_fire_rel_ms: float   # 相对窗口起点
    t_end_rel_ms: float
    level: str             # "BURST"

def build(*, n_pairs: int, alpha: float = 1.0, phase_ms: int = 600,
          guard_ms: int = 80, slot_offsets_ms=(100, 230, 360, 490),
          burst_ms: int = 90, seed: int = 0, mode: str = "alpha",
          orthogonal_phase: int = DRAM) -> list[Event]:
    """orthogonal_phase: wall-aware 认为"该在此相位下手"的那个相位。
    alpha = 事件落在 orthogonal_phase 的比例。
    mode: alpha | pack_random | poisson | noop
    """
    rng = random.Random(seed)
    slots = list(slot_offsets_ms)
    _PACK = [DRAM] * (n_pairs // 2) + [TC] * (n_pairs - n_pairs // 2)
    rng.shuffle(_PACK)
    assert all(o >= guard_ms for o in slots), "偏移必须大于护带"
    assert max(slots) + burst_ms <= phase_ms, "BURST 不能跨出 epoch"
    other = 1 - orthogonal_phase
    evs: list[Event] = []
    k = 0
    for p in range(n_pairs):
        pair_t0 = p * 2 * phase_ms          # pair 里第 0 个 epoch 是 DRAM 相
        if mode == "pack_random":
            # 构造性平衡: 一半 pair 整包落 DRAM 相, 一半整包落 TC 相, 顺序打乱。
            # 这样它与 a100 的**时间聚集结构完全相同**(4 个事件挤在同一 epoch),
            # 只有"挤在哪个相位"不同, 且 alpha 恰好 0.5 而不是靠抛硬币碰运气。
            kinds = [_PACK[p]] * len(slots)
        elif mode == "poisson":
            kinds = [rng.choice([DRAM, TC]) for _ in slots]
        else:  # alpha
            n_orth = round(alpha * len(slots))
            kinds = [orthogonal_phase] * n_orth + [other] * (len(slots) - n_orth)
            rng.shuffle(kinds)              # 偏移与相位的配对随机, 多重集不变
        for off, kind in zip(slots, kinds):
            base = pair_t0 + (0 if kind == DRAM else phase_ms)
            evs.append(Event(k, p, kind, off, base + off, base + off + burst_ms, "BURST"))
            k += 1
    evs.sort(key=lambda e: e.t_fire_rel_ms)
    _assert_invariants(evs, n_pairs, slots, burst_ms)
    return evs

def _assert_invariants(evs, n_pairs, slots, burst_ms):
    assert len(evs) == len(slots) * n_pairs, f"K 不对: {len(evs)}"
    for p in range(n_pairs):
        got = sorted(e.offset_ms for e in evs if e.pair_idx == p)
        assert got == sorted(slots), f"pair {p} 偏移多重集被破坏: {got}"
    tot = sum(e.t_end_rel_ms - e.t_fire_rel_ms for e in evs)
    assert abs(tot - len(evs) * burst_ms) < 1e-6, "总 BURST 时长不对"
    for a, b in zip(evs, evs[1:]):
        assert b.t_fire_rel_ms >= a.t_end_rel_ms - 1e-9, f"事件叠压: {a.idx}->{b.idx}"

def realized_alpha(evs, orthogonal_phase: int = DRAM) -> float:
    return sum(1 for e in evs if e.epoch_kind == orthogonal_phase) / max(1, len(evs))

def duty(evs, window_ms: float) -> float:
    return sum(e.t_end_rel_ms - e.t_fire_rel_ms for e in evs) / window_ms

if __name__ == "__main__":
    import json, sys
    n_pairs = 50          # 50 pair x 1200ms = 60s 窗口
    win = n_pairs * 1200
    rows = []
    for name, kw in [("a100", dict(alpha=1.0)), ("a050", dict(alpha=0.5)),
                     ("a000", dict(alpha=0.0)), ("pack_random", dict(mode="pack_random")),
                     ("blind_poisson", dict(mode="poisson"))]:
        e = build(n_pairs=n_pairs, seed=20260922, **kw)
        rows.append(dict(arm=name, K=len(e), alpha=round(realized_alpha(e), 4),
                         duty=round(duty(e, win), 4),
                         burst_total_ms=sum(x.t_end_rel_ms-x.t_fire_rel_ms for x in e)))
    print(f"{'臂':<15}{'K':>6}{'实测α':>9}{'duty':>8}{'ΣBURST(ms)':>12}")
    for r in rows:
        print(f"{r['arm']:<15}{r['K']:>6}{r['alpha']:>9}{r['duty']:>8}{r['burst_total_ms']:>12}")
