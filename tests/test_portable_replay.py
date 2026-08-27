from __future__ import annotations

import json
from pathlib import Path

from agentsys.portable_certificate import (
    agent_signature,
    endpoint_signature,
    substrate_signature,
)
from agentsys.workload import PROJECT_ROOT


def test_project_local_replay_contract_is_strict_and_serial() -> None:
    config = json.loads(
        (PROJECT_ROOT / "config/project-local-chipyard.json").read_text(
            encoding="utf-8"
        )
    )
    assert config["expected_stage_order"] == [
        "project_local_chipyard_preflight",
        "project_local_mlx_substrate",
        "project_local_three_agent_dags",
        "project_local_six_layer_regression",
    ]
    assert set(config["baselines"]) == {"chipyard", "agents", "layers"}


def test_endpoint_signature_supports_scalar_and_range_targets() -> None:
    result = {
        "audit": [
            {
                "endpoint": "scalar",
                "layer": "tisa",
                "observed": 1.2,
                "target": 1.25,
                "relative_error": 0.04,
                "limit": 0.1,
                "pass": True,
            },
            {
                "endpoint": "range",
                "layer": "tisa",
                "observed": 1.3,
                "target_range": [1.2, 1.4],
                "relative_error": 0.0,
                "limit": 0.1,
                "pass": True,
            },
        ]
    }
    signature = endpoint_signature(result)
    assert signature[0][3] == "1.25"
    assert signature[1][3] == "[1.2,1.4]"


def test_substrate_signature_ignores_artifact_locations() -> None:
    record = {
        "backend": "cycle",
        "workload": "bsmm",
        "summary": {"kernel": 48},
        "checks": {"golden": True},
        "pass": True,
    }
    first = {"records": [{**record, "log": "/first"}]}
    second = {"records": [{**record, "log": "/second"}]}
    assert substrate_signature(first) == substrate_signature(second)


def test_agent_signature_ignores_only_trace_location(tmp_path: Path) -> None:
    def write(name: str, trace_path: str) -> Path:
        path = tmp_path / f"{name}.json"
        path.write_text(
            json.dumps(
                {
                    "summary": {"pass": True},
                    "gates": {"work": True},
                    "backend_gates": {"cycle": {"golden": True}},
                    "backend_results": {
                        "cycle": {"parsed": {"summary": {"kernel": 10}}},
                        "rtl": {"parsed": {"summary": {"kernel": 8}}},
                    },
                    "trace": {
                        "path": trace_path,
                        "sha256": "same",
                        "events": 3,
                        "layers": ["cpu", "mlx"],
                    },
                }
            ),
            encoding="utf-8",
        )
        return path

    first = {
        "summary": {"pass": True},
        "workloads": {"w": {"path": str(write("first", "/first"))}},
    }
    second = {
        "summary": {"pass": True},
        "workloads": {"w": {"path": str(write("second", "/second"))}},
    }
    assert agent_signature(first) == agent_signature(second)
