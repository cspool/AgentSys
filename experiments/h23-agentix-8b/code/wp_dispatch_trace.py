#!/usr/bin/env python3
"""R031 filtered eager DispatchMode capture.

Records the ATen ops that actually run inside the R02-selected layers, with
tensor identity on both sides of each op, so R041 can rebuild the
producer-consumer DAG of a process.

Scope control matters here. Enabling a dispatch mode for the whole engine would
record every op of every layer of every step; instead the mode is entered in the
selected layer's forward pre-hook and left in its post-hook, and recording is
budgeted per (phase, layer) class so the capture covers the regimes the manifest
names without growing without bound.

Tensor identity is `(data_ptr, storage_offset, shape)`. The allocator reuses
addresses, so this identity is only trusted inside one layer forward — which is
exactly the window a process DAG spans. Ops are recorded with their layer event,
never pooled across events.
"""
from __future__ import annotations

import json
import os
from collections import defaultdict

import torch
from torch.utils._python_dispatch import TorchDispatchMode

_S = {
    "installed": False,
    "step": -1,
    "reqs": None,
    "tokens": None,
    "records": [],
    "budget": defaultdict(int),
    "per_class": int(os.environ.get("AGENTIX_DISPATCH_PER_CLASS", "2")),
    "layers": {int(x) for x in os.environ.get("AGENTIX_DISPATCH_LAYERS", "0,15,31").split(",") if x.strip()},
    "out": os.environ.get("AGENTIX_DISPATCH_OUT", "dispatch_profile.jsonl"),
    "event": None,
    "order": 0,
    "ops": 0,
    "written": 0,
}


def _phase(reqs, tokens) -> str:
    if not reqs or not tokens:
        return "unknown"
    if tokens > reqs * 4:
        return "prefill_heavy"
    if reqs >= 12:
        return "storm"
    return "steady_decode"


def _tid(t) -> str | None:
    if not isinstance(t, torch.Tensor):
        return None
    try:
        return f"{t.data_ptr():x}:{t.storage_offset()}:{tuple(t.shape)}"
    except Exception:
        return None


def _meta(t):
    return {"id": _tid(t), "dtype": str(t.dtype), "shape": list(t.shape),
            "stride": list(t.stride()), "device": str(t.device)}


class _Recorder(TorchDispatchMode):
    def __torch_dispatch__(self, func, types, args=(), kwargs=None):
        kwargs = kwargs or {}
        out = func(*args, **kwargs)
        ev = _S["event"]
        if ev is not None:
            ins, outs = [], []
            for a in list(args) + list(kwargs.values()):
                if isinstance(a, torch.Tensor):
                    ins.append(_meta(a))
                elif isinstance(a, (list, tuple)):
                    ins.extend(_meta(x) for x in a if isinstance(x, torch.Tensor))
            if isinstance(out, torch.Tensor):
                outs.append(_meta(out))
            elif isinstance(out, (list, tuple)):
                outs.extend(_meta(x) for x in out if isinstance(x, torch.Tensor))
            _S["records"].append({
                "event_id": ev["event_id"], "step_id": ev["step_id"],
                "layer_idx": ev["layer_idx"], "phase": ev["phase"],
                "order": _S["order"], "op": str(func),
                "inputs": ins, "outputs": outs,
            })
            _S["order"] += 1
            _S["ops"] += 1
        return out


_MODE = _Recorder()


def _hook_layer(layer, li):
    def pre(_m, _inp):
        cls = (_phase(_S["reqs"], _S["tokens"]), li)
        if _S["budget"][cls] >= _S["per_class"]:
            return None
        _S["budget"][cls] += 1
        _S["event"] = {
            "event_id": f"step{_S['step']}_layer{li}_occ0",
            "step_id": _S["step"], "layer_idx": li, "phase": cls[0],
        }
        _S["order"] = 0
        _MODE.__enter__()
        return None

    def post(_m, _inp, _out):
        if _S["event"] is not None:
            _MODE.__exit__(None, None, None)
            _S["event"] = None
            _flush()
        return None

    layer.register_forward_pre_hook(pre)
    layer.register_forward_hook(post)


def _path() -> str:
    # One file per process. The engine core records; the parent that also loads
    # this module must not truncate the child's file on its own exit.
    base = _S["out"]
    return f"{base}.{os.getpid()}"


def _flush():
    """Append this event's records now. The engine core is torn down by signal,
    so an atexit-only dump loses the whole capture."""
    if not _S["records"]:
        return
    path = _path()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a") as fh:
        for r in _S["records"]:
            fh.write(json.dumps(r) + "\n")
    _S["written"] += len(_S["records"])
    _S["records"] = []


def _dump():
    _flush()
    if not _S["written"]:
        return
    classes = {f"{k[0]}|L{k[1]}": v for k, v in sorted(_S["budget"].items())}
    print(f"[wp_dispatch] wrote {_S['written']} op records to {_path()} "
          f"classes={classes}", flush=True)


def install(verbose: bool = True) -> dict:
    if _S["installed"]:
        return {"already": True}
    import atexit

    from vllm.v1.worker import gpu_model_runner as gmr
    R = gmr.GPUModelRunner
    orig = R.execute_model
    hooked = {"done": False}

    def execute_model(self, scheduler_output, *a, **kw):
        _S["step"] += 1
        try:
            n = getattr(scheduler_output, "num_scheduled_tokens", None)
            if isinstance(n, dict):
                _S["reqs"] = len(n)
                _S["tokens"] = sum(n.values())
            else:
                _S["reqs"] = getattr(scheduler_output, "num_reqs", None)
                _S["tokens"] = getattr(scheduler_output, "total_num_scheduled_tokens", None)
        except Exception:
            _S["reqs"] = _S["tokens"] = None
        if not hooked["done"]:
            model = getattr(self, "model", None)
            layers = None
            for path in ("model.layers", "language_model.model.layers"):
                obj = model
                for part in path.split("."):
                    obj = getattr(obj, part, None)
                    if obj is None:
                        break
                if obj is not None:
                    layers = obj
                    break
            if layers is not None:
                for li, layer in enumerate(layers):
                    if li in _S["layers"]:
                        _hook_layer(layer, li)
                hooked["done"] = True
                print(f"[wp_dispatch] dispatch hooks on layers {sorted(_S['layers'])}, "
                      f"budget {_S['per_class']} per (phase, layer)", flush=True)
        return orig(self, scheduler_output, *a, **kw)

    R.execute_model = execute_model
    atexit.register(_dump)
    _S["installed"] = True
    if verbose:
        print("[wp_dispatch] installed (filtered eager DispatchMode)", flush=True)
    return {"installed": True, "layers": sorted(_S["layers"])}
