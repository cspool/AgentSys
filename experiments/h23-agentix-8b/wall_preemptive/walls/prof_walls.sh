#!/usr/bin/env bash
cd "$(dirname "$0")"
M="sm__throughput.avg.pct_of_peak_sustained_elapsed,dram__throughput.avg.pct_of_peak_sustained_elapsed,lts__throughput.avg.pct_of_peak_sustained_elapsed,l1tex__throughput.avg.pct_of_peak_sustained_elapsed,sm__pipe_tensor_cycles_active_v2.avg.pct_of_peak_sustained_elapsed,sm__inst_executed_pipe_fma.avg.pct_of_peak_sustained_elapsed,l1tex__data_pipe_lsu_wavefronts_mem_shared.avg.pct_of_peak_sustained_elapsed"
printf "%-13s %6s %6s %6s %6s %6s %6s %6s\n" 配置 SM TC FMA smem L1 L2 DRAM
printf -- "---------------------------------------------------------------------\n"
for C in "$@"; do
  case $C in gemm*|tc_*|l2f*) K="regex:gemm|Kernel2" ;; *) K="regex:flash_fwd_(kernel|splitkv_kernel)" ;; esac
  CUDA_VISIBLE_DEVICES=1 timeout 600 ncu --csv --cache-control none --kernel-name "$K" --launch-skip 1 --launch-count 1 \
      --metrics "$M" python3 real_walls.py --only $C --prof > /tmp/w_$C.csv 2>&1
  python3 - "$C" /tmp/w_$C.csv <<'PY'
import csv,sys
name,path=sys.argv[1],sys.argv[2]
lines=open(path).read().splitlines()
hdr=next((i for i,l in enumerate(lines) if l.startswith('"ID"')), None)
rows=[r for r in csv.DictReader(lines[hdr:])] if hdr is not None else []
if not rows: print(f"{name:<15}  无匹配"); raise SystemExit
g=lambda k: next((r['Metric Value'] for r in rows if r['Metric Name'].startswith(k)),'-')
print(f"{name:<13} {g('sm__throughput'):>6} {g('sm__pipe_tensor'):>6} {g('sm__inst_executed_pipe_fma'):>6} "
      f"{g('l1tex__data_pipe_lsu'):>6} {g('l1tex__throughput'):>6} {g('lts__throughput'):>6} {g('dram__throughput'):>6}")
PY
done
