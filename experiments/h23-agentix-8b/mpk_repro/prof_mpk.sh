#!/usr/bin/env bash
# 测 MPK megakernel 的原生资源画像 (它是 persistent kernel, 一次 launch 跑完整个模型)
set -u
export CUDA_VISIBLE_DEVICES=1
export MIRAGE_HOME=/workspace/AgentSys/third_party/mirage-mpk
export HF_HOME=/data3/docker_model/AgentSys/hf
export XDG_CACHE_HOME=/data3/docker_cache/AgentSys/xdg-cache-h23
V=/data3/docker_cache/AgentSys/envs/mpk
M=${MODEL:-/data3/docker_model/AgentSys/Qwen3-1.7B}
cd $MIRAGE_HOME/demo/qwen3
Mx="sm__pipe_tensor_op_hmma_cycles_active.avg.pct_of_peak_sustained_active,\
sm__pipe_fma_cycles_active.avg.pct_of_peak_sustained_active,\
dram__throughput.avg.pct_of_peak_sustained_elapsed,\
lts__t_sectors.avg.pct_of_peak_sustained_elapsed,\
l1tex__t_sectors.avg.pct_of_peak_sustained_elapsed,\
launch__shared_mem_per_block_dynamic,launch__block_size,launch__grid_size,\
sm__warps_active.avg.pct_of_peak_sustained_active"
echo "### MPK megakernel ###"
timeout 5400 ncu --csv --cache-control none --kernel-name regex:"(worker_kernel|scheduler_kernel|persistent_kernel)" --launch-count 2 --metrics "$Mx" \
  $V/bin/python demo.py --model $M --use-mirage --max-new-tokens ${NTOK:-8} > /tmp/mpk_ncu.csv 2>&1
echo "ncu rc=$?"
tail -n 3 /tmp/mpk_ncu.csv
