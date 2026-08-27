from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MLLM_ROOT = PROJECT_ROOT / ".references/mllm"
DEFAULT_BUILD_DIR = MLLM_ROOT / "build-x86-cuda"
PINNED_MLLM = "50ad5a9b6fbea742e38b5b31776c187e50319c8e"
PINNED_SUBMODULES = {
    "mllm/backends/cuda/vendors/cccl": "9c40ed11560fa8ffd21abe4cdc8dc3ce875e48e3",
    "mllm/backends/cuda/vendors/cutlass": "e51efbfe18fe4f4cbb66ab814c55bf4aa0185491",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_head(path: Path) -> str | None:
    if not (path / ".git").exists():
        return None
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def _cache_value(path: Path, name: str) -> str | None:
    if not path.is_file():
        return None
    prefix = f"{name}:"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line.split("=", 1)[1]
    return None


def _run(command: list[str], *, env: dict[str, str] | None = None) -> dict[str, Any]:
    process = subprocess.run(
        command,
        cwd=MLLM_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return {
        "command": command,
        "exit_code": process.returncode,
        "output": process.stdout,
        "pass": process.returncode == 0,
    }


def _noncomment_lines(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("//")
    ]


def audit_mllm_cuda(
    *,
    run_id: str,
    build_dir: Path = DEFAULT_BUILD_DIR,
    nvcc: Path | None = None,
    recovery_evidence: bool = False,
    setup_log: Path | None = None,
) -> dict[str, Any]:
    nvcc_text = str(nvcc) if nvcc is not None else os.environ.get("CUDACXX")
    nvcc_text = nvcc_text or shutil.which("nvcc")
    nvcc_path = Path(nvcc_text).resolve() if nvcc_text else None
    nvcc_result = (
        _run([str(nvcc_path), "--version"])
        if nvcc_path is not None and nvcc_path.is_file()
        else {"command": [], "exit_code": None, "output": "nvcc not found", "pass": False}
    )

    submodules = {
        relative: {
            "expected": expected,
            "observed": _git_head(MLLM_ROOT / relative),
        }
        for relative, expected in PINNED_SUBMODULES.items()
    }
    cache = build_dir / "CMakeCache.txt"
    target_candidates = {
        "cuda_ops": build_dir / "lib/libMllmCUDABackendCudaOps.so",
        "cuda_backend": build_dir / "lib/libMllmCUDABackend.so",
        "device_test": build_dir / "bin/Mllm-Test-CUDA-DeviceInfo",
    }
    targets = {
        name: {
            "path": str(path),
            "exists": path.is_file() and path.stat().st_size > 0,
            "bytes": path.stat().st_size if path.is_file() else 0,
            "sha256": _sha256(path) if path.is_file() else None,
        }
        for name, path in target_candidates.items()
    }
    library_env = os.environ.copy()
    library_env["LD_LIBRARY_PATH"] = os.pathsep.join(
        [str(build_dir / "lib"), str(build_dir / "bin"), library_env.get("LD_LIBRARY_PATH", "")]
    )
    device_test = (
        _run([str(target_candidates["device_test"])], env=library_env)
        if targets["device_test"]["exists"]
        else {"command": [], "exit_code": None, "output": "device test not built", "pass": False}
    )
    ldd = (
        _run(["ldd", str(target_candidates["cuda_backend"])])
        if targets["cuda_backend"]["exists"]
        else {"command": [], "exit_code": None, "output": "CUDA backend not built", "pass": False}
    )

    kernel_sources = sorted(
        (MLLM_ROOT / "mllm/backends/cuda/kernels").glob("*.cu")
    )
    source_boundary = {
        "kernel_translation_units": [str(path.relative_to(MLLM_ROOT)) for path in kernel_sources],
        "noncomment_lines": {str(path.relative_to(MLLM_ROOT)): _noncomment_lines(path) for path in kernel_sources},
        "op_factory_registration": "regOpFactory<" in "\n".join(
            _noncomment_lines(MLLM_ROOT / "mllm/backends/cuda/CudaBackend.cpp")
        ),
        "classification": "upstream_cuda_device_metadata_and_allocator_scaffold",
    }
    native = json.loads(
        (PROJECT_ROOT / "artifacts/results/mllm-native-run_023.json").read_text(encoding="utf-8")
    )
    layer = json.loads(
        (
            PROJECT_ROOT
            / "artifacts/parameterized_reproduction/run_032/layer-regression/layer-regression.json"
        ).read_text(encoding="utf-8")
    )
    try:
        wheel_version = importlib.metadata.version("nvidia-cuda-nvcc-cu12")
    except importlib.metadata.PackageNotFoundError:
        wheel_version = None

    gates = {
        "nvcc_12_8": nvcc_result["pass"]
        and re.search(r"release 12\.8", nvcc_result["output"]) is not None,
        "pinned_cuda_submodules": all(
            item["observed"] == item["expected"] for item in submodules.values()
        ),
        "cuda_cache": _cache_value(cache, "MLLM_BUILD_CUDA_BACKEND") == "ON"
        and _cache_value(cache, "CMAKE_CUDA_ARCHITECTURES") == "89"
        and _cache_value(cache, "CMAKE_CUDA_COMPILER") is not None,
        "three_build_targets": all(item["exists"] for item in targets.values()),
        "two_gpu_device_test": device_test["pass"]
        and device_test["output"].count("Found device: NVIDIA GeForce RTX 4090") == 2,
        "cuda_driver_runtime_nvml_link": ldd["pass"]
        and "libcudart.so" in ldd["output"]
        and "libcuda.so" in ldd["output"]
        and "libnvidia-ml.so" in ldd["output"],
        "upstream_boundary_audited": len(kernel_sources) == 4
        and not any(source_boundary["noncomment_lines"].values())
        and not source_boundary["op_factory_registration"],
        "prior_mllm_and_regression_intact": native["summary"]["pass"]
        and native["summary"]["executables"] == 20
        and native["summary"]["gtest_cases_passed"] == 101
        and layer["summary"]["endpoints"] == layer["summary"]["passing"] == 68
        and layer["summary"]["max_relative_error"] <= 0.10,
    }
    recovery: dict[str, Any] | None = None
    if recovery_evidence:
        micromamba = PROJECT_ROOT / ".tools/micromamba"
        package_path = PROJECT_ROOT / "artifacts/gpu_runtime/cuda-conda-packages.json"
        explicit_path = PROJECT_ROOT / "artifacts/gpu_runtime/cuda-conda-explicit.txt"
        packages = (
            json.loads(package_path.read_text(encoding="utf-8"))
            if package_path.is_file()
            else []
        )
        cuda_packages = {item["name"]: item for item in packages if item["name"].startswith("cuda-")}
        setup_log = setup_log or PROJECT_ROOT / f"artifacts/logs/mllm-cuda-setup-{run_id}.log"
        setup_text = setup_log.read_text(encoding="utf-8") if setup_log.is_file() else ""
        micromamba_version = (
            subprocess.check_output([str(micromamba), "--version"], text=True).strip()
            if micromamba.is_file()
            else None
        )
        installed_packages = subprocess.check_output(
            ["dpkg-query", "-W", "-f=${binary:Package}\n"], text=True
        ).splitlines()
        driver_versions = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
            text=True,
        ).splitlines()
        recovery = {
            "micromamba": {
                "path": str(micromamba),
                "version": micromamba_version,
                "sha256": _sha256(micromamba) if micromamba.is_file() else None,
            },
            "conda_packages": packages,
            "explicit_lock": {
                "path": str(explicit_path),
                "sha256": _sha256(explicit_path) if explicit_path.is_file() else None,
            },
            "setup_log": {
                "path": str(setup_log),
                "sha256": _sha256(setup_log) if setup_log.is_file() else None,
            },
            "driver_versions": driver_versions,
        }
        gates.update(
            {
                "recovery_micromamba_pin": micromamba_version == "2.8.1"
                and recovery["micromamba"]["sha256"]
                == "9689782d863c05a1bf5d2d371ba527104e7a4eb4310c1637d8653b751aed9c82",
                "recovery_cuda_conda_lock": explicit_path.is_file()
                and cuda_packages.get("cuda-nvcc", {}).get("version") == "12.8.93"
                and cuda_packages.get("cuda-cudart-dev", {}).get("version") == "12.8.90"
                and cuda_packages.get("cuda-nvml-dev", {}).get("version") == "12.8.90"
                and all(
                    item.get("channel") == "nvidia/label/cuda-12.8.1"
                    for item in cuda_packages.values()
                ),
                "recovery_build_log_and_devices": setup_log.is_file()
                and "CXX compiler identification is Clang 16.0.6" in setup_text
                and "CUDA compiler identification is NVIDIA 12.8.93" in setup_text
                and setup_text.count("Found device: NVIDIA GeForce RTX 4090") == 2,
                "recovery_boundary_unchanged": gates["upstream_boundary_audited"],
                "recovery_project_local_only": not Path("/usr/local/cuda").exists()
                and not any(name.startswith("cuda-") for name in installed_packages)
                and driver_versions == ["595.84", "595.84"],
            }
        )
    return {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "pinned_upstream_mllm_cuda_backend_audit",
        "evidence_boundary": (
            "upstream CUDA initialization/allocator scaffold; not full mllm CUDA inference"
        ),
        "mllm": {"path": str(MLLM_ROOT), "commit": _git_head(MLLM_ROOT)},
        "compiler": {
            "wheel": "nvidia-cuda-nvcc-cu12",
            "wheel_version": wheel_version,
            "nvcc_path": str(nvcc_path) if nvcc_path is not None else None,
            "probe": nvcc_result,
        },
        "submodules": submodules,
        "build": {
            "path": str(build_dir),
            "cache": str(cache),
            "cuda_backend": _cache_value(cache, "MLLM_BUILD_CUDA_BACKEND"),
            "cuda_architectures": _cache_value(cache, "CMAKE_CUDA_ARCHITECTURES"),
            "cuda_compiler": _cache_value(cache, "CMAKE_CUDA_COMPILER"),
            "targets": targets,
        },
        "device_test": device_test,
        "linkage": ldd,
        "source_boundary": source_boundary,
        "recovery": recovery,
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "pass": all(gates.values()),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit the pinned upstream mllm CUDA backend")
    parser.add_argument("--run-id", default="run_034")
    parser.add_argument("--build-dir", type=Path, default=DEFAULT_BUILD_DIR)
    parser.add_argument("--nvcc", type=Path)
    parser.add_argument("--recovery-evidence", action="store_true")
    parser.add_argument("--setup-log", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/mllm-cuda-run_034.json",
    )
    args = parser.parse_args(argv)
    result = audit_mllm_cuda(
        run_id=args.run_id,
        build_dir=args.build_dir,
        nvcc=args.nvcc,
        recovery_evidence=args.recovery_evidence,
        setup_log=args.setup_log,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(args.output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
