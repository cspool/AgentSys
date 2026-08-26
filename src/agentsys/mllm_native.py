from __future__ import annotations

import hashlib
import os
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MLLM_ROOT = PROJECT_ROOT / ".references" / "mllm"
DEFAULT_BUILD_DIR = MLLM_ROOT / "build-clang16"
GTEST_PASSED_RE = re.compile(r"\[\s*PASSED\s*\]\s*(\d+)\s+tests?")
GTEST_SKIPPED_RE = re.compile(r"\[\s*SKIPPED\s*\]\s*(\d+)\s+tests?")


@dataclass(frozen=True, slots=True)
class NativeTestSpec:
    binary: str
    category: str
    timeout_s: int = 120
    args: tuple[str, ...] = ()


DEFAULT_NATIVE_TESTS = (
    NativeTestSpec("Mllm-Test-IR-TraceFooNet", "native_ir"),
    NativeTestSpec("Mllm-Test-Pass-ProgramLowering", "native_ir"),
    NativeTestSpec("Mllm-Test-SymbolicExpr", "native_ir"),
    NativeTestSpec(
        "Mllm-Test-CPUKernel",
        "cpu_kernel",
        240,
        (
            "--gtest_filter=ElementwiseKernelTest.AddFloat32:"
            "ElementwiseKernelTest.AddInt*:ElementwiseKernelTest.SubFloat32:"
            "ElementwiseKernelTest.SubInt*:ElementwiseKernelTest.MulFloat32:"
            "ElementwiseKernelTest.MulInt*:ElementwiseKernelTest.AddScalarFloat32:"
            "ElementwiseKernelTest.AddScalarInt*:ElementwiseKernelTest.SubScalarFloat32:"
            "ElementwiseKernelTest.SubScalarInt*:ElementwiseKernelTest.MulScalarFloat32:"
            "ElementwiseKernelTest.MulScalarInt*:ElementwiseKernelTest.DivScalarFloat32:"
            "ElementwiseKernelTest.DivScalarInt32:GELUKernelTest.*:LlamaFileKernelTest.*:"
            "TransposeKernelTest.*:PermuteKernelTest.*:TopKKernelTest.*:"
            "ReduceKernelTest.SumFloat32:Scatter2ShardsKernelTest.*",
        ),
    ),
    NativeTestSpec("Mllm-Test-KaiW4A32Pack", "quantization"),
    NativeTestSpec("Mllm-Test-CPUContiguousOp", "cpu_kernel"),
    NativeTestSpec("Mllm-Test-Qwen35-GDN", "model_operator", 240),
    NativeTestSpec("Mllm-Test-Qwen35-GDN-Conv", "model_operator", 240),
    NativeTestSpec("Mllm-Test-Qwen35-Tokenizer", "tokenizer"),
    NativeTestSpec("Mllm-Test-Qwen35-Config", "model_contract"),
    NativeTestSpec("Mllm-Test-MiniCPM5-Config", "model_contract"),
    NativeTestSpec("Mllm-Test-MiniCPM5-Model", "model_contract"),
    NativeTestSpec("Mllm-Test-Nn-KVHeadStaticCache", "kv_cache"),
    NativeTestSpec("Mllm-Test-Nn-GroupedQueryAttention", "attention"),
    NativeTestSpec("Mllm-Test-Core-ARGeneration", "generation_runtime"),
    NativeTestSpec("Mllm-Test-Core-Qwen35BenchmarkHarness", "benchmark_contract"),
    NativeTestSpec("Mllm-Test-Engine-RadixTree", "engine"),
    NativeTestSpec("Mllm-Test-Engine-RandomStates", "engine"),
    NativeTestSpec("Mllm-Test-Nn-FooNetTest", "eager_runtime"),
    NativeTestSpec("Mllm-Test-Nn-StaticCacheTest", "kv_cache"),
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_head(path: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def _cache_value(cache: Path, name: str) -> str | None:
    prefix = f"{name}:"
    for line in cache.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line.split("=", 1)[1]
    return None


def _tail(text: str, lines: int = 40) -> str:
    return "\n".join(text.splitlines()[-lines:])


def run_native_test(
    spec: NativeTestSpec,
    *,
    build_dir: Path = DEFAULT_BUILD_DIR,
) -> dict[str, Any]:
    binary = build_dir / "bin" / spec.binary
    if not binary.is_file() or not os.access(binary, os.X_OK):
        return {
            "binary": spec.binary,
            "category": spec.category,
            "pass": False,
            "reason": "missing executable",
        }
    env = os.environ.copy()
    library_paths = [str(build_dir / "bin"), str(build_dir / "lib")]
    if env.get("LD_LIBRARY_PATH"):
        library_paths.append(env["LD_LIBRARY_PATH"])
    env["LD_LIBRARY_PATH"] = os.pathsep.join(library_paths)
    started = time.monotonic_ns()
    try:
        proc = subprocess.run(
            [str(binary), *spec.args],
            cwd=MLLM_ROOT,
            env=env,
            text=True,
            capture_output=True,
            timeout=spec.timeout_s,
            check=False,
        )
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        proc = None
        timed_out = True
        stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
    elapsed_s = (time.monotonic_ns() - started) / 1e9
    if proc is not None:
        stdout = proc.stdout
        stderr = proc.stderr
        returncode = proc.returncode
    else:
        returncode = None
    combined = stdout + "\n" + stderr
    passed_match = GTEST_PASSED_RE.search(combined)
    skipped_match = GTEST_SKIPPED_RE.search(combined)
    return {
        "binary": spec.binary,
        "category": spec.category,
        "args": list(spec.args),
        "pass": not timed_out and returncode == 0,
        "returncode": returncode,
        "timed_out": timed_out,
        "elapsed_s": elapsed_s,
        "gtest_passed": int(passed_match.group(1)) if passed_match else None,
        "gtest_skipped": int(skipped_match.group(1)) if skipped_match else 0,
        "stdout_tail": _tail(stdout),
        "stderr_tail": _tail(stderr),
        "sha256": _sha256(binary),
    }


def run_native_mllm_suite(
    specs: Iterable[NativeTestSpec] = DEFAULT_NATIVE_TESTS,
    *,
    build_dir: Path = DEFAULT_BUILD_DIR,
    run_id: str,
) -> dict[str, Any]:
    specs = tuple(specs)
    cache = build_dir / "CMakeCache.txt"
    if not cache.is_file():
        raise FileNotFoundError(cache)
    results = [run_native_test(spec, build_dir=build_dir) for spec in specs]
    passed = sum(bool(result["pass"]) for result in results)
    gtest_passed = sum(result.get("gtest_passed") or 0 for result in results)
    gtest_skipped = sum(result.get("gtest_skipped") or 0 for result in results)
    return {
        "schema_version": 1,
        "run_id": run_id,
        "component": "mllm-native-framework",
        "evidence_type": "real_upstream_build_and_execution",
        "reference": {
            "path": str(MLLM_ROOT.relative_to(PROJECT_ROOT)),
            "commit": _git_head(MLLM_ROOT),
        },
        "build": {
            "path": str(build_dir.relative_to(PROJECT_ROOT)),
            "compiler": _cache_value(cache, "CMAKE_CXX_COMPILER"),
            "compiler_id": _cache_value(cache, "CMAKE_CXX_COMPILER_ID"),
            "build_type": _cache_value(cache, "CMAKE_BUILD_TYPE"),
            "threads": _cache_value(cache, "MLLM_KERNEL_USE_THREADS"),
            "openmp": _cache_value(cache, "MLLM_KERNEL_THREADS_VENDOR_OPENMP"),
        },
        "tests": results,
        "excluded": {
            "requires_external_model_or_tokenizer": [
                "Mllm-Test-Core-LoadParams",
                "Mllm-Test-MiniCPM5-Tokenizer official-tokenizer oracle",
            ],
            "not_a_finite_unit_test": ["Mllm-Test-Engine-Service"],
            "upstream_x86_nyi_or_crash_observed_in_unfiltered_cpu_suite": [
                "FP16 elementwise operations",
                "INT8/INT16 division",
                "ClipOp",
                "ReduceMeanFloat32",
                "CausalMask/Conv2D continuation after NYI failures",
            ],
        },
        "summary": {
            "executables": len(results),
            "executables_passed": passed,
            "gtest_cases_passed": gtest_passed,
            "gtest_cases_skipped": gtest_skipped,
            "pass": passed == len(results),
        },
    }
