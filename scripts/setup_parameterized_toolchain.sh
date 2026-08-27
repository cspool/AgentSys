#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
verify_only=0

if [[ ${1:-} == "--verify-only" ]]; then
  verify_only=1
elif [[ $# -ne 0 ]]; then
  echo "usage: $0 [--verify-only]" >&2
  exit 2
fi

cd "${project_root}"

if [[ ${verify_only} -eq 1 ]]; then
  bash scripts/setup_revised_toolchain.sh --verify-only
else
  bash scripts/setup_revised_toolchain.sh
fi

"${project_root}/.venv/bin/python" - <<'PY'
import json
from pathlib import Path
from agentsys.workload import load_agent_workload

root = Path.cwd()
system = json.loads((root / "config/parameterized-system.json").read_text())
matrix = json.loads((root / system["layer_matrix"]).read_text())
assert matrix["active_layers"] == ["agentix", "agentxpu", "tisa", "mllm", "hptpe"]
assert sum(matrix["layers"][name]["expected_endpoints"] for name in matrix["active_layers"]) == 68
for workload in system["workloads"]:
    loaded = load_agent_workload(root / workload)
    loaded.hardware.require_installed_profile()
print("Parameterized workload/matrix source contract: PASS")
PY

echo "Setup complete. Replay with:"
echo "  .venv/bin/agentsys-reproduce-parameterized"
