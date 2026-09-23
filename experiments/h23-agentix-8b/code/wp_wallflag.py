"""Engine-side wall-state flag exporter (A1 ablation support).

Each engine step writes (n_prefill_reqs, n_running) to a tiny state file.
The client's preemption gate reads it at quantum-chunk boundaries to decide
whether switching NOW collides with the current resource wall (A0 finding:
boundary inflation tracks the phase's scarce resource, not the phase name).
Installed pre-fork; runs inside the EngineCore child (fork-inherited).
"""
import json
import os


def install(path=None):
    path = path or os.environ.get('AGENTIX_WALLFLAG_PATH', '/tmp/agentix_wallflag.json')
    from vllm.v1.engine import core as _core
    orig = _core.EngineCoreProc._process_engine_step

    def wrapped(self, *a, **k):
        r = orig(self, *a, **k)
        try:
            sched = getattr(self, 'scheduler', None)
            if sched is not None:
                running = getattr(sched, 'running', []) or []
                n_pref = sum(1 for req in running
                             if getattr(req, 'num_computed_tokens', 0)
                             < getattr(req, 'num_prompt_tokens',
                                       getattr(req, 'num_tokens', 0)))
                tmp = path + '.tmp'
                with open(tmp, 'w') as f:
                    json.dump({'n_prefill': n_pref, 'n_running': len(running)}, f)
                os.replace(tmp, path)
        except Exception:
            pass
        return r
    _core.EngineCoreProc._process_engine_step = wrapped
    print('[wp_wallflag] installed ->', path, flush=True)
