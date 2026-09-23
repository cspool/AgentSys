"""Iteration-boundary pause gate for the offline engine (KernelPreempt/TGS
proxy). While the pause file exists, the engine's step loop sleeps BETWEEN
iterations — no mid-kernel effect, pure boundary preemption. Installed
pre-fork under AGENTIX_PAUSE_FILE; runs in the EngineCore child."""
import os
import time


def install():
    pf = os.environ.get('AGENTIX_PAUSE_FILE')
    if not pf:
        return
    from vllm.v1.engine import core as _core
    orig = _core.EngineCoreProc._process_engine_step

    def gated(self, *a, **k):
        while os.path.exists(pf):
            time.sleep(0.005)
        return orig(self, *a, **k)
    _core.EngineCoreProc._process_engine_step = gated
    print('[wp_pause] iteration gate ->', pf, flush=True)
