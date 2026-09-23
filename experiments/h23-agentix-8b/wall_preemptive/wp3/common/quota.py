"""抢占者配额旋钮: 用 libsmctrl 给抢占者的 stream 打 TPC mask。

关键约束(来自对抗审查, 都已在本机核实):
  - 一律走 SMController.set_stream_mask(stream, low, high_exclusive), 不自己拼 mask。
    libsmctrl_make_mask 在 C 侧处理 "bit=1 表示禁用" 的极性, 自己拼必踩挂死坑。
  - 只给抢占者的 stream 打 mask, 绝不设 global mask(128 SM 上 sm_controller.py:70 会 raise),
    也绝不收窄受害者。
  - 绝不开 CUDA Graph: libsmctrl 与 graph 不兼容(图节点 TMD 在 instantiate 时定稿)。
  - Q_base 必须非零 —— 抢占事件只改配额, 不改"跑不跑", 这是全程并发的结构保证。
"""
from __future__ import annotations
import sys, time

def mono_ns() -> int:
    return time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW)

class TpcMaskKnob:
    def __init__(self, stream, base_tpcs: int, burst_tpcs: int,
                 bullet_py: str = "/workspace/AgentSys/third_party/BulletServe/python"):
        if bullet_py not in sys.path: sys.path.insert(0, bullet_py)
        from sglang.srt.bullet.sm_controller import SMController
        self.c = SMController()
        self.total = self.c.total_tpcs
        assert 0 < base_tpcs <= self.total and base_tpcs <= burst_tpcs <= self.total, \
            f"配额非法: base={base_tpcs} burst={burst_tpcs} total={self.total}"
        self.stream = stream
        self.levels = {"BASE": base_tpcs, "BURST": burst_tpcs}
        self.epoch = 0
        self.log: list[tuple[int, str, int]] = []   # (t_ns, level, n_tpc)
        self.set_quota("BASE")

    def set_quota(self, level: str) -> int:
        n = self.levels[level]
        self.c.set_stream_mask(self.stream, 0, n)    # [low, high_exclusive)
        t = mono_ns(); self.epoch += 1
        self.log.append((t, level, n))
        return t

    def describe(self) -> dict:
        return dict(knob="tpc_mask", total_tpcs=self.total,
                    base=self.levels["BASE"], burst=self.levels["BURST"],
                    n_switch=self.epoch)

    def selftest(self) -> dict:
        """BASE ⊂ BURST 且 |BASE| >= 2; 并用 validate_stream_mask 让 C 侧确认。"""
        assert self.levels["BASE"] >= 2, "Q_base 至少 2 个 TPC(全程并发的结构下界)"
        assert self.levels["BASE"] <= self.levels["BURST"], "BASE 必须是 BURST 的子集"
        ok = {}
        for lv, n in self.levels.items():
            self.c.set_stream_mask(self.stream, 0, n)
            try:
                r = self.c.lib.validate_stream_mask(self.stream, 0, n, False)
                ok[lv] = (r == 0)
            except Exception as e:
                ok[lv] = f"validate 不可用: {type(e).__name__}"
        self.set_quota("BASE")
        return dict(validated=ok, **self.describe())
