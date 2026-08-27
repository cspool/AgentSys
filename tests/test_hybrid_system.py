from __future__ import annotations

import json
from collections import Counter

from agentsys.hybrid_plan import DEFAULT_CONFIG
from agentsys.workload import PROJECT_ROOT


ROOT = PROJECT_ROOT / "artifacts/hybrid_reproduction/run_040"
EXPECTED = {
    "react_moa_mcts": {"calls": 11, "llm": 10, "ops": 80, "native": 133, "rocket": 860, "hybrid": 993, "ranks": [5, 5]},
    "react_tool": {"calls": 3, "llm": 2, "ops": 16, "native": 29, "rocket": 180, "hybrid": 209, "ranks": [1, 1]},
    "planner_debate": {"calls": 6, "llm": 5, "ops": 40, "native": 68, "rocket": 436, "hybrid": 504, "ranks": [3, 2]},
}


def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_run040_global_reproduction_closes_hybrid_protocol() -> None:
    result = _json(ROOT / "reproduction.json")
    assert result["summary"] == {
        "executed": 4,
        "failing": 0,
        "gates": 11,
        "max_relative_error": 0.09909909909909899,
        "paper_endpoints": 68,
        "paper_endpoints_passing": 68,
        "paper_layers": 5,
        "parameter_switches": 6,
        "pass": True,
        "passing": 11,
        "serial_order": True,
        "stages": 4,
        "workloads": 3,
    }
    assert all(result["gates"].values())
    assert result["layer_regression"]["summary"]["endpoints"] == 68
    assert result["layer_regression"]["summary"]["passing"] == 68
    assert result["layer_regression"]["summary"]["parameter_switches"] == 5
    assert set(result["workloads"]) == set(EXPECTED)


def test_run040_every_workload_uses_both_gpus_numa_and_full_mir() -> None:
    for name, expected in EXPECTED.items():
        base = ROOT / "workloads" / name
        plan = _json(base / "hybrid-plan.json")
        runtime = _json(base / "native/native-runtime.json")
        system = _json(base / "hybrid-system.json")
        assert plan["summary"]["calls"] == expected["calls"]
        assert plan["summary"]["llm_calls"] == expected["llm"]
        assert plan["summary"]["tool_calls"] == 1
        assert plan["summary"]["mir_operators"] == expected["ops"]
        assert plan["summary"]["gpu_rank_llm_calls"] == expected["ranks"]
        assert runtime["summary"]["events"] == expected["native"]
        assert runtime["summary"]["mir_operators"] == expected["ops"]
        assert runtime["summary"]["gpus"] == runtime["summary"]["numa_nodes"] == 2
        assert runtime["summary"]["passing"] == runtime["summary"]["gates"] == 13
        assert all(runtime["gates"].values())
        assert [rank["device"] for rank in runtime["ranks"]] == [0, 1]
        assert [rank["numa_node"] for rank in runtime["ranks"]] == [0, 1]
        assert all(len(rank["observed_affinity"]) == 32 for rank in runtime["ranks"])
        assert all(rank["torch_cpu_threads"] == 16 for rank in runtime["ranks"])
        assert all(rank["collective"]["correct"] for rank in runtime["ranks"])
        assert all(not any(rank["p2p"].values()) for rank in runtime["ranks"])
        assert system["summary"]["rocket_events"] == expected["rocket"]
        assert system["summary"]["hybrid_events"] == expected["hybrid"]
        assert system["summary"]["native_events"] == expected["native"]
        assert system["summary"]["passing"] == system["summary"]["gates"] == 9
        assert all(system["gates"].values())


def test_run040_operator_identity_and_transport_logs_are_complete() -> None:
    for name, expected in EXPECTED.items():
        base = ROOT / "workloads" / name
        events = [
            json.loads(line)
            for line in (base / "native/native-trace.jsonl").read_text(
                encoding="utf-8"
            ).splitlines()
        ]
        counts = Counter(event["event"] for event in events)
        assert counts["mir_operator"] == expected["ops"]
        assert counts["h2d"] == counts["d2h"] == expected["llm"]
        assert counts["mllm_token_preprocess"] == expected["llm"]
        assert counts["agent_tool_execute"] == 1
        assert counts["all_reduce_counts"] == 2
        by_call = Counter(
            (event["call_id"], event["engine"])
            for event in events
            if event["event"] == "mir_operator"
        )
        for call in _json(base / "hybrid-plan.json")["calls"]:
            if call["kind"] == "llm":
                assert by_call[(call["call_id"], "me")] == 3
                assert by_call[(call["call_id"], "ve")] == 3
                assert by_call[(call["call_id"], "de")] == 2
        for rank in (0, 1):
            nccl = (base / f"native/rank{rank}-nccl.log").read_text(encoding="utf-8")
            assert "via SHM/direct/direct" in nccl
        merged = _json(base / "hybrid-system.json")["trace"]
        assert merged["alignment"] == "call_identity_only_no_cross_domain_time_conversion"
        assert merged["clock_domains"] == [
            "host_monotonic_ns",
            "rocket_dynamic_cycle",
            "rocket_static_cycle",
        ]
        assert {"gpu", "cuda", "nccl", "tisa", "hptpe"}.issubset(
            merged["layers"]
        )


def test_hybrid_entrypoints_and_config_are_public() -> None:
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    for entrypoint in (
        "agentsys-run-hybrid",
        "agentsys-hybrid-runtime",
        "agentsys-reproduce-hybrid",
    ):
        assert entrypoint in pyproject
    config = _json(DEFAULT_CONFIG)
    assert config["manifest"].endswith("run_040/reproduction.json")
    assert config["mllm_cuda_audit"].endswith("mllm-cuda-run_039.json")
    assert (PROJECT_ROOT / "docs/hybrid-system.md").is_file()
