#!/usr/bin/env python3
"""R032 stage A: sample a real serving input for each selected layer event.

The sample is taken inside a live engine step, so the tensor carries the batch
composition that step actually had. A synthetic batch of one would specialize the
later FX graph to a shape the serving engine never runs, and every claim made
from that graph would then describe a shape that does not exist.

Only inputs are saved. Nothing is re-executed here, so the sampling has no effect
on the KV cache or on the run's outputs.
"""
from __future__ import annotations

import json
import os
from collections import defaultdict

import torch

_S = {
    "installed": False,
    "step": -1,
    "reqs": None,
    "tokens": None,
    "budget": defaultdict(int),
    "per_class": int(os.environ.get("AGENTIX_FXSAMPLE_PER_CLASS", "1")),
    "layers": {int(x) for x in os.environ.get("AGENTIX_FXSAMPLE_LAYERS", "0,15,31").split(",") if x.strip()},
    "out": os.environ.get("AGENTIX_FXSAMPLE_OUT", "samples"),
    "index": [],
}


def _phase(reqs, tokens) -> str:
    if not reqs or not tokens:
        return "unknown"
    if tokens > reqs * 4:
        return "prefill_heavy"
    if reqs >= 12:
        return "storm"
    return "steady_decode"


def _cpu(x):
    return x.detach().to("cpu").clone() if isinstance(x, torch.Tensor) else None


def _hook_layer(layer, li):
    def pre(_m, inp, kwargs=None):
        cls = (_phase(_S["reqs"], _S["tokens"]), li)
        if _S["budget"][cls] >= _S["per_class"]:
            return None
        _S["budget"][cls] += 1
        phase, _ = cls
        payload = {"positions": None, "hidden_states": None, "residual": None}
        tensors = [x for x in inp if isinstance(x, torch.Tensor)]
        if kwargs:
            tensors += [v for v in kwargs.values() if isinstance(v, torch.Tensor)]
        for t in tensors:
            if t.dim() == 1 and payload["positions"] is None:
                payload["positions"] = _cpu(t)
            elif t.dim() == 2 and payload["hidden_states"] is None:
                payload["hidden_states"] = _cpu(t)
            elif t.dim() == 2 and payload["residual"] is None:
                payload["residual"] = _cpu(t)
        name = f"{phase}_L{li:02d}_step{_S['step']}"
        path = os.path.join(_S["out"], f"{name}.pt")
        os.makedirs(_S["out"], exist_ok=True)
        torch.save(payload, path)
        _S["index"].append({
            "sample": name, "path": path, "phase": phase, "layer_idx": li,
            "step_id": _S["step"], "reqs": _S["reqs"], "tokens": _S["tokens"],
            "shapes": {k: (list(v.shape) if v is not None else None)
                       for k, v in payload.items()},
            "dtypes": {k: (str(v.dtype) if v is not None else None)
                       for k, v in payload.items()},
        })
        with open(os.path.join(_S["out"], "sample_index.json"), "w") as fh:
            json.dump(_S["index"], fh, indent=1)
        print(f"[wp_fxsample] saved {name} "
              f"shapes={_S['index'][-1]['shapes']}", flush=True)
        return None

    layer.register_forward_pre_hook(pre, with_kwargs=True)


def install(verbose: bool = True) -> dict:
    if _S["installed"]:
        return {"already": True}
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
                print(f"[wp_fxsample] sampling layers {sorted(_S['layers'])}, "
                      f"{_S['per_class']} per (phase, layer)", flush=True)
        return orig(self, scheduler_output, *a, **kw)

    R.execute_model = execute_model
    _S["installed"] = True
    if verbose:
        print("[wp_fxsample] installed (real-input sampling)", flush=True)
    return {"installed": True, "layers": sorted(_S["layers"])}
