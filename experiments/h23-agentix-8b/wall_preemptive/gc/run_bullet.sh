#!/usr/bin/env bash
# Bullet(greencontext 论文) 复现: prefill/decode 两实例经 MPS 空间共享 + libsmctrl TPC 分区
# 容量适配: 论文用 A100/A800/H100(80GB) 跑 8B~70B; 4090 只有 24GB 且 Bullet 是双进程,
#           两份 8B 权重放不下 -> 换 Qwen3-1.7B。机制(MPS + TPC resize)不变。
set -eu
B=/workspace/AgentSys/third_party/BulletServe
V=/data3/docker_cache/AgentSys/envs/bullet
MODEL=${MODEL:-/data3/docker_model/AgentSys/Qwen3-1.7B}
PORT=${PORT:-30000}
export CUDA_VISIBLE_DEVICES=${GPU:-0}
MPSDIR=${MPSDIR:-$B/log/mps/nvidia-mps}
export CUDA_MPS_PIPE_DIRECTORY=$MPSDIR
export CUDA_MPS_LOG_DIRECTORY=$B/log/mps/nvidia-log
export LD_LIBRARY_PATH=$B/csrc/build:${LD_LIBRARY_PATH:-}

case "${1:-serve}" in
  mps)   bash $B/scripts/start_mps.sh; sleep 2; echo "MPS 已起"; ps -ef|grep "[n]vidia-cuda-mps"|head -3 ;;
  stop)  bash $B/scripts/kill_mps.sh; bash $B/scripts/killall_sglang.sh 2>/dev/null || true ;;
  serve) cd $B && $V/bin/python -m sglang.launch_server --model-path "$MODEL" \
           --disable-radix-cache --mem-fraction-static ${MEMFRAC:-0.70} --max-total-tokens ${MAXTOK:-60000} --mps-pipe-dir $MPSDIR ${BULLET_FLAGS:---enable-bullet-engine} --port $PORT --host 127.0.0.1 ;;
  bench) cd $B && $V/bin/python ./python/sglang/bench_serving.py --backend sglang \
           --dataset-name sharegpt --num-prompts ${N:-200} --host 127.0.0.1 --port $PORT \
           --model "$MODEL" --dataset-path /data3/docker_model/AgentSys/_datasets/ShareGPT_V3_unfiltered_cleaned_split.json \
           --request-rate ${RATE:-10} ;;
  # wall: 用请求组成来构造墙型 —— prefill 重 => 算力/TC 墙; decode 重 => DRAM 墙; 均衡 => 双轴高
  wall)  cd $B && $V/bin/python ./python/sglang/bench_serving.py --backend sglang \
           --dataset-name random --num-prompts ${N:-200} --host 127.0.0.1 --port $PORT \
           --model "$MODEL" --random-input-len ${IN:-1024} --random-output-len ${OUT:-128} \
           --random-range-ratio ${RR:-1.0} --request-rate ${RATE:-inf} --max-concurrency ${CONC:-16} ;;
  *) echo "用法: $0 {mps|serve|bench|stop}"; exit 1 ;;
esac
