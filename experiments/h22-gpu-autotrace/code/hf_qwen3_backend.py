#!/usr/bin/env python3
"""Qwen3-1.7B backend for the h22 llm strand, on the user-supplied transformers.

Same interface as ``qwen3_local``'s ``Qwen3Model`` / ``ByteLevelBPE`` so the
runtime and the w01/w02 analyzers consume it unchanged:

  - ``forward(ids, pos, range_prefix=..., index_base=..., phase=..., op_hook=...)``
    emits one NVTX range + one op_hook event per forward stage, named
    ``<range_prefix>::<index>::<op_type>`` with op_type in
    ``{phase}_embed``, ``{phase}_layer{i:02d}``, ``{phase}_head`` (final norm
    folded into head, exactly like qwen3_local).
  - stages are delimited with forward pre/post hooks on the HF submodules, so
    no transformers-internal layer plumbing is reimplemented here.

No per-stage synchronize: ranges are host-side launch windows, kernels are
attributed by nsys through launch ownership.
"""

from __future__ import annotations

import glob
import sys
import time
from pathlib import Path
from typing import Any

import torch


def ensure_pynvml() -> None:
    """pynvml is absent from the conda env; borrow the pure-python module from .venv-gpu."""
    try:
        import pynvml  # noqa: F401
        return
    except ImportError:
        pass
    project_root = Path(__file__).resolve().parents[3]
    for sp in glob.glob(str(project_root / ".venv-gpu/lib/python*/site-packages")):
        if (Path(sp) / "pynvml.py").exists():
            sys.path.append(sp)
            import pynvml  # noqa: F401
            return
    raise ImportError("pynvml not found in conda env or .venv-gpu")


class HFTokenizer:
    def __init__(self, model_dir: Path):
        from transformers import AutoTokenizer

        self.tok = AutoTokenizer.from_pretrained(str(model_dir))

    def encode(self, text: str) -> list[int]:
        return self.tok.encode(text, add_special_tokens=False)

    def decode(self, ids: list[int]) -> str:
        return self.tok.decode(ids)


class HFQwen3Model:
    def __init__(self, model_dir: Path, device: torch.device, max_seq: int = 0, attn_implementation: str = "sdpa"):
        from transformers import AutoModelForCausalLM

        self.device = device
        self.attn_implementation = attn_implementation
        try:
            self.hf = AutoModelForCausalLM.from_pretrained(
                str(model_dir), dtype=torch.bfloat16, attn_implementation=attn_implementation
            ).to(device).eval()
        except ValueError:
            # vision-language checkpoints (e.g. Qwen2.5-VL); the agent calls are
            # text-only, so only the language tower is exercised.
            from transformers import AutoModelForImageTextToText

            self.hf = AutoModelForImageTextToText.from_pretrained(
                str(model_dir), dtype=torch.bfloat16, attn_implementation=attn_implementation
            ).to(device).eval()
        self.cfg = self.hf.config.to_dict()
        if "hidden_size" not in self.cfg and "text_config" in self.cfg:
            self.cfg = {**self.cfg["text_config"], **{k: v for k, v in self.cfg.items() if k != "text_config"}}
        self.cfg.setdefault("architectures", getattr(self.hf.config, "architectures", None))
        core = self.hf.model
        if not hasattr(core, "embed_tokens") and hasattr(core, "language_model"):
            core = core.language_model
        self.core = core
        self.layers = core.layers
        self.param_bytes = sum(p.numel() * p.element_size() for p in self.hf.parameters())
        # mutable per-forward state consumed by the hooks
        self._prefix: str | None = None
        self._phase = "prefill"
        self._index = 0
        self._op_hook: Any = None
        self._start_ns = 0
        self._cache: Any = None
        self._install_hooks()

    # -- stage delimiting -------------------------------------------------
    def _begin(self, op_type_fmt: str):
        def pre_hook(module, args, kwargs=None):
            if self._prefix is None:
                return
            self._stage_op_type = op_type_fmt.format(phase=self._phase)
            self._start_ns = time.monotonic_ns()
            torch.cuda.nvtx.range_push(f"{self._prefix}::{self._index}::{self._stage_op_type}")
        return pre_hook

    def _end(self):
        def post_hook(module, args, output):
            if self._prefix is None:
                return
            torch.cuda.nvtx.range_pop()
            if self._op_hook is not None:
                self._op_hook(self._index, self._stage_op_type, self._start_ns, time.monotonic_ns())
            self._index += 1
        return post_hook

    def _install_hooks(self) -> None:
        core = self.core
        core.embed_tokens.register_forward_pre_hook(self._begin("{phase}_embed"))
        core.embed_tokens.register_forward_hook(self._end())
        for i, layer in enumerate(core.layers):
            layer.register_forward_pre_hook(self._begin("{phase}_layer%02d" % i))
            layer.register_forward_hook(self._end())
        # final norm + lm_head folded into one "head" stage, like qwen3_local
        core.norm.register_forward_pre_hook(self._begin("{phase}_head"))
        self.hf.lm_head.register_forward_hook(self._end())

    # -- qwen3_local-compatible interface ---------------------------------
    @torch.inference_mode()
    def forward(self, ids: torch.Tensor, pos: int, *, range_prefix: str | None = None,
                index_base: int = 0, phase: str = "prefill", op_hook: Any = None):
        from transformers import DynamicCache

        if pos == 0:
            self._cache = DynamicCache()
        self._prefix, self._phase, self._index, self._op_hook = range_prefix, phase, index_base, op_hook
        try:
            out = self.hf(input_ids=ids, past_key_values=self._cache, use_cache=True)
        finally:
            index = self._index
            self._prefix = self._op_hook = None
        return out.logits[:, -1:], index

    def ops_per_forward(self) -> int:
        return 2 + len(self.layers)

    def probe(self, tok: HFTokenizer, prompt: str = "The capital of France is", n_tokens: int = 3) -> dict[str, Any]:
        ids = torch.tensor([tok.encode(prompt)], device=self.device)
        generated: list[int] = []
        pos = 0
        x = ids
        for _ in range(n_tokens):
            logits, _ = self.forward(x, pos)
            pos += x.shape[1]
            nxt = int(logits.argmax())
            generated.append(nxt)
            x = torch.tensor([[nxt]], device=self.device)
        text = tok.decode(generated)
        return {"pass": "Paris" in text, "prompt": prompt, "generated_text": text}
