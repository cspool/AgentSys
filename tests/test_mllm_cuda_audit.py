from __future__ import annotations

import json
import os

from agentsys.mllm_cuda_audit import MLLM_ROOT, PINNED_MLLM, PROJECT_ROOT


def test_mllm_cuda_setup_is_executable_and_pinned() -> None:
    setup = PROJECT_ROOT / "scripts/setup_mllm_cuda.sh"
    assert setup.is_file() and os.access(setup, os.X_OK)
    text = setup.read_text(encoding="utf-8")
    assert PINNED_MLLM in text
    assert "CMAKE_CUDA_ARCHITECTURES=89" in text
    assert "MLLM_BUILD_CUDA_BACKEND=ON" in text
    assert "Mllm-Test-CUDA-DeviceInfo" in text


def test_upstream_mllm_cuda_boundary_is_not_overstated() -> None:
    result = json.loads(
        (PROJECT_ROOT / "artifacts/results/mllm-cuda-run_034.json").read_text(
            encoding="utf-8"
        )
    )
    assert result["mllm"]["commit"] == PINNED_MLLM
    assert result["compiler"]["wheel_version"] == "12.8.93"
    assert result["compiler"]["nvcc_path"] is None
    assert result["source_boundary"]["classification"] == (
        "upstream_cuda_device_metadata_and_allocator_scaffold"
    )
    assert len(result["source_boundary"]["kernel_translation_units"]) == 4
    assert not any(result["source_boundary"]["noncomment_lines"].values())
    assert not result["source_boundary"]["op_factory_registration"]
    assert result["summary"] == {
        "failing": 5,
        "gates": 8,
        "pass": False,
        "passing": 3,
    }
    assert result["gates"]["pinned_cuda_submodules"]
    assert result["gates"]["upstream_boundary_audited"]
    assert result["gates"]["prior_mllm_and_regression_intact"]
    assert not result["gates"]["nvcc_12_8"]
    assert (MLLM_ROOT / "mllm/backends/cuda/vendors/cccl/.git").is_file()
    assert (MLLM_ROOT / "mllm/backends/cuda/vendors/cutlass/.git").is_file()


def test_run035_recovers_nvcc_and_retains_upstream_cmake_failure() -> None:
    result = json.loads(
        (PROJECT_ROOT / "artifacts/results/mllm-cuda-run_035.json").read_text(
            encoding="utf-8"
        )
    )
    assert result["compiler"]["probe"]["pass"]
    assert "release 12.8" in result["compiler"]["probe"]["output"]
    assert result["build"]["cuda_backend"] == "ON"
    assert result["build"]["cuda_architectures"] == "89"
    assert result["summary"] == {
        "failing": 4,
        "gates": 13,
        "pass": False,
        "passing": 9,
    }
    for gate in (
        "nvcc_12_8",
        "cuda_cache",
        "recovery_micromamba_pin",
        "recovery_cuda_conda_lock",
        "recovery_boundary_unchanged",
        "recovery_project_local_only",
    ):
        assert result["gates"][gate]
    assert not result["gates"]["three_build_targets"]
    assert not result["gates"]["two_gpu_device_test"]
    assert "target \"mllm-params-inspector\" which does not exist" in (
        PROJECT_ROOT / "artifacts/logs/mllm-cuda-setup-run_035.log"
    ).read_text(encoding="utf-8")
