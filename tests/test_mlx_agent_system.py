from __future__ import annotations

import json

from agentsys.workload import PROJECT_ROOT


ROOT = PROJECT_ROOT / "artifacts/mlx_agent/run_046"
EXPECTED = {
    "react_moa_mcts": {"calls": 11, "llm": 10, "micro": 450, "dma": 2288, "cycle": 3628, "rtl": 3068, "trace": 762},
    "react_tool": {"calls": 3, "llm": 2, "micro": 90, "dma": 560, "cycle": 828, "rtl": 716, "trace": 158},
    "planner_debate": {"calls": 6, "llm": 5, "micro": 225, "dma": 1208, "cycle": 1878, "rtl": 1598, "trace": 385},
}


def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_run046_global_three_workload_replay_passes() -> None:
    result = _json(ROOT / "reproduction.json")
    assert result["summary"] == {
        "calls": 20,
        "failing": 0,
        "gates": 9,
        "llm_calls": 17,
        "mlx_micro_ops": 765,
        "pass": True,
        "passing": 9,
        "serial_order": True,
        "tool_calls": 3,
        "workloads": 3,
    }
    assert all(result["gates"].values())
    assert set(result["workloads"]) == set(EXPECTED)


def test_run046_each_agent_dag_executes_exact_cpu_mlx_contract() -> None:
    header_hashes = set()
    elf_hashes = set()
    for name, expected in EXPECTED.items():
        base = ROOT / "workloads" / name
        system = _json(base / "mlx-agent-system.json")
        compiled = _json(base / "compiled-mlx.json")
        assert system["summary"]["passing"] == system["summary"]["gates"] == 10
        assert system["summary"]["calls"] == expected["calls"]
        assert system["summary"]["llm_calls"] == expected["llm"]
        assert system["summary"]["tool_calls"] == 1
        assert system["summary"]["mlx_micro_ops"] == expected["micro"]
        assert system["summary"]["trace_events"] == expected["trace"]
        assert all(system["gates"].values())
        assert compiled["summary"]["pass"] and all(compiled["gates"].values())
        for backend in ("cycle", "rtl"):
            assert all(system["backend_gates"][backend].values())
            final = system["backend_results"][backend]["parsed"]["summary"]
            assert final["dma"] == expected["dma"]
            assert final["system"] == expected[backend]
            assert final["mismatches"] == final["dependencies"] == 0
            llm_calls = [
                call
                for call in system["backend_results"][backend]["parsed"]["calls"]
                if call["kind"] == "llm"
            ]
            assert [call["dma"] for call in llm_calls] == [
                344,
                *([216] * (expected["llm"] - 1)),
            ]
            assert all(call["dma_bytes"] == 576 for call in llm_calls)
        elf_hashes.add(system["backend_results"]["cycle"]["elf_sha256"])
        header_hashes.add(
            __import__("hashlib").sha256(
                (base / "generated/agent-mlx.h").read_bytes()
            ).hexdigest()
        )
        assert len(system["trace"]["layers"]) == 14
        assert {"mlx_tag", "mlx_pe", "mlx_spm", "mlx_network"}.issubset(
            system["trace"]["layers"]
        )
    assert len(header_hashes) == len(elf_hashes) == 3
