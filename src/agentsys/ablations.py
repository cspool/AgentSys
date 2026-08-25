from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

from .agentxpu import AgentXPUSimulator, XPUConfig, XPUmode, poisson_mixed_flows
from .tisa import TISAMode, TISASimulator
from .workloads import tisa_model_workload


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _load_artifact(relative: str) -> tuple[dict[str, Any], str]:
    path = PROJECT_ROOT / relative
    return json.loads(path.read_text(encoding="utf-8")), hashlib.sha256(path.read_bytes()).hexdigest()


def me_dataflow_ablation(*, m: int = 32, n: int = 2048, k: int = 2048, array: int = 16, bytes_per_cycle: int = 4) -> dict[str, Any]:
    tile_m = math.ceil(m / array)
    tile_n = math.ceil(n / array)
    macs = m * n * k
    compute_cycles = tile_m * tile_n * (k + 2 * array - 2)
    output_bytes = m * n * 4
    os_bytes = tile_m * tile_n * ((array * k + k * array) * 2) + output_bytes
    ws_bytes = tile_n * k * array * 2 + tile_m * array * k * 2 + output_bytes
    os_cycles = max(compute_cycles, math.ceil(os_bytes / bytes_per_cycle))
    ws_cycles = max(compute_cycles, math.ceil(ws_bytes / bytes_per_cycle))
    return {
        "shape": [m, n, k],
        "array": [array, array],
        "macs": macs,
        "compute_cycles": compute_cycles,
        "bytes_per_cycle": bytes_per_cycle,
        "output_stationary": {"bytes": os_bytes, "cycles": os_cycles},
        "weight_stationary": {"bytes": ws_bytes, "cycles": ws_cycles},
        "ws_over_os_speedup": os_cycles / ws_cycles,
    }


def run_ablations(*, run_id: str = "run_013") -> dict[str, Any]:
    # Agent.xpu preemption granularity, same immutable 8B trace.
    flows = poisson_mixed_flows(
        duration_s=300,
        proactive_rate_min=6,
        reactive_rate_min=3,
        seed=313,
    )
    base = XPUConfig(tick_s=0.01)
    preemption: dict[str, Any] = {}
    preemption_work: set[tuple[int, int]] = set()
    percentile_valid = True
    for chunk in (8, 16, 32, 64, 256):
        config = replace(
            base,
            heg_prefill_chunk_tokens=chunk,
            igpu_prefill_tokens_s=base.igpu_prefill_tokens_s * 0.48,
            serial_prefill_tokens_s=base.serial_prefill_tokens_s * 0.48,
            heg_prefill_tokens_s=base.heg_prefill_tokens_s * 0.48,
            igpu_decode_tokens_s=base.igpu_decode_tokens_s * 0.48,
            heg_decode_tokens_s=base.heg_decode_tokens_s * 0.48,
        )
        result = AgentXPUSimulator(config).run(flows, XPUmode.HEG)
        preemption_work.add((result.logical_input_tokens, result.logical_output_tokens))
        if result.reactive_mean_latency_s is None or result.reactive_p90_latency_s is None or result.reactive_p99_latency_s is None:
            percentile_valid = False
        else:
            percentile_valid = percentile_valid and (
                result.reactive_mean_latency_s <= result.reactive_p90_latency_s <= result.reactive_p99_latency_s
            )
        preemption[str(chunk)] = result.to_dict()

    # TISA issue-window sensitivity.
    workload = tisa_model_workload("llama2", iterations=16)
    windows: dict[str, Any] = {}
    window_work: set[tuple[tuple[str, int], ...]] = set()
    for window in (1, 2, 4, 8, 16, 32):
        result = TISASimulator(window=window, dispatch_latency=7).run(workload.tiles, TISAMode.DYNAMIC)
        window_work.add(tuple(sorted(result.busy_cycles.items())))
        windows[str(window)] = result.to_dict()

    atx, atx_hash = _load_artifact("artifacts/results/atx-run_004.json")
    run007, run007_hash = _load_artifact("artifacts/results/full-stack-run_007.json")
    run008, run008_hash = _load_artifact("artifacts/results/full-stack-run_008.json")
    ramulator, ramulator_hash = _load_artifact("artifacts/results/ramulator2-run_012.json")
    dataflow = me_dataflow_ablation()
    dataflow_valid = (
        dataflow["macs"] > 0
        and dataflow["output_stationary"]["bytes"] > 0
        and dataflow["weight_stationary"]["bytes"] > 0
        and dataflow["output_stationary"]["cycles"] > 0
        and dataflow["weight_stationary"]["cycles"] > 0
    )

    gates = {
        "preemption_all_complete": all(value["completed"] == len(flows) for value in preemption.values()),
        "preemption_same_work": len(preemption_work) == 1,
        "percentiles_ordered": percentile_valid,
        "window_same_work": len(window_work) == 1,
        "window_all_complete": all(value["completed"] == len(workload.tiles) for value in windows.values()),
        "dataflow_equal_macs_positive": dataflow_valid,
        "source_artifacts_pass": atx["summary"]["pass"] and run007["summary"]["pass"] and run008["summary"]["pass"] and ramulator["summary"]["pass"],
    }
    return {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "cross_layer_sensitivity_ablation",
        "preemption_chunk_tokens": preemption,
        "tisa_window": windows,
        "atx_prefetch": {
            name: {
                "no_prefetch_vs_l2": value["ratios"]["vs_l2_no_prefetch"],
                "full_prefetch_vs_l2": value["ratios"]["vs_l2_prefetch"],
            }
            for name, value in atx["kernels"].items()
        },
        "priority": {
            "no_top_priority_reactive": run007["configurations"]["full_stack"]["reactive_completion"],
            "urgency_first_reactive": run008["configurations"]["full_stack"]["reactive_completion"],
            "reactive_speedup": run007["configurations"]["full_stack"]["reactive_completion"]
            / run008["configurations"]["full_stack"]["reactive_completion"],
        },
        "memory_bandwidth": ramulator["derived"],
        "me_dataflow": dataflow,
        "sources": {
            "atx_run004_sha256": atx_hash,
            "full_stack_run007_sha256": run007_hash,
            "full_stack_run008_sha256": run008_hash,
            "ramulator_run012_sha256": ramulator_hash,
        },
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "pass": all(gates.values()),
        },
    }

