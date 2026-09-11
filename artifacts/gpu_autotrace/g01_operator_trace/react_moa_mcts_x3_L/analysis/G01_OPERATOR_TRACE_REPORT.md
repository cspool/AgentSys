# G01 operator-wise single-GPU trace: `react_moa_mcts_x3_L`

Lineage `h22-gpu-autotrace`, workflow w01. Real execution on one RTX 4090
(`0000:b1:00.0`), warmup 3 iterations discarded, 8 measured iterations. Attribution basis: NVTX operator range -> CUDA runtime API launched inside it -> CUPTI kernel/memcpy by correlationId.

## Conservation

| Quantity | Value |
|---|---:|
| Operator instances observed / expected | 1920 / 1920 |
| Measured wall per iteration (median) | 6,606,040.4 us |
| GPU busy per iteration (median, union of GPU intervals) | 50.3 % |
| Operator-owned GPU time (total over measured) | 25,931,652.4 us |
| Call-overhead GPU time (weight init, H2D/D2H, staging) | 655,418.3 us |
| Unattributed GPU items inside measured window | 0 (0.0 us) |
| Kernel launches over measured iterations | 146400 |
| Warmup iteration 0 wall | 7,166,107.8 us |
| Warmup GPU busy (median) | 50.6 % |
| Pass | True |

## Operator-type breakdown (measured iterations)

| op_type | instances | kernel launches | GPU total (us) | GPU share | NVTX CPU total (us) | wall share | GPU per instance (us) |
|---|---:|---:|---:|---:|---:|---:|---:|
| LinearOp | 720 | 23040 | 17,375,384.6 | 65.35 % | 17,490,508.4 | 32.98 % | 24,132.5 |
| RMSNormOp | 480 | 107520 | 6,786,648.1 | 25.53 % | 6,903,717.0 | 13.02 % | 14,138.9 |
| TransposeOp | 240 | 7680 | 1,634,155.3 | 6.15 % | 1,665,680.3 | 3.14 % | 6,809.0 |
| call_overhead | 240 | 480 | 655,418.3 | 2.47 % | 0.0 | 0.0 % | 2,730.9 |
| AddOp | 240 | 7680 | 135,464.4 | 0.51 % | 164,547.6 | 0.31 % | 564.4 |
| ViewOp | 240 | 0 | 0.0 | 0.0 % | 37,665.3 | 0.07 % | 0.0 |

## Kernel-family breakdown (measured iterations)

| family | instances | GPU total (us) | share |
|---|---:|---:|---:|
| gemm | 23040 | 17,352,501.3 | 65.27 % |
| copy | 38400 | 4,088,233.6 | 15.38 % |
| elementwise_unary | 30720 | 2,029,570.9 | 7.63 % |
| elementwise_binary | 38640 | 1,933,421.8 | 7.27 % |
| memcpy | 480 | 643,587.7 | 2.42 % |
| reduce | 15360 | 509,614.0 | 1.92 % |
| memset | 18432 | 22,883.3 | 0.09 % |
| rng_init | 240 | 7,258.1 | 0.03 % |

## Per-operator summary (measured iterations)

