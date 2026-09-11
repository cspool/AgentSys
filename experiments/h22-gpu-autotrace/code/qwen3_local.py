#!/usr/bin/env python3
"""Minimal, dependency-free Qwen3 inference from local safetensors weights.

No `transformers`, `safetensors` or `tokenizers` packages are available in this
environment and nothing may be downloaded, so this module implements the three
pieces needed to run the local ``Qwen3-1.7B`` checkpoint with plain PyTorch:

* ``SafetensorsFile``: header parse + zero-copy tensor slicing from the file;
* ``ByteLevelBPE``: GPT-2 style byte-level BPE (vocab.json + merges.txt) with
  the Qwen pre-tokenizer regex approximated for ASCII text (the ``regex``
  module with ``\\p{L}`` classes is not installed). Round-trip is verified at
  load time on the prompts that are used.
* ``Qwen3Model``: embedding, 28 decoder layers (RMSNorm, GQA attention with
  per-head q/k RMSNorm and RoPE theta 1e6, SwiGLU MLP), final norm, tied
  lm_head. Eager PyTorch, bf16, preallocated KV cache, greedy decoding.

Every layer forward is wrapped in an NVTX range named in the certified
``agentsys.mllm::<call>::<index>::<op_type>`` form so the w01/w02 analyzers
consume the trace unchanged. Nothing here touches ``src/agentsys``.
"""

from __future__ import annotations

import json
import math
import re
import struct
from functools import lru_cache
from pathlib import Path
from typing import Any

import torch

DTYPES = {"BF16": torch.bfloat16, "F16": torch.float16, "F32": torch.float32, "I64": torch.int64, "I32": torch.int32}


class SafetensorsFile:
    def __init__(self, path: Path):
        self.path = path
        with path.open("rb") as handle:
            (n,) = struct.unpack("<Q", handle.read(8))
            header = json.loads(handle.read(n))
        self.header = {k: v for k, v in header.items() if k != "__metadata__"}
        self.data_start = 8 + n
        self._storage: torch.Tensor | None = None

    def _bytes(self) -> torch.Tensor:
        if self._storage is None:
            # Whole-file uint8 tensor from an mmap; slices below are views.
            self._storage = torch.from_file(str(self.path), shared=False, size=self.path.stat().st_size, dtype=torch.uint8)
        return self._storage

    def tensor(self, name: str, device: torch.device) -> torch.Tensor:
        meta = self.header[name]
        start, end = meta["data_offsets"]
        raw = self._bytes()[self.data_start + start : self.data_start + end]
        return raw.view(DTYPES[meta["dtype"]]).reshape(meta["shape"]).to(device, copy=True)


@lru_cache(maxsize=1)
def _bytes_to_unicode() -> dict[int, str]:
    bs = list(range(ord("!"), ord("~") + 1)) + list(range(ord("¡"), ord("¬") + 1)) + list(range(ord("®"), ord("ÿ") + 1))
    cs = bs[:]
    n = 0
    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(256 + n)
            n += 1
    return dict(zip(bs, (chr(c) for c in cs)))


class ByteLevelBPE:
    # Qwen pattern with \p{L} -> ASCII letters and \p{N} -> ASCII digits.
    PATTERN = re.compile(r"(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\nA-Za-z0-9]?[A-Za-z]+|[0-9]| ?[^\sA-Za-z0-9]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+")

    def __init__(self, model_dir: Path):
        self.encoder: dict[str, int] = json.loads((model_dir / "vocab.json").read_text(encoding="utf-8"))
        self.decoder = {v: k for k, v in self.encoder.items()}
        merges = [line.split() for line in (model_dir / "merges.txt").read_text(encoding="utf-8").splitlines() if line and not line.startswith("#")]
        self.bpe_ranks = {tuple(m): i for i, m in enumerate(merges)}
        self.byte_encoder = _bytes_to_unicode()
        self.byte_decoder = {v: k for k, v in self.byte_encoder.items()}
        tok = json.loads((model_dir / "tokenizer.json").read_text(encoding="utf-8"))
        self.special = {a["content"]: a["id"] for a in tok["added_tokens"]}
        self.decoder.update({v: k for k, v in self.special.items()})
        self.cache: dict[str, list[str]] = {}

    def _bpe(self, token: str) -> list[str]:
        if token in self.cache:
            return self.cache[token]
        word = list(token)
        while len(word) > 1:
            pairs = {(word[i], word[i + 1]) for i in range(len(word) - 1)}
            best = min(pairs, key=lambda p: self.bpe_ranks.get(p, math.inf))
            if best not in self.bpe_ranks:
                break
            first, second = best
            merged: list[str] = []
            i = 0
            while i < len(word):
                if i < len(word) - 1 and word[i] == first and word[i + 1] == second:
                    merged.append(first + second)
                    i += 2
                else:
                    merged.append(word[i])
                    i += 1
            word = merged
        self.cache[token] = word
        return word

    def encode(self, text: str) -> list[int]:
        ids: list[int] = []
        # split out special tokens first
        pattern = "(" + "|".join(re.escape(s) for s in sorted(self.special, key=len, reverse=True)) + ")"
        for chunk in re.split(pattern, text):
            if not chunk:
                continue
            if chunk in self.special:
                ids.append(self.special[chunk])
                continue
            for piece in self.PATTERN.findall(chunk):
                mapped = "".join(self.byte_encoder[b] for b in piece.encode("utf-8"))
                ids.extend(self.encoder[t] for t in self._bpe(mapped))
        return ids

    def decode(self, ids: list[int]) -> str:
        out = bytearray()
        for i in ids:
            tok = self.decoder[i]
            if tok in self.special:
                out += tok.encode("utf-8")
            else:
                out += bytes(self.byte_decoder[c] for c in tok)
        return out.decode("utf-8", errors="replace")


