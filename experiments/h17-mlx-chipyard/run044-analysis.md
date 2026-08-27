# H17.2 run-044 analysis — ordinary Rocket plus MLX

## Outcome

H17 and H17.2 are supported. Both Chipyard configurations build, four distinct
RISC-V ELFs execute on both, and all 12 system gates pass. All eight runs match
their software goldens and report ABI magic `0x4d4c5801`.

| workload | backend | host cycles | system | DMA | kernel | instructions | bytes |
|---|---|---:|---:|---:|---:|---:|---:|
| BSMM | cycle / RTL | 1456 / 1389 | 458 / 391 | 328 | 128 / 61 | 44 | 576 |
| FFT-CMP | cycle / RTL | 1214 / 1168 | 385 / 339 | 288 | 95 / 49 | 34 | 512 |
| SWA | cycle / RTL | 1038 / 1022 | 349 / 333 | 248 | 99 / 83 | 25 | 448 |
| Transformer | cycle / RTL | 1497 / 1441 | 478 / 422 | 344 | 132 / 76 | 45 | 576 |

The kernel cycles exactly equal fresh run 043, proving the RoCC wrapper does not
replace or retime the selected backend. Every record satisfies
`system = DMA + kernel + 2`; load/store/compute/xfer sum to instructions; DMA
bytes equal 64 times input+output vectors. Host `rdcycle` includes positive
configuration and launch/wait costs and is larger than controller system time.

Twelve installed Scala/RTL files byte-match active MLX. The active checkout
remains clean. This is real ordinary-Rocket bare-metal/custom0/HellaCache
simulation and consumes no paper target.
