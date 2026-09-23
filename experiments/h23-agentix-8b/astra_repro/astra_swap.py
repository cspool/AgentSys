"""Run serve_agentix with Astra's optimized kernels patched into vLLM.

ASTRA_SWAP=silu : replace SiluAndMul.forward_cuda with their sgl_silu_mul
                  (bf16-native kernel from silu_mul_ultimate.cu).
ASTRA_SWAP=rms  : replace RMSNorm fused-add path with their fp32-only
                  rms_ultimate.cu the way a wall-clock-guided integration
                  would: bf16 add + residual copy + fp32 casts + zeros
                  residual + fp32 kernel + cast back. Their kernel does not
                  write residual back, so the add must happen outside it.
Unset           : stock kernels (control).
"""
import os, sys
# must be set before any vllm import: run the engine in-process (same as the
# v2 lineage contract) so kernel patches apply inside the engine loop
os.environ["VLLM_ENABLE_V1_MULTIPROCESSING"] = "0"
os.environ["VLLM_USE_V2_MODEL_RUNNER"] = "0"
import torch

BASE = "/workspace/AgentSys/experiments/h23-agentix-8b/astra_repro/Astra/test"
MODE = os.environ.get("ASTRA_SWAP", "")

def _load_prebuilt(name, sodir):
    # torch.utils.cpp_extension merely IMPORTING it poisons CUDA fork (the
    # EngineCore child then dies with "Cannot re-initialize CUDA in forked
    # subprocess"), so dlopen the prebuilt .so directly.
    import importlib.machinery, glob
    so = glob.glob(f"{sodir}/{name}*.so")
    assert so, f"prebuilt {name}.so missing in {sodir} — build it via the harness first"
    return importlib.machinery.ExtensionFileLoader(name, so[0]).load_module()

if MODE == "silu":
    ext = _load_prebuilt("silu_mul_ext", f"{BASE}/silu")
    from vllm.model_executor.layers import activation as _act
    def _fwd(self, x):
        d = x.shape[-1] // 2
        out = torch.empty(x.shape[:-1] + (d,), dtype=x.dtype, device=x.device)
        ext.sgl_silu_mul(x.contiguous(), out)
        return out
    _act.SiluAndMul.forward_cuda = _fwd
    print("[astra_swap] SiluAndMul -> Astra ultimate", flush=True)
elif MODE == "rms":
    ext = _load_prebuilt("rmsnorm_ext_new", f"{BASE}/rms")
    from vllm.model_executor.layers import layernorm as _ln
    _orig = _ln.RMSNorm.forward_cuda
    def _fwd(self, x, residual=None):
        if residual is None:
            return _orig(self, x, None)
        z = x + residual
        residual.copy_(z)
        zf = z.float()
        zr = torch.zeros_like(zf)
        wf = getattr(self, "_astra_wf", None)
        if wf is None or wf.device != zf.device:
            wf = self.weight.data.float(); self._astra_wf = wf
        ext.sgl_fused_add_rmsnorm(zf, zr, wf, float(self.variance_epsilon), False)
        x.copy_(zf.to(x.dtype))
        return x, residual
    _ln.RMSNorm.forward_cuda = _fwd
    print("[astra_swap] RMSNorm fused-add -> Astra ultimate (fp32 chain)", flush=True)

sys.path.insert(0, "/workspace/AgentSys/experiments/h23-agentix-8b/code")

# 对照协议登记:每臂自动落 launch_manifest.json(缺 manifest 不得进对照表)
def _emit_manifest():
    import hashlib, json, subprocess
    from datetime import datetime, timezone
    argv = sys.argv[1:]
    out_dir = None
    wl = None
    for i, a in enumerate(argv):
        if a == '--output-dir':
            out_dir = argv[i + 1]
        if a == '--workload':
            wl = argv[i + 1]
    if not out_dir:
        return
    sha = lambda f: hashlib.sha256(Path(f).read_bytes()).hexdigest()
    base = Path('/workspace/AgentSys/experiments/h23-agentix-8b')
    try:
        gpu = subprocess.run(['nvidia-smi', '--query-gpu=name,driver_version',
                              '--format=csv,noheader'], capture_output=True,
                             text=True, timeout=10).stdout.strip().splitlines()[0]
    except Exception:
        gpu = 'unknown'
    man = {
        'argv': argv,
        'workload': wl, 'workload_sha256': sha(wl) if wl else None,
        'harness_sha256': {'serve_agentix.py': sha(base / 'code/serve_agentix.py'),
                           'astra_swap.py': sha(__file__)},
        'env': {k: v for k, v in os.environ.items()
                if k.startswith(('VLLM_', 'AGENTIX_', 'CUDA_', 'ASTRA_', 'LD_LIBRARY'))},
        'gpu_driver': gpu,
        'utc': f'{datetime.now(timezone.utc):%Y-%m-%dT%H:%M:%SZ}',
    }
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    (Path(out_dir) / 'launch_manifest.json').write_text(
        json.dumps(man, indent=1, ensure_ascii=False) + '\n')

from pathlib import Path
_emit_manifest()
import serve_agentix
sys.exit(serve_agentix.main())
