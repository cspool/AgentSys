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


def test_run036_builds_cuda_objects_and_retains_openmp_link_failure() -> None:
    result = json.loads(
        (PROJECT_ROOT / "artifacts/results/mllm-cuda-run_036.json").read_text(
            encoding="utf-8"
        )
    )
    assert result["summary"] == {
        "failing": 4,
        "gates": 13,
        "pass": False,
        "passing": 9,
    }
    assert result["build"]["targets"]["cuda_ops"]["exists"]
    assert not result["build"]["targets"]["cuda_backend"]["exists"]
    assert not result["build"]["targets"]["device_test"]["exists"]
    log = (PROJECT_ROOT / "artifacts/logs/mllm-cuda-setup-run_036.log").read_text(
        encoding="utf-8"
    )
    assert "Linking CUDA shared library bin/libMllmCUDABackendCudaOps.so" in log
    assert "cannot find -lomp" in log


def test_run037_links_core_and_retains_conda_nvml_stub_path_failure() -> None:
    result = json.loads(
        (PROJECT_ROOT / "artifacts/results/mllm-cuda-run_037.json").read_text(
            encoding="utf-8"
        )
    )
    assert result["summary"]["passing"] == 9
    assert result["build"]["targets"]["cuda_ops"]["exists"]
    log = (PROJECT_ROOT / "artifacts/logs/mllm-cuda-setup-run_037.log").read_text(
        encoding="utf-8"
    )
    assert "Linking CXX shared library bin/libMllmRT.so" in log
    assert "cannot find -lnvidia-ml" in log
    assert (PROJECT_ROOT / ".cuda-toolkit/targets/x86_64-linux/lib/stubs/libnvidia-ml.so").is_file()


def test_run038_builds_backend_and_exposes_cuda_shutdown_order_bug() -> None:
    result = json.loads(
        (PROJECT_ROOT / "artifacts/results/mllm-cuda-run_038.json").read_text(
            encoding="utf-8"
        )
    )
    assert result["summary"] == {
        "failing": 2,
        "gates": 13,
        "pass": False,
        "passing": 11,
    }
    assert all(item["exists"] for item in result["build"]["targets"].values())
    assert result["gates"]["cuda_driver_runtime_nvml_link"]
    assert not result["gates"]["two_gpu_device_test"]
    assert result["device_test"]["output"].count(
        "Found device: NVIDIA GeForce RTX 4090"
    ) == 2
    assert "driver shutting down" in result["device_test"]["output"]
    assert "framework_patch" not in result


def test_run039_patched_backend_passes_twice_with_exact_boundary() -> None:
    result = json.loads(
        (PROJECT_ROOT / "artifacts/results/mllm-cuda-run_039.json").read_text(
            encoding="utf-8"
        )
    )
    assert result["summary"] == {
        "failing": 0,
        "gates": 13,
        "pass": True,
        "passing": 13,
    }
    assert all(result["gates"].values())
    assert result["device_test"]["exit_code"] == 0
    assert result["device_test"]["output"].count(
        "Found device: NVIDIA GeForce RTX 4090"
    ) == 2
    assert result["framework_patch"]["applied"]
    assert result["framework_patch"]["sha256"] == (
        "8d5514345283fe37f8ece4d0a0bd4d679804afe9eb5e25b90433d0a41afafd3c"
    )
    assert result["framework_patch"]["upstream_diff"].count(
        "+  Context::instance().memoryManager()->clearAll();"
    ) == 1
    linkage = result["linkage"]["output"]
    assert "/usr/lib/x86_64-linux-gnu/libcuda.so.1" in linkage
    assert "/usr/lib/x86_64-linux-gnu/libnvidia-ml.so.1" in linkage
    first = (PROJECT_ROOT / "artifacts/logs/mllm-cuda-setup-run_039-first.log").read_text(
        encoding="utf-8"
    )
    second = (PROJECT_ROOT / "artifacts/logs/mllm-cuda-setup-run_039-second.log").read_text(
        encoding="utf-8"
    )
    assert first.count("Found device: NVIDIA GeForce RTX 4090") == 2
    assert second.count("Found device: NVIDIA GeForce RTX 4090") == 2
    assert second.count("ninja: no work to do.") == 3
