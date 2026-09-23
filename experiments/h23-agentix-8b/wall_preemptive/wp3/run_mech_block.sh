#!/usr/bin/env bash
# 一个 block: 指定并发机制, 三个抢占时机臂按随机序各跑一遍
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
MECH=${MECH:-pod2}; AX=${AX:-tc}; REP=${1:-1}
export CUDA_VISIBLE_DEVICES=${GPU:-1} CUDA_MPS_PIPE_DIRECTORY=/tmp/mps1/pipe
export LD_LIBRARY_PATH=/workspace/AgentSys/third_party/BulletServe/csrc/build:${LD_LIBRARY_PATH:-}
VP=/data3/docker_cache/AgentSys/envs/pod_attn/bin/python
CP=/data3/docker_cache/AgentSys/envs/bullet/bin/python
if [ -n "${ARMS_OVERRIDE:-}" ]; then
  ARMS=$(python3 -c "
import random; random.seed($REP*31+7)
a='${ARMS_OVERRIDE}'.split(); random.shuffle(a); print(' '.join(a))")
else
  ARMS=$(python3 -c "
import random; random.seed($REP*31+7)
a=['a100','a050','a000']; random.shuffle(a); print(' '.join(a))")
fi
echo "block $REP mech=$MECH ax=$AX 臂序: $ARMS"
for ARM in $ARMS; do
  SFX=""; [ "${SUSP:-0}" = "1" ] && SFX="_susp"; [ "${MODE:-quota}" = "cilp" ] && SFX="_cilp"
  GATE=/tmp/wp3_gate_gpu${GPU:-1}
  VOUT=$R/out/m_${MECH}_w${WAVE:-01}${SFX}_${AX}_${ARM}_r${REP}_vic.json
  COUT=$R/out/m_${MECH}_w${WAVE:-01}${SFX}_${AX}_${ARM}_r${REP}_co.json
  rm -f $VOUT $COUT
  MPSENV="CUDA_MPS_PIPE_DIRECTORY=/tmp/mps1/pipe"; [ "${MODE:-quota}" = "cilp" ] && MPSENV="CUDA_MPS_PIPE_DIRECTORY="
  setsid nohup env CUDA_VISIBLE_DEVICES=${GPU:-1} $MPSENV \
    $VP $R/victim/pod_wave.py --mech $MECH --secs ${VSECS:-95} --wave ${WAVE:-01} --beacon /tmp/wp3_phase_gpu${GPU:-1} $([ "${SUSP:-0}" = "1" ] && echo --suspend-gate $GATE) --out $VOUT > /tmp/m_${MECH}_${AX}_${ARM}_r${REP}_v.log 2>&1 < /dev/null & disown
  sleep 8
  setsid nohup env CUDA_VISIBLE_DEVICES=${GPU:-1} $MPSENV \
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH $CP $R/preemptor/co_phase.py --mode ${MODE:-quota} --arm $ARM --axis $AX --orth-phase ${ORTH:-0} --anti-phase ${ANTI:-1} \
    --secs ${CSECS:-70} --warmup ${WARM:-5} --offsets-ms ${OFFS:-100,230,360,490} --burst-ms ${BMS:-90} --beacon /tmp/wp3_phase_gpu${GPU:-1} $([ "${SUSP:-0}" = "1" ] && echo --suspend-victim $GATE --burst-tpcs 64) --out $COUT > /tmp/m_${MECH}_${AX}_${ARM}_r${REP}_c.log 2>&1 < /dev/null & disown
  for i in $(seq 1 40); do [ -f $VOUT ] && [ -f $COUT ] && break; sleep 5; done
  echo "  $ARM: 受害者=$([ -f $VOUT ] && echo ok || echo 缺) 抢占者=$([ -f $COUT ] && echo ok || echo 缺)"
  # 只杀本 GPU 的进程: 读 /proc/PID/environ 里的 CUDA_VISIBLE_DEVICES 判断, 与命令行写法无关。
  # 按进程名杀会误杀另一块卡上正在跑的实验, 残留的受害者又会污染下一个臂(曾把 solo 锚从 815 拉到 592)。
  for p in $(pgrep -x python3.12); do
    c=$(tr '\0' '\n' < /proc/$p/cmdline 2>/dev/null | tr '\n' ' ')
    case "$c" in *pod_wave.py*|*co_phase.py*) ;; *) continue;; esac
    e=$(tr '\0' '\n' < /proc/$p/environ 2>/dev/null | grep '^CUDA_VISIBLE_DEVICES=' | cut -d= -f2)
    [ "$e" = "${GPU:-1}" ] && kill -KILL $p 2>/dev/null
  done
  sleep 10
done
echo "MECH_BLOCK_${MECH}_w${WAVE:-01}_${AX}_${REP}_DONE"
