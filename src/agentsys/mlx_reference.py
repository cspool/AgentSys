from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from .workload import PROJECT_ROOT


DEFAULT_CONFIG = PROJECT_ROOT / "config/mlx-active-source.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_head(path: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_mlx_reference(
    *, config_path: Path = DEFAULT_CONFIG, run_id: str = "run_042"
) -> dict[str, Any]:
    config_path = config_path.resolve()
    config = _json(config_path)
    if config.get("schema_version") != 1:
        raise ValueError("unsupported MLX active-source contract")
    active = (PROJECT_ROOT / config["active_path"]).resolve()
    historical = (PROJECT_ROOT / config["historical_path"]).resolve()
    active_clean = not subprocess.check_output(
        ["git", "-C", str(active), "status", "--porcelain", "--untracked-files=no"],
        text=True,
    ).strip()
    source_evidence: dict[str, Any] = {}
    byte_identical = True
    for relative in config["core_sources"]:
        active_path = active / relative
        historical_path = historical / relative
        item = {
            "active": {
                "path": str(active_path),
                "exists": active_path.is_file(),
                "bytes": active_path.stat().st_size if active_path.is_file() else 0,
                "sha256": _sha256(active_path) if active_path.is_file() else None,
            },
            "historical": {
                "path": str(historical_path),
                "exists": historical_path.is_file(),
                "bytes": historical_path.stat().st_size if historical_path.is_file() else 0,
                "sha256": _sha256(historical_path) if historical_path.is_file() else None,
            },
        }
        item["byte_identical"] = (
            item["active"]["exists"]
            and item["historical"]["exists"]
            and item["active"]["sha256"] == item["historical"]["sha256"]
        )
        byte_identical = byte_identical and bool(item["byte_identical"])
        source_evidence[relative] = item

    frozen: dict[str, Any] = {}
    for name, relative in config["frozen_evidence"].items():
        path = active / relative
        frozen[name] = {
            "path": str(path),
            "bytes": path.stat().st_size,
            "sha256": _sha256(path),
            "value": _json(path),
        }
    standalone = frozen["standalone"]["value"]
    chipyard = frozen["chipyard"]["value"]
    core = frozen["core_claims"]["value"]
    e2e = frozen["paper_e2e"]["value"]
    full = frozen["full_paper"]["value"]

    array_text = (active / "rtl/mlx/mlx_array_4x4.sv").read_text(encoding="utf-8")
    pe_text = (active / "rtl/mlx/mlx_pe_top.sv").read_text(encoding="utf-8")
    rocc_text = (active / "rtl/mlx/mlx_rocc_controller.sv").read_text(
        encoding="utf-8"
    )
    scala_text = (active / "system_sim/chipyard/MLXRoCC.scala").read_text(
        encoding="utf-8"
    )
    e2e_summary = e2e["summary"]
    handoff = {
        "classification": "required_agentsys_mlx_integration_work",
        "primary_final_hardware": "ordinary_single_core_Rocket_plus_MLX",
        "excluded_primary_hardware": ["HPTPE", "native_RTX4090"],
        "retained_optional_evidence": ["HPTPE", "native_dual_GPU"],
        "tasks": [
            "compile Agentix-ordered Agent DAG calls into per-call MLX spatial programs",
            "preserve mllm source indices and Agent.xpu/TISA flow-stage metadata",
            "generate per-workload inputs, FP16 goldens, C header and RISC-V ELF",
            "execute CPU dependency/tool runtime plus MLX config-launch-wait-status",
            "run both MLX cycle and physical 4x4 RTL Rocket configurations",
            "merge application/framework/compiler/CPU/DMA/MLX traces by call identity",
            "add an executable MLX layer and sensitivity switch to the <=10% matrix",
            "issue a fresh MLX+CPU completion certificate",
        ],
    }
    gates = {
        "active_checkout": _git_head(active) == config["active_commit"]
        and active_clean,
        "historical_checkout_preserved": _git_head(historical)
        == config["historical_commit"],
        "core_sources_complete_and_unchanged": len(source_evidence) == 21
        and byte_identical,
        "mlx_architecture_present": all(
            token in array_text
            for token in (
                "parameter PE_COUNT = 16",
                "mlx_pe_top",
                "packet_route_grant",
                "packet_delivery_accept",
                "spm_select_valid",
            )
        )
        and "mlx_tag_buffer" in pe_text
        and "mlx_fu" in pe_text
        and "BACKEND == 0" in rocc_text
        and "MLXRTLRocketConfig" in scala_text,
        "frozen_standalone_supported": standalone["status"] == "supported"
        and all(standalone["checks"].values())
        and len(standalone["records"]) == 4,
        "frozen_chipyard_supported": chipyard["status"] == "supported"
        and all(chipyard["checks"].values())
        and len(chipyard["records"]) == 8,
        "target_free_core_claims": core["hypothesis_status"] == "supported"
        and core["summary"]["primary_claims"]
        == core["summary"]["primary_claims_reproduced"]
        == 5
        and core["summary"]["supporting_claims"]
        == core["summary"]["supporting_claims_reproduced"]
        == 3,
        "paper_e2e_five_at_10pct_bounded": e2e["hypothesis_status"] == "supported"
        and e2e["validation_eligible"] is False
        and e2e["paper_performance_targets_consumed"] is True
        and e2e_summary["performance_rows"] == 5
        and e2e_summary["fit_max_relative_error"] <= 0.10
        and e2e_summary["independent_validation_claimed"] is False,
        "strict_full_paper_negative_retained": full["summary"][
            "all_paper_experiments_reproduced_within_10pct"
        ]
        is False
        and full["summary"]["reproduced_within_10pct_count"] == 1
        and full["summary"]["not_fully_reproduced_count"] == 17,
        "agentsys_handoff_complete": len(handoff["tasks"]) == 8
        and handoff["primary_final_hardware"]
        == "ordinary_single_core_Rocket_plus_MLX",
    }
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "active_mlx_cpu_source_evidence_and_gap_audit",
        "evidence_boundary": (
            "MLX_dev is an open surrogate; target-free mechanism/RTL/Chipyard "
            "evidence and target-informed five-row paper regression are separate"
        ),
        "configuration": {"path": str(config_path), "sha256": _sha256(config_path)},
        "active": {"path": str(active), "commit": _git_head(active), "clean": active_clean},
        "historical": {"path": str(historical), "commit": _git_head(historical)},
        "chipyard": {
            "path": config["chipyard"]["path"],
            "expected_commit": config["chipyard"]["commit"],
            "observed_commit": _git_head(Path(config["chipyard"]["path"])),
        },
        "sources": source_evidence,
        "frozen_evidence": {
            name: {key: value for key, value in item.items() if key != "value"}
            for name, item in frozen.items()
        },
        "paper_regression": {
            "rows": e2e_summary["performance_rows"],
            "fit_mape": e2e_summary["fit_mape"],
            "max_relative_error": e2e_summary["fit_max_relative_error"],
            "leave_one_out_max_relative_error": e2e_summary[
                "leave_one_out_max_relative_error"
            ],
            "classification": config["paper_regression"]["classification"],
            "independent_validation": False,
        },
        "full_paper_scope": full["summary"],
        "handoff": handoff,
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "active_sources": len(source_evidence),
            "paper_rows_at_10pct": e2e_summary["performance_rows"],
            "full_paper_complete": False,
            "pass": all(gates.values()),
        },
    }
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit the active MLX+CPU source basis")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--run-id", default="run_042")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/mlx-reference-audit-run_042.json",
    )
    args = parser.parse_args(argv)
    result = audit_mlx_reference(config_path=args.config, run_id=args.run_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(args.output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
