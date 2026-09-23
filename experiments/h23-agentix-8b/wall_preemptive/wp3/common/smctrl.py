"""libsmctrl 的最小 ctypes 绑定 —— 不依赖 sglang(它的服务端在持续负载下会崩)。

只用三个符号:
  libsmctrl_get_tpc_count(uint32* out, int dev)
  libsmctrl_make_mask(uint64* out, uint32 low, uint32 high_exclusive)   # bit=1 表示禁用, 极性由 C 侧处理
  libsmctrl_set_stream_mask_ext(cudaStream_t, uint128)                  # >64 TPC 的卡用 ext
"""
import ctypes, os

SO = os.environ.get("LIBSMCTRL_SO", "/workspace/AgentSys/third_party/BulletServe/csrc/build/libsmctrl.so")

class c_uint128(ctypes.Structure):
    _fields_ = [("low", ctypes.c_uint64), ("high", ctypes.c_uint64)]

class SmCtrl:
    def __init__(self, dev: int = 0, so: str = SO):
        self.lib = ctypes.CDLL(so)
        self.lib.libsmctrl_make_mask.argtypes = [ctypes.POINTER(ctypes.c_uint64), ctypes.c_uint32, ctypes.c_uint32]
        self.lib.libsmctrl_set_stream_mask_ext.argtypes = [ctypes.c_void_p, c_uint128]
        n = ctypes.c_uint32()
        try:
            self.lib.libsmctrl_get_tpc_info_cuda.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_int]
            if self.lib.libsmctrl_get_tpc_info_cuda(ctypes.byref(n), dev) == 0:
                self.total_tpcs = n.value
            else:
                self.total_tpcs = 64
        except Exception:
            self.total_tpcs = 64

    def mask(self, low: int, high_exclusive: int) -> int:
        out = ctypes.c_uint64()
        r = self.lib.libsmctrl_make_mask(ctypes.byref(out), ctypes.c_uint32(low), ctypes.c_uint32(high_exclusive))
        if r != 0: raise RuntimeError(f"libsmctrl_make_mask 失败 rc={r}")
        return out.value

    def set_stream(self, stream, low: int, high_exclusive: int) -> int:
        m = self.mask(low, high_exclusive)
        ptr = ctypes.c_void_p(stream.cuda_stream)
        self.lib.libsmctrl_set_stream_mask_ext(ptr, c_uint128(m, 0))
        return m
