from __future__ import annotations

import json
from pathlib import Path

import pytest

from agentsys.model import Priority
from agentsys.workload import PROJECT_ROOT, load_agent_workload


def test_three_parameterized_workloads_load_and_differ() -> None:
    expected = {
        "react_moa_mcts": (3, 11, 10, 1),
        "react_tool": (1, 3, 2, 1),
        "planner_debate": (2, 6, 5, 1),
    }
    hashes = set()
    for name, counts in expected.items():
        workload = load_agent_workload(PROJECT_ROOT / f"workloads/{name}.json")
        contract = workload.to_contract_dict()
        observed = contract["summary"]
        assert (
            observed["programs"],
            observed["calls"],
            observed["llm_calls"],
            observed["tool_calls"],
        ) == counts
        assert len(workload.call_specs()) == counts[1]
        assert len(workload.sha256) == 64
        hashes.add(workload.sha256)
        workload.hardware.require_installed_profile()
    assert len(hashes) == 3


def test_workload_exposes_agentix_agentxpu_and_priority_parameters() -> None:
    workload = load_agent_workload(PROJECT_ROOT / "workloads/planner_debate.json")
    assert workload.agentix_policy.value == "plas"
    assert workload.agentix_batch_size == 2
    assert workload.agentxpu_config.heg_prefill_chunk_tokens == 32
    assert workload.agentxpu_config.max_decode_batch == 8
    assert workload.program_priorities == {
        "planner": Priority.REACTIVE,
        "debate": Priority.PROACTIVE,
    }


def _write_workload(tmp_path: Path, value: dict) -> Path:
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def test_workload_rejects_cycles_and_missing_dependencies(tmp_path: Path) -> None:
    base = json.loads((PROJECT_ROOT / "workloads/react_tool.json").read_text(encoding="utf-8"))
    base["calls"][0]["deps"] = ["answer"]
    with pytest.raises(ValueError, match="cycle"):
        load_agent_workload(_write_workload(tmp_path, base))

    base = json.loads((PROJECT_ROOT / "workloads/react_tool.json").read_text(encoding="utf-8"))
    base["calls"][0]["deps"] = ["missing"]
    with pytest.raises(ValueError, match="missing deps"):
        load_agent_workload(_write_workload(tmp_path, base))


def test_workload_rejects_oversized_tile_window_and_incompatible_hardware(
    tmp_path: Path,
) -> None:
    base = json.loads((PROJECT_ROOT / "workloads/react_tool.json").read_text(encoding="utf-8"))
    base["models"][0]["selected_source_indices"] = list(range(9))
    base["models"][0]["stages"] = [0] * 9
    with pytest.raises(ValueError, match="1..8"):
        load_agent_workload(_write_workload(tmp_path, base))

    base = json.loads((PROJECT_ROOT / "workloads/react_tool.json").read_text(encoding="utf-8"))
    base["hardware"]["hptpe_rows"] = 8
    workload = load_agent_workload(_write_workload(tmp_path, base))
    with pytest.raises(ValueError, match="not installed"):
        workload.hardware.require_installed_profile()
