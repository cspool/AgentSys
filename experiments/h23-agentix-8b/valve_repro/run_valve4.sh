#!/bin/bash
cd /workspace/AgentSys/experiments/h23-agentix-8b/valve_repro
PY=/workspace/AgentSys/.venv-vllm/bin/python
for arm in on_solo off_solo naive channel iter; do
  echo "=== $arm ==="
  $PY valve_run.py --arm $arm --device 0 --cool 0.074
done
echo "=== Valve v4 完成 ==="
