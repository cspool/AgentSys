#!/usr/bin/env python3
"""R032 stage C: in-context FX trace, so attn_core stops being a hole.

The offline trace (wp_fx_trace.py) cannot contain vLLM's attention op: that op
reads the engine's forward context — KV cache handles, block tables, sequence
metadata — and none of it exists outside a serving step. Tracing the layer
*inside* a live step closes that gap: the forward context is the real one, so
make_fx records unified_attention_with_output and unified_kv_cache_update along
with everything else.

The price is one extra execution of the traced layer. It is taken deliberately
and bounded:

  - only the selected (phase, layer) classes are traced, once each;
  - the KV write it repeats is the same values into the same slots, so the cache
    ends in the state it would have reached anyway;
  - the traced run's output is discarded — the model keeps the output of its own
    forward, so no request sees a different token;
  - this run is a tracing run. Its wall-clock is not an endpoint.

Recursion is guarded: the hooks that trigger the trace are disabled while the
trace is running.
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
    "per_class": int(os.environ.get("AGENTIX_FXCTX_PER_CLASS", "1")),
    "layers": {int(x) for x in os.environ.get("AGENTIX_FXCTX_LAYERS", "0,15,31").split(",") if x.strip()},
    "out": os.environ.get("AGENTIX_FXCTX_OUT", "fx_incontext"),
    "tracing": False,
    "plain": set(),
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


def _plainify(module) -> int:
    """vLLM's weight parameter subclasses carry loader metadata and implement no
    __torch_dispatch__ for ops like aten.t, which make_fx hits immediately. The
    storage is untouched; only the wrapper changes."""
    n = 0
    for name, param in list(module.named_parameters(recurse=True)):
        owner = module
        parts = name.split(".")
        for part in parts[:-1]:
            owner = getattr(owner, part)
        setattr(owner, parts[-1], torch.nn.Parameter(
            param.data.detach().as_subclass(torch.Tensor), requires_grad=False))
        n += 1
    return n


def _node_record(n, order: int) -> dict:
    val = n.meta.get("val")
    return {"order": order, "name": n.name, "op": n.op, "target": str(n.target),
            "args": [str(a) for a in n.args], "users": [u.name for u in n.users],
            "shape": list(val.shape) if hasattr(val, "shape") else None,
            "dtype": str(val.dtype) if hasattr(val, "dtype") else None}


def _hook_layer(layer, li):
    def pre(_m, args, kwargs):
        if _S["tracing"]:
            return None
        cls = (_phase(_S["reqs"], _S["tokens"]), li)
        if _S["budget"][cls] >= _S["per_class"]:
            return None
        _S["budget"][cls] += 1
        phase = cls[0]
        if li not in _S["plain"]:
            _plainify(layer)
            _S["plain"].add(li)
        tag = f"{phase}_L{li:02d}_step{_S['step']}_incontext"
        _S["tracing"] = True
        try:
            from torch.fx.experimental.proxy_tensor import make_fx

            def fn(*a, **kw):
                return layer(*a, **kw)

            with torch.no_grad():
                gm = make_fx(fn, tracing_mode="real")(*args, **(kwargs or {}))
            nodes = [_node_record(n, i) for i, n in enumerate(gm.graph.nodes)]
            os.makedirs(_S["out"], exist_ok=True)
            with open(os.path.join(_S["out"], f"{tag}.json"), "w") as fh:
                json.dump({"sample": tag, "fragment": "full_layer_incontext",
                           "phase": phase, "layer_idx": li, "step_id": _S["step"],
                           "reqs": _S["reqs"], "tokens": _S["tokens"],
                           "input_shapes": {"hidden_states": list(args[1].shape)
                                            if len(args) > 1 and isinstance(args[1], torch.Tensor)
                                            else None},
                           "nodes": nodes}, fh, indent=1)
            with open(os.path.join(_S["out"], f"{tag}.py"), "w") as fh:
                fh.write(gm.code)
            targets = {n["target"] for n in nodes}
            _S["index"].append({
                "tag": tag, "phase": phase, "layer_idx": li, "step_id": _S["step"],
                "reqs": _S["reqs"], "tokens": _S["tokens"], "nodes": len(nodes),
                "has_attention": any("unified_attention" in t for t in targets),
                "has_kv_update": any("unified_kv_cache_update" in t for t in targets)})
            with open(os.path.join(_S["out"], "incontext_index.json"), "w") as fh:
                json.dump(_S["index"], fh, indent=1)
            print(f"[wp_fxctx] {tag}: {len(nodes)} nodes "
                  f"attention={_S['index'][-1]['has_attention']} "
                  f"kv_update={_S['index'][-1]['has_kv_update']}", flush=True)
        except Exception as exc:
            print(f"[wp_fxctx] {tag} FAILED: {type(exc).__name__}: {exc}", flush=True)
            _S["index"].append({"tag": tag, "phase": phase, "layer_idx": li,
                                "error": f"{type(exc).__name__}: {exc}"})
        finally:
            _S["tracing"] = False
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
                print(f"[wp_fxctx] in-context tracing on layers {sorted(_S['layers'])}, "
                      f"{_S['per_class']} per (phase, layer)", flush=True)
        return orig(self, scheduler_output, *a, **kw)

    R.execute_model = execute_model
    _S["installed"] = True
    if verbose:
        print("[wp_fxctx] installed (in-context FX tracing)", flush=True)
    return {"installed": True, "layers": sorted(_S["layers"])}
