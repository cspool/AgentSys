#!/bin/bash
cd /workspace/AgentSys/experiments/h23-agentix-8b/valve_repro
/workspace/AgentSys/.venv-vllm/bin/python valve_run.py --arm channel --device 0 --cool 0.074