class RMSNorm(torch.nn.Module):
    def __init__(self, weight: torch.Tensor, eps: float):
        super().__init__()
        self.weight = torch.nn.Parameter(weight, requires_grad=False)
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        xf = x.float()
        xf = xf * torch.rsqrt(xf.pow(2).mean(-1, keepdim=True) + self.eps)
        return (self.weight * xf.to(x.dtype))


def _rope_cache(head_dim: int, max_pos: int, theta: float, device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
    inv = 1.0 / (theta ** (torch.arange(0, head_dim, 2, device=device, dtype=torch.float32) / head_dim))
    t = torch.arange(max_pos, device=device, dtype=torch.float32)
    freqs = torch.outer(t, inv)
    emb = torch.cat([freqs, freqs], dim=-1)
    return emb.cos(), emb.sin()


def _rotate_half(x: torch.Tensor) -> torch.Tensor:
    x1, x2 = x[..., : x.shape[-1] // 2], x[..., x.shape[-1] // 2 :]
    return torch.cat([-x2, x1], dim=-1)


class Qwen3Layer(torch.nn.Module):
    def __init__(self, w: dict[str, torch.Tensor], cfg: dict[str, Any]):
        super().__init__()
        eps = cfg["rms_norm_eps"]
        self.n_heads, self.n_kv, self.head_dim = cfg["num_attention_heads"], cfg["num_key_value_heads"], cfg["head_dim"]
        self.input_norm = RMSNorm(w["input_layernorm.weight"], eps)
        self.post_norm = RMSNorm(w["post_attention_layernorm.weight"], eps)
        self.q_norm = RMSNorm(w["self_attn.q_norm.weight"], eps)
        self.k_norm = RMSNorm(w["self_attn.k_norm.weight"], eps)
        P = lambda k: torch.nn.Parameter(w[k], requires_grad=False)
        self.q_proj, self.k_proj, self.v_proj, self.o_proj = P("self_attn.q_proj.weight"), P("self_attn.k_proj.weight"), P("self_attn.v_proj.weight"), P("self_attn.o_proj.weight")
        self.gate_proj, self.up_proj, self.down_proj = P("mlp.gate_proj.weight"), P("mlp.up_proj.weight"), P("mlp.down_proj.weight")

    def forward(self, x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor, k_cache: torch.Tensor, v_cache: torch.Tensor, pos: int, causal: bool) -> torch.Tensor:
        B, T, _ = x.shape
        h = self.input_norm(x)
        q = (h @ self.q_proj.T).view(B, T, self.n_heads, self.head_dim)
        k = (h @ self.k_proj.T).view(B, T, self.n_kv, self.head_dim)
        v = (h @ self.v_proj.T).view(B, T, self.n_kv, self.head_dim)
        q, k = self.q_norm(q), self.k_norm(k)
        q, k, v = q.transpose(1, 2), k.transpose(1, 2), v.transpose(1, 2)  # B, H, T, D
        c, s = cos[pos : pos + T].to(x.dtype), sin[pos : pos + T].to(x.dtype)
        q = q * c + _rotate_half(q) * s
        k = k * c + _rotate_half(k) * s
        k_cache[:, :, pos : pos + T] = k
        v_cache[:, :, pos : pos + T] = v
        K, V = k_cache[:, :, : pos + T], v_cache[:, :, : pos + T]
        attn = torch.nn.functional.scaled_dot_product_attention(q, K, V, is_causal=causal, enable_gqa=True)
        attn = attn.transpose(1, 2).reshape(B, T, -1)
        x = x + attn @ self.o_proj.T
        h = self.post_norm(x)
        x = x + (torch.nn.functional.silu(h @ self.gate_proj.T) * (h @ self.up_proj.T)) @ self.down_proj.T
        return x


class Qwen3Model:
    def __init__(self, model_dir: Path, device: torch.device, max_seq: int = 2048, dtype: torch.dtype = torch.bfloat16):
        self.cfg = json.loads((model_dir / "config.json").read_text())
        self.device, self.dtype, self.max_seq = device, dtype, max_seq
        index = json.loads((model_dir / "model.safetensors.index.json").read_text())
        files = {name: SafetensorsFile(model_dir / name) for name in set(index["weight_map"].values())}

        def get(name: str) -> torch.Tensor:
            return files[index["weight_map"][name]].tensor(name, device).to(dtype)

        self.embed = get("model.embed_tokens.weight")
        self.lm_head = get("lm_head.weight") if "lm_head.weight" in index["weight_map"] else self.embed
        self.norm = RMSNorm(get("model.norm.weight"), self.cfg["rms_norm_eps"])
        self.layers = []
        for i in range(self.cfg["num_hidden_layers"]):
            prefix = f"model.layers.{i}."
            w = {k[len(prefix):]: get(k) for k in index["weight_map"] if k.startswith(prefix)}
            self.layers.append(Qwen3Layer(w, self.cfg))
        self.cos, self.sin = _rope_cache(self.cfg["head_dim"], max_seq, self.cfg["rope_theta"], device)
        nkv, hd = self.cfg["num_key_value_heads"], self.cfg["head_dim"]
        self.k_cache = [torch.zeros((1, nkv, max_seq, hd), device=device, dtype=dtype) for _ in self.layers]
        self.v_cache = [torch.zeros((1, nkv, max_seq, hd), device=device, dtype=dtype) for _ in self.layers]
        self.param_bytes = sum(p.numel() * p.element_size() for l in self.layers for p in l.parameters()) + self.embed.numel() * 2 + (0 if self.lm_head is self.embed else self.lm_head.numel() * 2)

    @torch.inference_mode()
    def forward(self, ids: torch.Tensor, pos: int, *, range_prefix: str | None = None, index_base: int = 0, phase: str = "prefill", op_hook: Any = None) -> torch.Tensor:
        """Run ids (1, T) at cache position pos; returns logits of the last token.

        With range_prefix set, each stage is wrapped in an NVTX range named
        ``<range_prefix>::<index>::<op_type>`` and op_hook(index, op_type, start_ns, end_ns) is
        called after the range so the host trace mirrors the NVTX ranges 1:1.
        """
        import time

        T = ids.shape[1]
        causal = T > 1
        idx = index_base

        def run(op_type: str, fn: Any) -> Any:
            nonlocal idx
            if range_prefix is None:
                return fn()
            name = f"{range_prefix}::{idx}::{op_type}"
            start = time.monotonic_ns()
            torch.cuda.nvtx.range_push(name)
            try:
                out = fn()
            finally:
                torch.cuda.nvtx.range_pop()
            end = time.monotonic_ns()
            if op_hook is not None:
                op_hook(idx, op_type, start, end)
            idx += 1
            return out

        x = run(f"{phase}_embed", lambda: self.embed[ids])
        for i, layer in enumerate(self.layers):
            x = run(f"{phase}_layer{i:02d}", lambda: layer(x, self.cos, self.sin, self.k_cache[i], self.v_cache[i], pos, causal))
        logits = run(f"{phase}_head", lambda: self.norm(x[:, -1:]) @ self.lm_head.T)
        return logits[:, -1].float(), idx

    def ops_per_forward(self) -> int:
        return 2 + len(self.layers)


def validate(model_dir: Path, device: torch.device) -> dict[str, Any]:
    tok = ByteLevelBPE(model_dir)
    probe = "The capital of France is"
    ids = tok.encode(probe)
    assert tok.decode(ids) == probe, "tokenizer round-trip failed"
    model = Qwen3Model(model_dir, device)
    x = torch.tensor([ids], device=device)
    logits, _ = model.forward(x, 0)
    out = [int(logits.argmax())]
    for step in range(3):
        logits, _ = model.forward(torch.tensor([[out[-1]]], device=device), len(ids) + step)
        out.append(int(logits.argmax()))
    text = tok.decode(out)
    return {"probe": probe, "prompt_ids": ids, "generated_ids": out, "generated_text": text, "param_bytes": model.param_bytes, "pass": "Paris" in text}


if __name__ == "__main__":
    import sys

    torch.cuda.set_device(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    print(json.dumps(validate(Path(sys.argv[1]), torch.device("cuda")), indent=2))
