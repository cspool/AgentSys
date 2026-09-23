"""相位信标: 受害者侧写, 抢占者/控制器侧读。

用 mmap 文件 + 奇偶 seq 做撕裂检测(写前 seq+1 变奇数, 写后 seq+1 变偶数),
读侧看到奇数或前后 seq 不一致就重读。避免了跨进程加锁。

布局 (小端):
  0  : uint64 seq
  8  : int32  phase_id   (0=DRAM 相, 1=TC 相, 2=过渡/混合)
  12 : int32  _pad
  16 : uint64 t_change_ns (CLOCK_MONOTONIC_RAW)
  24 : uint64 n_switch
"""
from __future__ import annotations
import mmap, os, struct, time

SIZE = 64
_FMT = "<QiiQQ"

def mono_ns() -> int:
    return time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW)

class PhaseBeacon:
    def __init__(self, path: str, create: bool = False):
        self.path = path
        if create:
            with open(path, "wb") as f:
                f.write(b"\0" * SIZE)
        self.f = open(path, "r+b")
        self.m = mmap.mmap(self.f.fileno(), SIZE)
        if create:
            self._write(0, 2, mono_ns(), 0)

    def _write(self, seq, phase, t_ns, n_sw):
        self.m.seek(0); self.m.write(struct.pack(_FMT, seq, phase, 0, t_ns, n_sw))

    def publish(self, phase_id: int) -> None:
        seq, _, _, _, n_sw = struct.unpack(_FMT, self.m[:struct.calcsize(_FMT)])
        self._write(seq + 1, phase_id, mono_ns(), n_sw)          # 奇数 = 写入中
        self._write(seq + 2, phase_id, mono_ns(), n_sw + 1)      # 偶数 = 稳定

    def read(self):
        """返回 (phase_id, t_change_ns, n_switch) 或 None(撕裂)。"""
        for _ in range(8):
            a = struct.unpack(_FMT, self.m[:struct.calcsize(_FMT)])
            if a[0] % 2: continue
            b = struct.unpack(_FMT, self.m[:struct.calcsize(_FMT)])
            if a[0] == b[0]: return a[1], a[3], a[4]
        return None

    def close(self):
        try: self.m.close(); self.f.close()
        except Exception: pass
