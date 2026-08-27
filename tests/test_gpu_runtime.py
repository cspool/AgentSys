from __future__ import annotations

import json
import os
from pathlib import Path

from agentsys.gpu_runtime import PROJECT_ROOT, _cpus


CONFIG = PROJECT_ROOT / "config/local-dual-gpu.json"
RUNTIME_ROOT = PROJECT_ROOT / "artifacts/gpu_runtime"
RUN_DIR = RUNTIME_ROOT / "run_033"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_gpu_config_maps_each_rank_to_its_local_numa_socket() -> None:
    config = _json(CONFIG)
    assert config["schema_version"] == 1
    assert config["backend"] == "nccl"
    assert [gpu["device"] for gpu in config["gpus"]] == [0, 1]
    assert [gpu["numa_node"] for gpu in config["gpus"]] == [0, 1]
    assert [len(_cpus(gpu["cpu_affinity"])) for gpu in config["gpus"]] == [32, 32]
    assert _cpus(config["gpus"][0]["cpu_affinity"]).isdisjoint(
        _cpus(config["gpus"][1]["cpu_affinity"])
    )
    assert config["benchmark"]["matrix_size"] == 4096
    assert config["benchmark"]["all_reduce_mib"] == 64


def test_gpu_runtime_setup_and_entrypoints_are_pinned() -> None:
    setup = PROJECT_ROOT / "scripts/setup_gpu_runtime.sh"
    requirements = (
        PROJECT_ROOT / "config/gpu-runtime-requirements.txt"
    ).read_text(encoding="utf-8")
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert setup.is_file() and os.access(setup, os.X_OK)
    assert "torch==2.7.0+cu128" in requirements
    assert "numpy==2.2.6" in requirements
    assert "nvidia-ml-py==13.610.43" in requirements
    assert "agentsys-gpu-runtime" in pyproject
    assert "agentsys-gpu-runtime-audit" in pyproject


def test_run033_executes_two_real_gpus_and_two_cpu_numa_domains() -> None:
    runtime = _json(RUN_DIR / "gpu-runtime.json")
    assert runtime["classification"] == (
        "native_dual_rtx4090_dual_numa_cpu_runtime_measurement"
    )
    assert "not A100/Core-Ultra" in runtime["evidence_boundary"]
    assert runtime["summary"] == {
        "events": 12,
        "failing": 0,
        "gates": 11,
        "gpus": 2,
        "numa_nodes": 2,
        "pass": True,
        "passing": 11,
    }
    assert all(runtime["gates"].values())
    ranks = runtime["ranks"]
    assert [rank["device"] for rank in ranks] == [0, 1]
    assert [rank["numa_node"] for rank in ranks] == [0, 1]
    assert len({rank["nvml_before"]["uuid"] for rank in ranks}) == 2
    assert all(rank["device_name"] == "NVIDIA GeForce RTX 4090" for rank in ranks)
    assert all(rank["compute_capability"] == [8, 9] for rank in ranks)
    assert all(rank["configured_affinity"] == rank["observed_affinity"] for rank in ranks)
    assert all(rank["torch_cpu_threads"] == 16 for rank in ranks)
    assert all(rank["gpu"]["matmul_tflops"] > 100 for rank in ranks)
    assert all(not any(rank["p2p"].values()) for rank in ranks)
    assert all(rank["collective"]["correct"] for rank in ranks)
    assert {rank["collective"]["observed"] for rank in ranks} == {3.0}
    assert ranks[0]["gpu"]["checksum"] == ranks[1]["gpu"]["checksum"]


def test_run033_nsight_and_software_evidence_are_machine_audited() -> None:
    environment = _json(RUNTIME_ROOT / "environment.json")
    audit = _json(RUN_DIR / "gpu-runtime-audit.json")
    assert environment["torch"] == "2.7.0+cu128"
    assert environment["torch_cuda"] == "12.8"
    assert environment["nccl"] == [2, 26, 2]
    assert environment["devices"] == [
        "NVIDIA GeForce RTX 4090",
        "NVIDIA GeForce RTX 4090",
    ]
    assert audit["summary"] == {
        "failing": 0,
        "gates": 9,
        "pass": True,
        "passing": 9,
    }
    assert all(audit["gates"].values())
    assert audit["kernel_rows"] >= 3
    assert audit["api_rows"] >= 2
    assert audit["memory_rows"] >= 2
    assert (RUN_DIR / "nsight-dual-gpu.nsys-rep").stat().st_size > 1_000_000
    assert (RUN_DIR / "nsight-dual-gpu.sqlite").stat().st_size > 1_000_000
    assert all(
        (RUN_DIR / f"rank{rank}-torch-trace.json").stat().st_size > 0
        for rank in (0, 1)
    )
