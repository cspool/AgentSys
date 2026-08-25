# mllm run 005 analysis

## Result

Seven of eight locked gates pass. The backend consumes the pinned upstream mllm MIR files directly:

- FooNet: exactly four Linear ops, all mapped to ME.
- Qwen3-1.7B: exactly 160 selected executable ops, mapped to ME/VE/DE as 23/61/76; deterministic operator digest and dependency ordering pass.
- Decoder slice: static and dynamic consume identical ME/VE/DE work (48/12/4 cycles), and dynamic exposes cross-engine overlap.

The failed gate is `dynamic_faster`: static takes 64 cycles and dynamic 102 cycles (0.627×). Seven-cycle dispatch dominates because the initial duration estimator emits 2-cycle DE, 4-cycle VE, and 16-cycle ME tiles. That violates the TISA hardware regime: the paper/knowledge source specifies tile work at roughly 10³–10⁵ cycles so seven-cycle dispatch remains negligible.

## Direction

Retain run 005. Run 006 will change only the duration normalization to source-aligned minimum tile cycles, preserve shape ratios/op mapping/dependencies, and rerun the same MIR inputs. No paper performance target or observed run-005 speedup will select the scale.

