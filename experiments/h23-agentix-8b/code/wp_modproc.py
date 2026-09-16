#!/usr/bin/env python3
"""Stage W (workload_profile port): module-level process instrumentation.

Determines the process layer the reference workflow's way — by the MODEL'S OWN
module structure (vLLM LlamaDecoderLayer), not by folding kernel sequences.
Each leaf module of every decoder layer gets a paired pre/post forward hook
emitting an NVTX range `p.L{layer}.{process}`; fragments are then the kernels
each range strictly owns (launch-time attribution, as in batch8).

Instrumentation arm only: module NVTX is dead under cudagraphs (verified
negative), so captures using this run with --enforce-eager. The graph arm
stays the performance-faithful companion (batch8's instrument/perf split).

DCU->GPU port notes: HIPTX -> torch.cuda.nvtx; everything else unchanged.
"""
from __future__ import annotations

import atexit
import json
import os
from collections import defaultdict

import torch.cuda.nvtx as nvtx

# process taxonomy: leaf module path (relative to a decoder layer) -> process
TAXONOMY = {
    "input_layernorm": "norm_in",
    "self_attn.qkv_proj": "qkv_proj",
    "self_attn.attn": "attn_core",      # kv-cache write + attention kernel(s)
    "self_attn.o_proj": "o_proj",
    "post_attention_layernorm": "norm_post",
    "mlp.gate_up_proj": "mlp_gate_up",
    "mlp.act_fn": "act_mul",
    "mlp.down_proj": "mlp_down",
}

_S = {"installed": False, "hooked_layers": 0, "counts": defaultdict(int)}


def _dump():
    if _S["hooked_layers"]:
        print(f"[wp_modproc] LEDGER layers={_S['hooked_layers']} "
              + " ".join(f"{k}={v}" for k, v in sorted(_S["counts"].items())), flush=True)


def _get(obj, path):
    for part in path.split("."):
        obj = getattr(obj, part, None)
        if obj is None:
            return None
    return obj


def _hook_layer(layer, li):
    for path, proc in TAXONOMY.items():
        mod = _get(layer, path)
        if mod is None:
            _S["counts"][f"missing:{proc}"] += 1
            continue
        label = f"p.L{li:02d}.{proc}"

        def pre(_m, _inp, _lab=label, _p=proc):
            nvtx.range_push(_lab)
            _S["counts"][_p] += 1

        def post(_m, _inp, _out):
            nvtx.range_pop()

        mod.register_forward_pre_hook(pre)
        mod.register_forward_hook(post)
    # the layer itself, so processes nest inside p.L{i}
    # NOTE: hooks MUST return None — range_push/pop return the depth int, and a
    # non-None pre-hook return replaces the forward args (post: the output).
    _ll = f"p.L{li:02d}"

    def lpre(_m, _inp):
        nvtx.range_push(_ll)

    def lpost(_m, _inp, _out):
        nvtx.range_pop()

    layer.register_forward_pre_hook(lpre)
    layer.register_forward_hook(lpost)


def install(verbose: bool = True) -> dict:
    """Patch GPUModelRunner.execute_model to hook decoder layers on first use
    (the model only exists inside the engine process)."""
    if _S["installed"]:
        return {"already": True}
    from vllm.v1.worker import gpu_model_runner as gmr
    R = gmr.GPUModelRunner
    orig = R.execute_model

    def execute_model(self, scheduler_output, *a, **kw):
        if not _S["hooked_layers"]:
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
                    _hook_layer(layer, li)
                _S["hooked_layers"] = len(layers)
                print(f"[wp_modproc] process hooks on {len(layers)} layers × "
                      f"{len(TAXONOMY)} processes", flush=True)
        return orig(self, scheduler_output, *a, **kw)

    execute_model._w_wrapped = True
    R.execute_model = execute_model
    atexit.register(_dump)
    _S["installed"] = True
    if verbose:
        print("[wp_modproc] installed (module-level process NVTX; eager arm only)",
              flush=True)
    return {"installed": True, "taxonomy": sorted(set(TAXONOMY.values()))}


def write_taxonomy(path: str):
    doc = {
        "schema": "PROCESS_TAXONOMY v1 (workload_profile port, vLLM Llama)",
        "hierarchy": ["call", "iter(step)", "layer", "process", "fragment(kernel)",
                      "ncu_counters"],
        "processes": [
            {"process": proc, "module": f"layers.{{i}}.{path}",
             "expected_fragments": FRAGS.get(proc, ["<capture-derived>"])}
            for path, proc in TAXONOMY.items()],
        "notes": "rotary embedding is applied inside self_attn.forward between "
                 "qkv_proj and attn ranges (not a hooked leaf module); its kernel "
                 "lands in the p.L*. gap between qkv_proj and attn_core and is "
                 "attributed by launch order. lm_head/logits are model-level, "
                 "outside the layer taxonomy.",
    }
    with open(path, "w") as f:
        json.dump(doc, f, indent=1)


FRAGS = {
    "norm_in": ["triton_red_fused_fused_add_rms_norm*"],
    "qkv_proj": ["cutlass::Kernel2<gemm>"],
    "attn_core": ["vllm::reshape_and_cache_flash*", "flash::flash_fwd_splitkv_kernel*",
                  "flash::flash_fwd_splitkv_combine*"],
    "o_proj": ["cutlass::Kernel2<gemm>"],
    "norm_post": ["triton_red_fused_fused_add_rms_norm*"],
    "mlp_gate_up": ["cutlass::Kernel2<gemm>"],
    "act_mul": ["triton_poi_fused_mul_silu*"],
    "mlp_down": ["cutlass::Kernel2<gemm>"],
}