| call | idx | op_type | engine | GPU median (us) | GPU min/max (us) | NVTX CPU median (us) | GPU/CPU | kernels |
|---|---:|---|---|---:|---:|---:|---:|---:|
| mcts-actor0#r0 | 6 | RMSNormOp | ve | 15,874.6 | 15,815.3/16,288.6 | 16,141.3 | 98.4 % | 224 |
| mcts-actor0#r0 | 7 | AddOp | ve | 604.3 | 601.5/625.0 | 700.3 | 85.0 % | 32 |
| mcts-actor0#r0 | 8 | RMSNormOp | ve | 15,804.2 | 15,775.6/16,273.0 | 16,054.4 | 98.6 % | 224 |
| mcts-actor0#r0 | 10 | LinearOp | me | 25,798.7 | 25,534.1/25,892.3 | 26,033.2 | 99.1 % | 32 |
| mcts-actor0#r0 | 11 | LinearOp | me | 26,541.2 | 25,957.5/26,988.2 | 26,678.5 | 99.4 % | 32 |
| mcts-actor0#r0 | 12 | LinearOp | me | 26,585.1 | 25,961.5/27,240.3 | 26,758.5 | 99.4 % | 32 |
| mcts-actor0#r0 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 150.2 | 0.0 % | 0 |
| mcts-actor0#r0 | 14 | TransposeOp | de | 7,282.9 | 6,846.7/7,690.8 | 7,411.2 | 97.9 % | 32 |
| mcts-actor0#r0 |  | call_overhead |  | 2,877.3 | 2,845.3/3,111.6 |  |  % | 2 |
| mcts-actor0#r1 | 6 | RMSNormOp | ve | 16,193.3 | 15,805.1/16,320.5 | 16,447.2 | 98.4 % | 224 |
| mcts-actor0#r1 | 7 | AddOp | ve | 604.8 | 603.2/644.4 | 706.9 | 86.1 % | 32 |
| mcts-actor0#r1 | 8 | RMSNormOp | ve | 15,993.2 | 15,772.8/16,253.2 | 16,210.8 | 98.7 % | 224 |
| mcts-actor0#r1 | 10 | LinearOp | me | 25,895.5 | 25,527.1/26,191.3 | 26,082.0 | 99.3 % | 32 |
| mcts-actor0#r1 | 11 | LinearOp | me | 26,171.6 | 25,874.2/26,901.6 | 26,298.6 | 99.5 % | 32 |
| mcts-actor0#r1 | 12 | LinearOp | me | 26,305.4 | 25,707.1/27,704.8 | 26,455.6 | 99.4 % | 32 |
| mcts-actor0#r1 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 160.9 | 0.0 % | 0 |
| mcts-actor0#r1 | 14 | TransposeOp | de | 7,211.8 | 6,911.6/7,273.9 | 7,353.9 | 98.2 % | 32 |
| mcts-actor0#r1 |  | call_overhead |  | 2,947.8 | 2,868.4/3,395.2 |  |  % | 2 |
| mcts-actor0#r2 | 6 | RMSNormOp | ve | 15,829.6 | 15,789.6/16,261.2 | 16,081.3 | 97.6 % | 224 |
| mcts-actor0#r2 | 7 | AddOp | ve | 603.9 | 601.5/646.5 | 718.1 | 85.0 % | 32 |
| mcts-actor0#r2 | 8 | RMSNormOp | ve | 16,155.7 | 15,786.3/16,293.1 | 16,389.9 | 98.7 % | 224 |
| mcts-actor0#r2 | 10 | LinearOp | me | 25,831.2 | 25,539.2/26,174.4 | 26,032.4 | 99.2 % | 32 |
| mcts-actor0#r2 | 11 | LinearOp | me | 26,461.4 | 25,610.3/26,945.3 | 26,606.8 | 99.4 % | 32 |
| mcts-actor0#r2 | 12 | LinearOp | me | 26,927.1 | 26,339.0/27,207.3 | 27,113.3 | 99.4 % | 32 |
| mcts-actor0#r2 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 150.8 | 0.0 % | 0 |
| mcts-actor0#r2 | 14 | TransposeOp | de | 7,223.3 | 7,172.1/7,733.0 | 7,357.2 | 98.3 % | 32 |
| mcts-actor0#r2 |  | call_overhead |  | 2,900.1 | 2,851.8/2,986.1 |  |  % | 2 |
| mcts-actor1#r0 | 6 | RMSNormOp | ve | 16,263.8 | 15,829.4/16,386.3 | 16,531.7 | 98.3 % | 224 |
| mcts-actor1#r0 | 7 | AddOp | ve | 603.4 | 601.9/606.5 | 703.0 | 86.0 % | 32 |
| mcts-actor1#r0 | 8 | RMSNormOp | ve | 15,820.5 | 15,796.8/16,188.6 | 16,039.8 | 98.7 % | 224 |
| mcts-actor1#r0 | 10 | LinearOp | me | 25,686.9 | 25,508.4/25,897.0 | 25,915.1 | 99.2 % | 32 |
| mcts-actor1#r0 | 11 | LinearOp | me | 26,197.0 | 25,589.7/26,987.4 | 26,413.7 | 99.3 % | 32 |
| mcts-actor1#r0 | 12 | LinearOp | me | 26,787.8 | 26,353.4/27,156.6 | 26,938.7 | 99.4 % | 32 |
| mcts-actor1#r0 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 149.7 | 0.0 % | 0 |
| mcts-actor1#r0 | 14 | TransposeOp | de | 7,247.6 | 6,865.7/7,671.5 | 7,386.9 | 98.1 % | 32 |
| mcts-actor1#r0 |  | call_overhead |  | 2,892.7 | 2,833.3/2,969.7 |  |  % | 2 |
| mcts-actor1#r1 | 6 | RMSNormOp | ve | 16,133.0 | 15,832.5/16,216.0 | 16,396.9 | 98.4 % | 224 |
| mcts-actor1#r1 | 7 | AddOp | ve | 607.5 | 599.6/648.7 | 715.2 | 85.7 % | 32 |
| mcts-actor1#r1 | 8 | RMSNormOp | ve | 15,987.1 | 15,781.9/16,308.3 | 16,223.9 | 98.6 % | 224 |
| mcts-actor1#r1 | 10 | LinearOp | me | 25,747.0 | 25,539.1/25,894.7 | 25,931.9 | 99.2 % | 32 |
| mcts-actor1#r1 | 11 | LinearOp | me | 26,115.5 | 25,585.2/26,971.3 | 26,257.5 | 99.4 % | 32 |
| mcts-actor1#r1 | 12 | LinearOp | me | 26,933.6 | 26,362.3/27,515.5 | 27,097.0 | 99.4 % | 32 |
| mcts-actor1#r1 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 158.1 | 0.0 % | 0 |
| mcts-actor1#r1 | 14 | TransposeOp | de | 7,222.7 | 7,178.6/7,650.4 | 7,354.9 | 98.2 % | 32 |
| mcts-actor1#r1 |  | call_overhead |  | 2,870.2 | 2,832.3/2,952.4 |  |  % | 2 |
| mcts-actor1#r2 | 6 | RMSNormOp | ve | 15,850.8 | 15,808.4/16,272.2 | 16,095.8 | 98.4 % | 224 |
| mcts-actor1#r2 | 7 | AddOp | ve | 612.1 | 600.2/724.6 | 704.0 | 86.3 % | 32 |
| mcts-actor1#r2 | 8 | RMSNormOp | ve | 15,816.6 | 15,780.3/16,296.3 | 16,079.5 | 98.6 % | 224 |
| mcts-actor1#r2 | 10 | LinearOp | me | 26,025.2 | 25,515.4/26,219.6 | 26,207.5 | 99.3 % | 32 |
| mcts-actor1#r2 | 11 | LinearOp | me | 26,093.2 | 25,671.2/26,697.1 | 26,248.8 | 99.4 % | 32 |
| mcts-actor1#r2 | 12 | LinearOp | me | 26,739.4 | 26,029.4/27,486.7 | 26,895.5 | 99.4 % | 32 |
| mcts-actor1#r2 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 155.5 | 0.0 % | 0 |
| mcts-actor1#r2 | 14 | TransposeOp | de | 7,221.4 | 6,876.2/7,681.9 | 7,352.6 | 98.2 % | 32 |
| mcts-actor1#r2 |  | call_overhead |  | 2,911.6 | 2,855.0/3,081.0 |  |  % | 2 |
| mcts-critic#r0 | 6 | RMSNormOp | ve | 16,146.6 | 15,810.5/16,307.0 | 16,402.0 | 98.4 % | 224 |
| mcts-critic#r0 | 7 | AddOp | ve | 603.5 | 600.1/631.3 | 701.8 | 85.9 % | 32 |
| mcts-critic#r0 | 8 | RMSNormOp | ve | 16,158.6 | 15,798.7/16,291.9 | 16,368.6 | 98.7 % | 224 |
| mcts-critic#r0 | 10 | LinearOp | me | 25,876.1 | 25,548.8/26,213.0 | 26,099.9 | 99.2 % | 32 |
| mcts-critic#r0 | 11 | LinearOp | me | 25,902.8 | 25,706.5/26,968.4 | 26,064.4 | 99.4 % | 32 |
| mcts-critic#r0 | 12 | LinearOp | me | 26,538.7 | 26,201.8/27,183.0 | 26,672.7 | 99.5 % | 32 |
| mcts-critic#r0 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 163.1 | 0.0 % | 0 |
| mcts-critic#r0 | 14 | TransposeOp | de | 7,259.0 | 7,182.9/7,740.9 | 7,410.7 | 98.0 % | 32 |
| mcts-critic#r0 |  | call_overhead |  | 2,528.7 | 2,506.5/2,590.4 |  |  % | 2 |
| mcts-critic#r1 | 6 | RMSNormOp | ve | 16,194.9 | 15,815.4/16,299.8 | 16,452.9 | 98.4 % | 224 |
| mcts-critic#r1 | 7 | AddOp | ve | 604.9 | 601.8/621.7 | 705.3 | 85.2 % | 32 |
| mcts-critic#r1 | 8 | RMSNormOp | ve | 15,823.0 | 15,784.2/16,183.1 | 16,037.0 | 98.7 % | 224 |
| mcts-critic#r1 | 10 | LinearOp | me | 25,560.8 | 25,493.8/25,891.1 | 25,765.1 | 99.2 % | 32 |
| mcts-critic#r1 | 11 | LinearOp | me | 26,432.8 | 25,913.4/26,817.7 | 26,591.6 | 99.4 % | 32 |
| mcts-critic#r1 | 12 | LinearOp | me | 26,797.1 | 25,765.0/27,402.1 | 26,922.6 | 99.5 % | 32 |
| mcts-critic#r1 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 147.3 | 0.0 % | 0 |
| mcts-critic#r1 | 14 | TransposeOp | de | 7,442.8 | 7,171.5/7,761.8 | 7,563.7 | 98.4 % | 32 |
| mcts-critic#r1 |  | call_overhead |  | 2,556.6 | 2,521.2/2,722.3 |  |  % | 2 |
| mcts-critic#r2 | 6 | RMSNormOp | ve | 16,204.2 | 15,826.2/16,276.6 | 16,479.0 | 98.4 % | 224 |
| mcts-critic#r2 | 7 | AddOp | ve | 605.4 | 599.6/725.1 | 713.1 | 85.6 % | 32 |
| mcts-critic#r2 | 8 | RMSNormOp | ve | 15,807.4 | 15,773.4/16,210.1 | 16,028.5 | 98.5 % | 224 |
| mcts-critic#r2 | 10 | LinearOp | me | 25,874.0 | 25,522.1/26,198.5 | 26,076.4 | 99.2 % | 32 |
| mcts-critic#r2 | 11 | LinearOp | me | 25,981.8 | 25,612.9/26,782.8 | 26,143.6 | 99.4 % | 32 |
| mcts-critic#r2 | 12 | LinearOp | me | 26,802.5 | 25,666.8/27,307.6 | 26,947.1 | 99.5 % | 32 |
| mcts-critic#r2 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 156.9 | 0.0 % | 0 |
| mcts-critic#r2 | 14 | TransposeOp | de | 7,281.3 | 6,762.6/7,695.1 | 7,411.4 | 98.2 % | 32 |
| mcts-critic#r2 |  | call_overhead |  | 3,966.0 | 3,944.5/4,210.7 |  |  % | 2 |
| mcts-root#r0 | 6 | RMSNormOp | ve | 15,825.2 | 15,801.2/16,273.1 | 16,112.2 | 98.4 % | 224 |
| mcts-root#r0 | 7 | AddOp | ve | 604.4 | 602.1/606.9 | 699.5 | 80.9 % | 32 |
| mcts-root#r0 | 8 | RMSNormOp | ve | 15,807.0 | 15,784.0/16,258.4 | 16,062.0 | 98.6 % | 224 |
| mcts-root#r0 | 10 | LinearOp | me | 25,851.5 | 25,537.2/26,205.4 | 26,047.7 | 99.2 % | 32 |
| mcts-root#r0 | 11 | LinearOp | me | 26,263.1 | 25,660.5/26,562.5 | 26,405.4 | 99.4 % | 32 |
| mcts-root#r0 | 12 | LinearOp | me | 26,638.1 | 26,051.6/27,469.7 | 26,809.6 | 99.3 % | 32 |
| mcts-root#r0 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 157.1 | 0.0 % | 0 |
| mcts-root#r0 | 14 | TransposeOp | de | 7,221.8 | 6,952.4/7,766.3 | 7,357.2 | 98.2 % | 32 |
| mcts-root#r0 |  | call_overhead |  | 2,880.7 | 2,845.2/3,052.1 |  |  % | 2 |
| mcts-root#r1 | 6 | RMSNormOp | ve | 15,835.9 | 15,807.5/16,291.5 | 16,099.2 | 98.4 % | 224 |
| mcts-root#r1 | 7 | AddOp | ve | 604.1 | 601.0/605.6 | 701.1 | 80.2 % | 32 |
| mcts-root#r1 | 8 | RMSNormOp | ve | 16,126.1 | 15,763.3/16,240.3 | 16,336.8 | 98.7 % | 224 |
| mcts-root#r1 | 10 | LinearOp | me | 25,882.3 | 25,529.4/26,207.5 | 26,086.2 | 99.2 % | 32 |
| mcts-root#r1 | 11 | LinearOp | me | 26,402.7 | 25,701.0/26,891.0 | 26,532.3 | 99.4 % | 32 |
| mcts-root#r1 | 12 | LinearOp | me | 26,833.7 | 25,682.8/27,759.8 | 27,061.4 | 99.4 % | 32 |
| mcts-root#r1 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 154.2 | 0.0 % | 0 |
| mcts-root#r1 | 14 | TransposeOp | de | 7,220.1 | 7,171.9/7,696.1 | 7,367.8 | 98.2 % | 32 |
| mcts-root#r1 |  | call_overhead |  | 2,906.2 | 2,847.6/3,181.8 |  |  % | 2 |
| mcts-root#r2 | 6 | RMSNormOp | ve | 16,020.2 | 15,830.7/16,220.4 | 16,278.6 | 98.4 % | 224 |
| mcts-root#r2 | 7 | AddOp | ve | 603.2 | 601.6/622.6 | 708.5 | 84.4 % | 32 |
| mcts-root#r2 | 8 | RMSNormOp | ve | 15,989.9 | 15,797.9/16,289.5 | 16,202.9 | 98.7 % | 224 |
| mcts-root#r2 | 10 | LinearOp | me | 25,831.8 | 25,519.8/26,193.4 | 26,021.7 | 99.3 % | 32 |
| mcts-root#r2 | 11 | LinearOp | me | 25,966.4 | 25,618.2/26,483.9 | 26,106.3 | 99.5 % | 32 |
| mcts-root#r2 | 12 | LinearOp | me | 26,765.4 | 26,042.5/27,224.1 | 26,912.0 | 99.5 % | 32 |
| mcts-root#r2 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 151.5 | 0.0 % | 0 |
| mcts-root#r2 | 14 | TransposeOp | de | 7,249.0 | 7,039.5/7,789.7 | 7,385.3 | 98.3 % | 32 |
| mcts-root#r2 |  | call_overhead |  | 2,885.0 | 2,854.5/3,350.7 |  |  % | 2 |
| moa-map0#r0 | 6 | RMSNormOp | ve | 16,181.0 | 15,828.5/16,289.6 | 16,422.7 | 98.5 % | 224 |
| moa-map0#r0 | 7 | AddOp | ve | 603.6 | 600.1/606.9 | 696.7 | 86.5 % | 32 |
| moa-map0#r0 | 8 | RMSNormOp | ve | 15,799.7 | 15,791.8/16,278.7 | 16,015.6 | 98.7 % | 224 |
| moa-map0#r0 | 10 | LinearOp | me | 25,873.6 | 25,511.2/26,178.7 | 26,070.8 | 99.3 % | 32 |
| moa-map0#r0 | 11 | LinearOp | me | 26,612.4 | 25,615.6/26,997.5 | 26,765.6 | 99.4 % | 32 |
| moa-map0#r0 | 12 | LinearOp | me | 27,038.2 | 26,066.1/27,230.7 | 27,209.9 | 99.4 % | 32 |
| moa-map0#r0 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 145.9 | 0.0 % | 0 |
| moa-map0#r0 | 14 | TransposeOp | de | 7,201.1 | 7,172.0/7,703.7 | 7,329.1 | 98.3 % | 32 |
| moa-map0#r0 |  | call_overhead |  | 2,285.2 | 2,230.6/2,345.4 |  |  % | 2 |
| moa-map0#r1 | 6 | RMSNormOp | ve | 15,879.6 | 15,804.6/16,277.8 | 16,151.3 | 98.4 % | 224 |
| moa-map0#r1 | 7 | AddOp | ve | 605.3 | 602.6/625.8 | 699.3 | 85.5 % | 32 |
| moa-map0#r1 | 8 | RMSNormOp | ve | 15,851.5 | 15,800.7/16,284.2 | 16,073.7 | 98.7 % | 224 |
| moa-map0#r1 | 10 | LinearOp | me | 25,728.9 | 25,510.8/26,137.5 | 25,923.0 | 99.2 % | 32 |
| moa-map0#r1 | 11 | LinearOp | me | 26,459.9 | 25,571.1/27,252.4 | 26,600.1 | 99.4 % | 32 |
| moa-map0#r1 | 12 | LinearOp | me | 26,713.4 | 25,997.0/27,126.9 | 26,881.6 | 99.4 % | 32 |
| moa-map0#r1 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 159.0 | 0.0 % | 0 |
| moa-map0#r1 | 14 | TransposeOp | de | 7,294.4 | 6,887.6/7,681.3 | 7,427.4 | 98.3 % | 32 |
| moa-map0#r1 |  | call_overhead |  | 2,300.5 | 2,250.0/2,764.5 |  |  % | 2 |
| moa-map0#r2 | 6 | RMSNormOp | ve | 15,826.5 | 15,801.9/16,169.9 | 16,076.3 | 98.5 % | 224 |
| moa-map0#r2 | 7 | AddOp | ve | 607.5 | 603.3/734.2 | 700.1 | 86.1 % | 32 |
| moa-map0#r2 | 8 | RMSNormOp | ve | 15,837.7 | 15,799.3/16,314.5 | 16,087.2 | 98.6 % | 224 |
| moa-map0#r2 | 10 | LinearOp | me | 25,864.7 | 25,511.6/26,247.8 | 26,053.8 | 99.2 % | 32 |
| moa-map0#r2 | 11 | LinearOp | me | 25,981.5 | 25,625.3/26,769.2 | 26,114.7 | 99.5 % | 32 |
| moa-map0#r2 | 12 | LinearOp | me | 26,629.8 | 25,978.4/27,093.8 | 26,753.6 | 99.5 % | 32 |
| moa-map0#r2 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 145.5 | 0.0 % | 0 |
| moa-map0#r2 | 14 | TransposeOp | de | 7,222.3 | 6,854.1/7,704.3 | 7,339.0 | 98.3 % | 32 |
| moa-map0#r2 |  | call_overhead |  | 2,249.6 | 2,229.5/2,377.8 |  |  % | 2 |
| moa-map1#r0 | 6 | RMSNormOp | ve | 15,836.9 | 15,806.1/16,304.3 | 16,101.1 | 98.4 % | 224 |
| moa-map1#r0 | 7 | AddOp | ve | 604.8 | 600.5/701.7 | 713.4 | 85.6 % | 32 |
| moa-map1#r0 | 8 | RMSNormOp | ve | 15,963.9 | 15,796.7/16,318.0 | 16,220.9 | 98.6 % | 224 |
| moa-map1#r0 | 10 | LinearOp | me | 25,857.6 | 25,510.1/26,184.0 | 26,039.2 | 99.2 % | 32 |
| moa-map1#r0 | 11 | LinearOp | me | 26,095.3 | 25,907.6/26,900.6 | 26,256.8 | 99.5 % | 32 |
| moa-map1#r0 | 12 | LinearOp | me | 26,705.9 | 25,732.5/27,232.7 | 26,855.5 | 99.5 % | 32 |
| moa-map1#r0 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 152.8 | 0.0 % | 0 |
| moa-map1#r0 | 14 | TransposeOp | de | 7,207.2 | 6,765.2/7,703.7 | 7,337.8 | 98.3 % | 32 |
| moa-map1#r0 |  | call_overhead |  | 2,876.8 | 2,833.2/3,072.5 |  |  % | 2 |
| moa-map1#r1 | 6 | RMSNormOp | ve | 15,996.1 | 15,797.7/16,307.2 | 16,261.6 | 98.4 % | 224 |
| moa-map1#r1 | 7 | AddOp | ve | 605.8 | 601.5/607.4 | 703.4 | 86.3 % | 32 |
| moa-map1#r1 | 8 | RMSNormOp | ve | 16,099.6 | 15,784.8/16,291.1 | 16,318.8 | 98.6 % | 224 |
| moa-map1#r1 | 10 | LinearOp | me | 25,821.5 | 25,569.4/25,994.3 | 26,004.7 | 99.2 % | 32 |
| moa-map1#r1 | 11 | LinearOp | me | 26,750.0 | 25,906.1/26,877.0 | 26,897.7 | 99.4 % | 32 |
| moa-map1#r1 | 12 | LinearOp | me | 26,769.1 | 25,997.3/27,557.5 | 26,905.1 | 99.5 % | 32 |
| moa-map1#r1 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 149.4 | 0.0 % | 0 |
| moa-map1#r1 | 14 | TransposeOp | de | 7,221.3 | 7,138.5/7,612.4 | 7,348.8 | 98.2 % | 32 |
| moa-map1#r1 |  | call_overhead |  | 2,890.5 | 2,838.7/2,975.0 |  |  % | 2 |
| moa-map1#r2 | 6 | RMSNormOp | ve | 15,852.9 | 15,816.1/16,292.6 | 16,114.7 | 98.3 % | 224 |
| moa-map1#r2 | 7 | AddOp | ve | 603.4 | 599.5/611.4 | 710.0 | 85.4 % | 32 |
| moa-map1#r2 | 8 | RMSNormOp | ve | 16,148.9 | 15,774.0/16,216.3 | 16,366.8 | 98.6 % | 224 |
| moa-map1#r2 | 10 | LinearOp | me | 25,717.8 | 25,513.0/25,893.9 | 25,936.6 | 99.2 % | 32 |
| moa-map1#r2 | 11 | LinearOp | me | 26,123.7 | 25,612.2/26,719.4 | 26,285.1 | 99.4 % | 32 |
| moa-map1#r2 | 12 | LinearOp | me | 26,820.4 | 25,716.7/27,168.0 | 27,033.6 | 99.4 % | 32 |
| moa-map1#r2 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 145.5 | 0.0 % | 0 |
| moa-map1#r2 | 14 | TransposeOp | de | 7,222.2 | 6,896.8/7,629.4 | 7,352.8 | 98.3 % | 32 |
| moa-map1#r2 |  | call_overhead |  | 2,925.2 | 2,878.2/3,001.1 |  |  % | 2 |
| moa-map2#r0 | 6 | RMSNormOp | ve | 15,836.0 | 15,793.3/16,189.7 | 16,087.0 | 98.4 % | 224 |
| moa-map2#r0 | 7 | AddOp | ve | 603.2 | 600.9/646.4 | 708.3 | 85.2 % | 32 |
| moa-map2#r0 | 8 | RMSNormOp | ve | 16,174.0 | 15,791.3/16,219.1 | 16,406.3 | 98.6 % | 224 |
| moa-map2#r0 | 10 | LinearOp | me | 25,850.7 | 25,519.5/25,949.7 | 26,040.3 | 99.2 % | 32 |
| moa-map2#r0 | 11 | LinearOp | me | 26,489.3 | 25,599.6/26,987.6 | 26,689.0 | 99.4 % | 32 |
| moa-map2#r0 | 12 | LinearOp | me | 26,763.0 | 26,194.7/27,127.1 | 26,917.4 | 99.4 % | 32 |
| moa-map2#r0 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 154.9 | 0.0 % | 0 |
| moa-map2#r0 | 14 | TransposeOp | de | 7,222.1 | 7,171.8/7,666.4 | 7,401.0 | 98.1 % | 32 |
| moa-map2#r0 |  | call_overhead |  | 2,938.0 | 2,875.1/3,020.7 |  |  % | 2 |
| moa-map2#r1 | 6 | RMSNormOp | ve | 15,969.1 | 15,809.7/16,320.7 | 16,232.8 | 98.4 % | 224 |
| moa-map2#r1 | 7 | AddOp | ve | 604.4 | 601.8/645.7 | 705.7 | 85.9 % | 32 |
| moa-map2#r1 | 8 | RMSNormOp | ve | 15,818.9 | 15,805.5/16,206.5 | 16,053.8 | 98.6 % | 224 |
| moa-map2#r1 | 10 | LinearOp | me | 25,844.3 | 25,539.7/25,899.5 | 26,038.5 | 99.2 % | 32 |
| moa-map2#r1 | 11 | LinearOp | me | 25,991.1 | 25,598.4/27,237.2 | 26,134.0 | 99.4 % | 32 |
| moa-map2#r1 | 12 | LinearOp | me | 26,852.6 | 26,008.7/27,446.6 | 27,021.1 | 99.4 % | 32 |
| moa-map2#r1 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 149.6 | 0.0 % | 0 |
| moa-map2#r1 | 14 | TransposeOp | de | 7,244.3 | 7,173.3/7,281.1 | 7,374.0 | 98.1 % | 32 |
| moa-map2#r1 |  | call_overhead |  | 2,920.2 | 2,849.5/3,105.1 |  |  % | 2 |
| moa-map2#r2 | 6 | RMSNormOp | ve | 15,861.0 | 15,811.3/16,250.4 | 16,115.6 | 98.5 % | 224 |
| moa-map2#r2 | 7 | AddOp | ve | 604.9 | 600.0/623.7 | 700.3 | 85.0 % | 32 |
| moa-map2#r2 | 8 | RMSNormOp | ve | 15,839.5 | 15,788.8/16,549.1 | 16,053.4 | 98.7 % | 224 |
| moa-map2#r2 | 10 | LinearOp | me | 25,824.0 | 25,522.3/25,919.3 | 26,030.6 | 99.2 % | 32 |
| moa-map2#r2 | 11 | LinearOp | me | 26,459.1 | 25,611.9/26,775.5 | 26,618.3 | 99.4 % | 32 |
| moa-map2#r2 | 12 | LinearOp | me | 26,772.9 | 26,031.6/27,382.1 | 26,934.0 | 99.4 % | 32 |
| moa-map2#r2 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 154.1 | 0.0 % | 0 |
| moa-map2#r2 | 14 | TransposeOp | de | 7,222.1 | 6,959.4/7,694.3 | 7,343.4 | 98.1 % | 32 |
| moa-map2#r2 |  | call_overhead |  | 2,866.6 | 2,839.8/3,013.8 |  |  % | 2 |
| moa-reduce#r0 | 6 | RMSNormOp | ve | 16,021.9 | 15,817.9/16,215.6 | 16,284.2 | 98.4 % | 224 |
| moa-reduce#r0 | 7 | AddOp | ve | 606.0 | 600.1/609.8 | 704.5 | 86.1 % | 32 |
| moa-reduce#r0 | 8 | RMSNormOp | ve | 15,817.5 | 15,778.2/16,255.5 | 16,042.1 | 98.7 % | 224 |
| moa-reduce#r0 | 10 | LinearOp | me | 25,878.5 | 25,496.8/26,196.0 | 26,065.2 | 99.2 % | 32 |
| moa-reduce#r0 | 11 | LinearOp | me | 26,086.2 | 25,658.0/26,948.3 | 26,245.3 | 99.4 % | 32 |
| moa-reduce#r0 | 12 | LinearOp | me | 26,692.5 | 26,451.6/27,182.9 | 26,856.5 | 99.5 % | 32 |
| moa-reduce#r0 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 149.0 | 0.0 % | 0 |
| moa-reduce#r0 | 14 | TransposeOp | de | 7,272.9 | 7,078.8/7,337.7 | 7,393.4 | 98.3 % | 32 |
| moa-reduce#r0 |  | call_overhead |  | 2,867.4 | 2,857.1/2,971.1 |  |  % | 2 |
| moa-reduce#r1 | 6 | RMSNormOp | ve | 16,185.3 | 15,836.0/16,271.4 | 16,436.5 | 98.4 % | 224 |
| moa-reduce#r1 | 7 | AddOp | ve | 605.8 | 600.5/644.5 | 703.6 | 85.7 % | 32 |
| moa-reduce#r1 | 8 | RMSNormOp | ve | 16,112.7 | 15,785.5/16,306.6 | 16,319.5 | 98.7 % | 224 |
| moa-reduce#r1 | 10 | LinearOp | me | 25,882.0 | 25,531.3/25,910.1 | 26,073.3 | 99.3 % | 32 |
| moa-reduce#r1 | 11 | LinearOp | me | 26,435.8 | 25,631.2/26,859.1 | 26,570.3 | 99.4 % | 32 |
| moa-reduce#r1 | 12 | LinearOp | me | 26,784.1 | 25,992.4/27,163.5 | 26,943.8 | 99.5 % | 32 |
| moa-reduce#r1 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 148.6 | 0.0 % | 0 |
| moa-reduce#r1 | 14 | TransposeOp | de | 7,224.3 | 7,172.2/7,334.5 | 7,359.3 | 98.3 % | 32 |
| moa-reduce#r1 |  | call_overhead |  | 2,933.1 | 2,884.6/2,976.4 |  |  % | 2 |
| moa-reduce#r2 | 6 | RMSNormOp | ve | 15,837.3 | 15,801.7/16,217.7 | 16,090.0 | 98.4 % | 224 |
| moa-reduce#r2 | 7 | AddOp | ve | 604.6 | 603.1/606.4 | 701.6 | 85.6 % | 32 |
| moa-reduce#r2 | 8 | RMSNormOp | ve | 16,099.7 | 15,786.2/16,278.3 | 16,311.9 | 98.7 % | 224 |
| moa-reduce#r2 | 10 | LinearOp | me | 25,849.6 | 25,576.3/26,211.7 | 26,058.9 | 99.2 % | 32 |
| moa-reduce#r2 | 11 | LinearOp | me | 26,267.9 | 25,606.6/26,895.6 | 26,449.7 | 99.4 % | 32 |
| moa-reduce#r2 | 12 | LinearOp | me | 26,943.4 | 26,349.1/27,245.7 | 27,083.0 | 99.3 % | 32 |
| moa-reduce#r2 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 169.2 | 0.0 % | 0 |
| moa-reduce#r2 | 14 | TransposeOp | de | 7,227.5 | 7,076.4/7,695.3 | 7,357.4 | 97.8 % | 32 |
| moa-reduce#r2 |  | call_overhead |  | 2,932.9 | 2,855.4/3,085.2 |  |  % | 2 |
| react-answer#r0 | 6 | RMSNormOp | ve | 9,215.1 | 9,190.4/9,622.3 | 9,471.9 | 97.4 % | 224 |
| react-answer#r0 | 7 | AddOp | ve | 432.6 | 431.7/435.3 | 541.4 | 79.1 % | 32 |
| react-answer#r0 | 8 | RMSNormOp | ve | 9,162.3 | 9,115.4/9,625.7 | 9,376.2 | 97.8 % | 224 |
| react-answer#r0 | 10 | LinearOp | me | 19,550.1 | 19,498.9/19,882.6 | 19,708.3 | 99.2 % | 32 |
| react-answer#r0 | 11 | LinearOp | me | 19,853.5 | 19,656.8/19,918.0 | 19,951.0 | 99.5 % | 32 |
| react-answer#r0 | 12 | LinearOp | me | 19,790.8 | 19,477.3/20,570.9 | 19,902.0 | 99.5 % | 32 |
| react-answer#r0 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 143.6 | 0.0 % | 0 |
| react-answer#r0 | 14 | TransposeOp | de | 5,628.2 | 5,318.1/6,259.6 | 5,756.0 | 97.9 % | 32 |
| react-answer#r0 |  | call_overhead |  | 2,554.4 | 2,507.3/2,827.5 |  |  % | 2 |
| react-answer#r1 | 6 | RMSNormOp | ve | 9,208.6 | 9,168.8/9,595.6 | 9,452.0 | 97.4 % | 224 |
| react-answer#r1 | 7 | AddOp | ve | 433.4 | 428.0/481.9 | 569.2 | 77.8 % | 32 |
| react-answer#r1 | 8 | RMSNormOp | ve | 9,507.1 | 9,138.8/9,595.7 | 9,714.7 | 97.8 % | 224 |
| react-answer#r1 | 10 | LinearOp | me | 19,516.5 | 19,495.5/19,572.2 | 19,668.9 | 99.1 % | 32 |
| react-answer#r1 | 11 | LinearOp | me | 19,770.0 | 19,574.8/20,322.5 | 19,894.0 | 99.4 % | 32 |
| react-answer#r1 | 12 | LinearOp | me | 20,284.9 | 19,507.9/20,696.3 | 20,398.7 | 99.5 % | 32 |
| react-answer#r1 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 150.7 | 0.0 % | 0 |
| react-answer#r1 | 14 | TransposeOp | de | 5,742.3 | 5,328.5/5,833.6 | 5,878.5 | 97.8 % | 32 |
| react-answer#r1 |  | call_overhead |  | 2,571.3 | 2,502.2/3,025.2 |  |  % | 2 |
| react-answer#r2 | 6 | RMSNormOp | ve | 9,226.5 | 9,183.2/9,674.5 | 9,478.4 | 97.4 % | 224 |
| react-answer#r2 | 7 | AddOp | ve | 432.5 | 431.6/433.9 | 567.1 | 77.0 % | 32 |
| react-answer#r2 | 8 | RMSNormOp | ve | 9,201.7 | 9,113.5/9,593.6 | 9,426.0 | 97.5 % | 224 |
| react-answer#r2 | 10 | LinearOp | me | 19,821.9 | 19,491.5/19,857.0 | 19,984.3 | 99.1 % | 32 |
| react-answer#r2 | 11 | LinearOp | me | 19,788.7 | 19,545.3/20,284.8 | 19,891.7 | 99.5 % | 32 |
| react-answer#r2 | 12 | LinearOp | me | 20,007.8 | 19,588.5/20,913.0 | 20,100.8 | 99.5 % | 32 |
| react-answer#r2 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 148.4 | 0.0 % | 0 |
| react-answer#r2 | 14 | TransposeOp | de | 5,761.0 | 5,332.7/5,825.2 | 5,874.1 | 97.9 % | 32 |
| react-answer#r2 |  | call_overhead |  | 2,537.3 | 2,509.3/2,684.8 |  |  % | 2 |
| react-plan#r0 | 6 | RMSNormOp | ve | 4,052.1 | 4,045.8/4,107.8 | 4,311.8 | 94.2 % | 224 |
| react-plan#r0 | 7 | AddOp | ve | 326.2 | 324.4/335.2 | 555.7 | 59.8 % | 32 |
| react-plan#r0 | 8 | RMSNormOp | ve | 4,038.8 | 4,019.8/4,115.6 | 4,250.5 | 95.1 % | 224 |
| react-plan#r0 | 10 | LinearOp | me | 11,489.6 | 11,152.6/11,535.7 | 11,628.1 | 98.8 % | 32 |
| react-plan#r0 | 11 | LinearOp | me | 11,339.5 | 11,116.7/11,519.7 | 11,436.8 | 99.2 % | 32 |
| react-plan#r0 | 12 | LinearOp | me | 11,230.8 | 11,155.3/11,588.7 | 11,320.2 | 99.2 % | 32 |
| react-plan#r0 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 141.2 | 0.0 % | 0 |
| react-plan#r0 | 14 | TransposeOp | de | 4,206.5 | 4,002.6/4,465.6 | 4,326.4 | 97.4 % | 32 |
| react-plan#r0 |  | call_overhead |  | 804.9 | 797.5/845.2 |  |  % | 2 |
| react-plan#r1 | 6 | RMSNormOp | ve | 4,052.0 | 4,040.3/4,164.0 | 4,310.7 | 91.9 % | 224 |
| react-plan#r1 | 7 | AddOp | ve | 325.0 | 321.8/326.5 | 574.2 | 54.1 % | 32 |
| react-plan#r1 | 8 | RMSNormOp | ve | 4,047.4 | 4,009.3/4,115.9 | 4,282.1 | 92.5 % | 224 |
| react-plan#r1 | 10 | LinearOp | me | 11,375.8 | 11,137.9/11,508.3 | 11,530.0 | 98.7 % | 32 |
| react-plan#r1 | 11 | LinearOp | me | 11,185.6 | 11,140.7/11,516.7 | 11,305.6 | 99.1 % | 32 |
| react-plan#r1 | 12 | LinearOp | me | 11,267.0 | 11,170.3/11,541.1 | 11,355.1 | 99.2 % | 32 |
| react-plan#r1 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 150.6 | 0.0 % | 0 |
| react-plan#r1 | 14 | TransposeOp | de | 4,055.4 | 4,004.1/4,334.9 | 4,181.2 | 97.1 % | 32 |
| react-plan#r1 |  | call_overhead |  | 2,251.5 | 2,228.5/2,281.5 |  |  % | 2 |
| react-plan#r2 | 6 | RMSNormOp | ve | 4,096.8 | 4,039.1/4,146.0 | 4,344.7 | 94.2 % | 224 |
| react-plan#r2 | 7 | AddOp | ve | 326.2 | 324.4/340.6 | 555.0 | 59.6 % | 32 |
| react-plan#r2 | 8 | RMSNormOp | ve | 4,033.5 | 4,011.6/4,077.5 | 4,246.9 | 95.0 % | 224 |
| react-plan#r2 | 10 | LinearOp | me | 11,194.4 | 11,135.0/11,500.6 | 11,331.1 | 98.7 % | 32 |
| react-plan#r2 | 11 | LinearOp | me | 11,340.1 | 11,129.6/11,521.0 | 11,425.6 | 99.2 % | 32 |
| react-plan#r2 | 12 | LinearOp | me | 11,220.3 | 11,145.5/11,657.7 | 11,315.4 | 99.2 % | 32 |
| react-plan#r2 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 141.7 | 0.0 % | 0 |
| react-plan#r2 | 14 | TransposeOp | de | 4,008.8 | 4,002.5/4,483.4 | 4,128.5 | 97.3 % | 32 |
| react-plan#r2 |  | call_overhead |  | 2,307.0 | 2,216.5/2,354.5 |  |  % | 2 |

