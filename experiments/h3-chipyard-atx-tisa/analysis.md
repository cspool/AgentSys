# H3 Chipyard run 003 analysis

## Result

The static and dynamic Rocket+Verilator configurations build successfully and the same bare-metal ELF passes all software checks on both. The automated artifact passes 17/17 system gates.

- Static: 332 backend cycles, 370 system cycles, zero engine-overlap cycles.
- Dynamic: 249 backend cycles, 287 system cycles, 79 pair-overlap cycles.
- Speedups: 1.333× backend, 1.289× system, 1.258× host launch/wait.
- Work conservation: 8 submitted = 8 issued = 8 completed; ME/VE/DE issues 2/2/4 and busy cycles 160/80/80 for both.
- Functional equivalence: 96 DMA bytes and checksum `a42f89ec1a613914` for both; software output reference matches.
- Safety/ABI: zero priority violations, prefetch 1/1, ABI magic checked, installed files byte-match project sources.

This supports the H3 mechanism direction in a real SoC simulator. It does not yet close ATX paper performance endpoints, mllm integration, or the unified program-to-engine trace.

