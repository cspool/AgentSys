#!/usr/bin/env bash
# 用 MPK 自身负载构造墙型谱 —— 上下文长度是旋钮:
#   上下文短 => decode 每步读的 KV 少 => 偏算力
#   上下文长 => 每步读整段 KV => 偏 DRAM
# (已实测: 329 token 时 4.274 ms/token, 2009 token 时 5.121 ms/token)
set -u
export CUDA_VISIBLE_DEVICES=${GPU:-1}
export MIRAGE_HOME=/workspace/AgentSys/third_party/mirage-mpk
export HF_HOME=/data3/docker_model/AgentSys/hf
export XDG_CACHE_HOME=/data3/docker_cache/AgentSys/xdg-cache-h23
export PATH=/data3/docker_cache/AgentSys/envs/mpk/bin:$PATH
V=/data3/docker_cache/AgentSys/envs/mpk
M=${MODEL:-/data3/docker_model/AgentSys/Qwen3-1.7B}
cd $MIRAGE_HOME/demo/qwen3
printf "%-10s %10s %10s %12s\n" "上下文" "生成长度" "ms/token" "整段秒数"
for L in 256 512 1024 2048 4096; do
  s=$SECONDS
  out=$(timeout 1800 $V/bin/python demo.py --model $M --use-mirage --max-seq-length $L --ignore-eos 2>&1 | grep -E "per-token latency")
  lat=$(echo "$out" | grep -oE "[0-9.]+ ms" | head -1 | awk '{print $1}')
  gl=$(echo "$out" | grep -oE "generate length [0-9]+" | awk '{print $3}')
  printf "%-10s %10s %10s %12s\n" "$L" "${gl:-失败}" "${lat:-失败}" "$((SECONDS-s))"
done
echo "MPK_WALLS_DONE"
