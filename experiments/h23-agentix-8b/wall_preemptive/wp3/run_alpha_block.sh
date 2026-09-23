#!/usr/bin/env bash
# 一个 block = 该 cell 全部臂按随机排列各跑一遍 (RCBD)。
# 必须等受害者自然打印 per-token 时延 —— 否则拿不到 G_v, STP 无从计算。
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
AX=${AX:-tc}; REP=${1:-1}
ARMS=$(python3 -c "
import random; random.seed($REP*7+11)
a=['late','spread','early']; random.shuffle(a); print(' '.join(a))")
echo "block $REP 臂序: $ARMS"
for ARM in $ARMS; do
  rm -f $R/out/alpha_${AX}_${ARM}_r${REP}.json
  $R/run_alpha.sh $ARM $AX $REP
  VLOG=/tmp/mpk_alpha_${AX}_${ARM}_r${REP}.log
  for i in $(seq 1 90); do
    if [ -f $R/out/alpha_${AX}_${ARM}_r${REP}.json ] && grep -q "per-token latency" $VLOG 2>/dev/null; then break; fi
    sleep 5
  done
  V=$(grep -oE 'per-token latency: [0-9.]+' $VLOG 2>/dev/null|tail -1)
  echo "  $ARM: 抢占者=$([ -f $R/out/alpha_${AX}_${ARM}_r${REP}.json ] && echo ok || echo 缺)  受害者=${V:-缺}"
  pkill -KILL -f "[d]emo.py" 2>/dev/null || true
  pkill -KILL -f "[c]o_alpha.py" 2>/dev/null || true
  sleep 20
done
echo "BLOCK_${REP}_DONE"