## Per-iteration conservation

| phase | iter | wall (us) | GPU busy % | operator GPU (us) | overhead GPU (us) | launches |
|---|---:|---:|---:|---:|---:|---:|
| warmup | 0 | 7,166,107.8 | 46.64 | 3,259,285.9 | 82,914.0 | 18300 |
| warmup | 1 | 6,568,370.2 | 50.7 | 3,248,983.6 | 81,233.4 | 18300 |
| warmup | 2 | 6,570,333.4 | 50.6 | 3,243,810.8 | 80,808.7 | 18300 |
| measured | 0 | 6,504,168.5 | 51.16 | 3,245,510.0 | 82,077.4 | 18300 |
| measured | 1 | 6,610,736.5 | 50.3 | 3,243,952.3 | 81,504.9 | 18300 |
| measured | 2 | 6,595,384.2 | 50.43 | 3,243,853.5 | 82,085.9 | 18300 |
| measured | 3 | 6,605,965.9 | 50.31 | 3,242,228.5 | 81,266.2 | 18300 |
| measured | 4 | 6,889,112.9 | 48.21 | 3,237,875.4 | 83,319.3 | 18300 |
| measured | 5 | 6,694,798.1 | 49.69 | 3,244,505.6 | 82,087.8 | 18300 |
| measured | 6 | 6,606,114.8 | 50.34 | 3,243,343.2 | 82,057.3 | 18300 |
| measured | 7 | 6,522,214.5 | 50.77 | 3,230,383.9 | 81,019.5 | 18300 |

## Reading notes

- `GPU busy %` is the union of all GPU intervals launched inside the iteration divided by the iteration wall.
  The remainder is host-side: Python dispatch, per-operator `cudaEventSynchronize`, CPU tool matmuls, pinned staging.
- `GPU/CPU` per operator compares launch-owned GPU time to the NVTX CPU range, which encloses a synchronize.
- Warmup rows are shown for context only; no measured statistic includes them.
- Plan `/workspace/AgentSys/artifacts/gpu_autotrace/scaled_plans/react_moa_mcts_x3_L/hybrid-plan.json` sha256 `1b0c2b73b03b9590…`; sqlite sha256 `d52546eef3fa1774…`.
