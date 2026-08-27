# H17.2 protocol — fresh MLX ordinary-Rocket system closure (run 044)

Locked before installing MLX sources into Chipyard, compiling ELFs or building
the two Rocket simulators.

## Fixed system

- Chipyard/Rocket commit: `b5d013190d637e634113cb5179f8c8885df1945a`.
- CPU: one ordinary big Rocket core; no ATX.
- Accelerator interface: custom0 `config/launch/wait/status` and HellaCache DMA.
- Backends: `MLXCycleRocketConfig` and `MLXRTLRocketConfig` from the exact active
  run-042 source.
- Workloads: the same four run-043 programs/inputs/goldens.
- Compiler: RISC-V GCC 9.2.0; outputs under
  `artifacts/mlx_chipyard/run_044`.

The installer may modify only the selected Chipyard overlay/resources and the
already-required compatibility patches. It must not modify the active MLX
checkout.

## Gates

1. All 12 installed Scala/RTL files byte-match active MLX sources.
2. Both Rocket simulators build successfully and are hashed.
3. Four distinct bare-metal ELFs build successfully and are hashed.
4. Eight simulator executions exit zero and report exact workload/backend
   identity with no golden mismatches.
5. Kernel cycles and instruction counts exactly match the corresponding fresh
   run-043 standalone backend.
6. Controller counters conserve load/store/compute/xfer work.
7. DMA bytes equal 64 bytes times input+output vectors and DMA cycles are nonzero.
8. `system_cycles = dma_cycles + kernel_cycles + 2` for all runs.
9. RISC-V `rdcycle` host config and launch/wait totals are positive and include
   controller work.
10. ABI magic, status backend bit and all artifact/log/source hashes pass.
11. Active MLX source remains clean and pinned after installation/execution.
12. Run 044 reads no paper performance target.

Passing run 044 supports H17 and unlocks Agent-specific MLX lowering.
