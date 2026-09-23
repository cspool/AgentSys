#!/usr/bin/env bash
# 用 nsys GPU 指标采样测 MPK megakernel 的资源轴。
# 为什么不用 NCU: NCU 串行化 kernel, 而 MPK 要求 worker_kernel 与 scheduler_kernel 同时在跑并互相通信,
#                 串行化后 worker 永远等不到 scheduler -> 死等(实测 50 分钟零产出)。
set -u
NS=/opt/nvidia/nsight-systems/2026.3.1/bin/nsys
export CUDA_VISIBLE_DEVICES=${GPU:-1}
export MIRAGE_HOME=/workspace/AgentSys/third_party/mirage-mpk
export HF_HOME=/data3/docker_model/AgentSys/hf
export XDG_CACHE_HOME=/data3/docker_cache/AgentSys/xdg-cache-h23
export PATH=/data3/docker_cache/AgentSys/envs/mpk/bin:$PATH
V=/data3/docker_cache/AgentSys/envs/mpk
M=${MODEL:-/data3/docker_model/AgentSys/Qwen3-1.7B}
OUT=${OUT:-/tmp/nsys_mpk}
cd $MIRAGE_HOME/demo/qwen3
for L in ${LENS:-256 4096}; do
  echo "### 上下文 $L ###"
  timeout 1800 $NS profile --gpu-metrics-devices=cuda-visible --gpu-metrics-set=ad10x \
    --gpu-metrics-frequency=20000 --sample=none --cpuctxsw=none --trace=cuda \
    -o ${OUT}_$L --force-overwrite true \
    $V/bin/python demo.py --model $M --use-mirage --max-seq-length $L --ignore-eos > /tmp/nsys_run_$L.log 2>&1
  echo "nsys rc=$? -> ${OUT}_$L.nsys-rep"
  grep -hE "per-token latency" /tmp/nsys_run_$L.log | tail -1
done
echo "NSYS_MPK_DONE"
