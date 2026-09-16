#!/usr/bin/env python3
"""R032 stage B: fixed-input FX ATen DAG for the sampled layer events.

Runs with no engine serving. The model is loaded, the sampled activations are
replayed through the selected layer's submodules, and make_fx records the ATen
graph with node args and users.

Attention is a declared boundary, not an omission. vLLM's attention op reads the
engine's forward context (KV cache handles, block tables, sequence metadata);
outside a serving step that context does not exist, and fabricating one would
produce a graph for a shape the engine never runs. The layer is therefore traced
as two fragments — everything before attention and everything after it — and
attn_core is reported as an uncovered process with this reason. R041's dispatch
evidence already covers attn_core's ATen ops.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import torch


def node_record(n, order: int) -> dict:
    return {
        "order": order,
        "name": n.name,
        "op": n.op,
        "target": str(n.target),
        "args": [str(a) for a in n.args],
        "users": [u.name for u in n.users],
        "shape": (list(n.meta["val"].shape)
                  if "val" in n.meta and hasattr(n.meta["val"], "shape") else None),
        "dtype": (str(n.meta["val"].dtype)
                  if "val" in n.meta and hasattr(n.meta["val"], "dtype") else None),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", default="/data3/docker_model/AgentSys/Llama-3.1-8B")
    ap.add_argument("--samples", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--gpu-util", type=float, default=0.85)
    a = ap.parse_args()
    (a.out_dir / "fx_trace").mkdir(parents=True, exist_ok=True)
    (a.out_dir / "fx_graphmodules").mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("VLLM_USE_V2_MODEL_RUNNER", "0")
    os.environ.setdefault("VLLM_ENABLE_V1_MULTIPROCESSING", "0")
    from torch.fx.experimental.proxy_tensor import make_fx
    from vllm import LLM

    index = json.loads((a.samples / "sample_index.json").read_text())
    llm = LLM(model=a.model_dir, dtype="bfloat16", gpu_memory_utilization=a.gpu_util,
              max_model_len=2048, enforce_eager=True, seed=0, disable_log_stats=True)
    runner = llm.llm_engine.engine_core.engine_core.model_executor.driver_worker.model_runner
    layers = runner.model.model.layers
    dev = next(layers[0].parameters()).device

    def plainify(module) -> int:
        """vLLM wraps weights in parameter subclasses that carry loader metadata.
        Those subclasses have no __torch_dispatch__ implementation for ops like
        aten.t, so make_fx fails on the first transpose. Offline, with nothing
        left to load, the loader metadata has no job: re-wrap each weight as a
        plain parameter holding the same storage."""
        n = 0
        for name, param in list(module.named_parameters(recurse=True)):
            owner = module
            parts = name.split(".")
            for part in parts[:-1]:
                owner = getattr(owner, part)
            plain = torch.nn.Parameter(
                param.data.detach().as_subclass(torch.Tensor), requires_grad=False)
            setattr(owner, parts[-1], plain)
            n += 1
        return n

    plainified = {}
    for li in sorted({e["layer_idx"] for e in index}):
        plainified[li] = plainify(layers[li])
    print(f"[wp_fx] plainified params per layer: {plainified}", flush=True)

    results, failures = [], []
    for entry in index:
        li = entry["layer_idx"]
        layer = layers[li]
        payload = torch.load(entry["path"])
        hs = payload["hidden_states"].to(dev)
        res = payload["residual"]
        res = res.to(dev) if res is not None else None
        pos = payload["positions"].to(dev)

        def pre_attention(hidden, residual, positions):
            out = layer.input_layernorm(hidden) if residual is None else \
                layer.input_layernorm(hidden, residual)
            normed = out[0] if isinstance(out, tuple) else out
            qkv, _ = layer.self_attn.qkv_proj(normed)
            q, k, v = qkv.split(
                [layer.self_attn.q_size, layer.self_attn.kv_size,
                 layer.self_attn.kv_size], dim=-1)
            q, k = layer.self_attn.rotary_emb(positions, q, k)
            return q, k, v

        def post_attention(attn_out, residual):
            out, _ = layer.self_attn.o_proj(attn_out)
            normed, res2 = layer.post_attention_layernorm(out, residual)
            return layer.mlp(normed), res2

        hidden_size = hs.shape[-1]
        attn_out = torch.zeros_like(hs)
        residual_in = res if res is not None else torch.zeros_like(hs)
        for name, fn, args in (("pre_attention", pre_attention, (hs, res, pos)),
                               ("post_attention", post_attention, (attn_out, residual_in))):
            tag = f"{entry['sample']}_{name}"
            try:
                with torch.no_grad():
                    gm = make_fx(fn, tracing_mode="real")(*args)
                nodes = [node_record(n, i) for i, n in enumerate(gm.graph.nodes)]
                (a.out_dir / "fx_trace" / f"{tag}.json").write_text(json.dumps({
                    "sample": entry["sample"], "fragment": name,
                    "phase": entry["phase"], "layer_idx": li,
                    "step_id": entry["step_id"], "reqs": entry["reqs"],
                    "tokens": entry["tokens"], "hidden_size": hidden_size,
                    "input_shapes": {k: v for k, v in entry["shapes"].items()},
                    "nodes": nodes,
                }, indent=1) + "\n")
                (a.out_dir / "fx_graphmodules" / f"{tag}.py").write_text(gm.code)
                results.append({"tag": tag, "sample": entry["sample"],
                                "fragment": name, "phase": entry["phase"],
                                "layer_idx": li, "nodes": len(nodes),
                                "call_function_nodes": sum(
                                    1 for n in nodes if n["op"] == "call_function")})
                print(f"[wp_fx] {tag}: {len(nodes)} nodes", flush=True)
            except Exception as exc:
                failures.append({"tag": tag, "fragment": name,
                                 "error": f"{type(exc).__name__}: {exc}"})
                print(f"[wp_fx] {tag} FAILED: {type(exc).__name__}: {exc}", flush=True)

    out = {
        "samples": len(index),
        "plainified_params_per_layer": plainified,
        "fragments_traced": len(results),
        "fragments_failed": len(failures),
        "uncovered_processes": ["attn_core"],
        "uncovered_reason": ("vLLM's attention op reads the engine forward context "
                             "(KV cache handles, block tables, sequence metadata); "
                             "outside a serving step that context does not exist. "
                             "attn_core's ATen ops are covered by the R031/R041 "
                             "dispatch evidence instead."),
        "post_attention_input_note": ("the attention output fed to the post-attention "
                                      "fragment is a zero tensor of the sampled shape: "
                                      "the graph structure depends on the shape, and no "
                                      "sampled values for that tensor were kept"),
        "results": results, "failures": failures,
    }
    (a.out_dir / "fx_validation.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in
                      ("samples", "fragments_traced", "fragments_failed")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
