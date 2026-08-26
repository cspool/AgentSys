from __future__ import annotations

import argparse
import json
from pathlib import Path

from .reproduce import reproduction_plan, run_serial_reproduction
from .toolchain import PROJECT_ROOT, load_toolchain_config


DEFAULT_REVISED_CONFIG = PROJECT_ROOT / "config/revised-toolchain.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Serially replay the five active revised components and Rocket+HPTPE system"
    )
    parser.add_argument("--run-id", default="run_028")
    parser.add_argument("--config", type=Path, default=DEFAULT_REVISED_CONFIG)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--toolchain-output", type=Path)
    parser.add_argument("--certificate-output", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    config = load_toolchain_config(args.config)
    if args.dry_run:
        print(json.dumps({"serial_plan": reproduction_plan(config)}, indent=2, sort_keys=True))
        return 0

    result = run_serial_reproduction(
        run_id=args.run_id,
        config_path=args.config,
        manifest_path=args.manifest,
        toolchain_output=args.toolchain_output,
        certificate_output=args.certificate_output,
    )
    print(json.dumps(result["manifest"]["summary"], indent=2, sort_keys=True))
    if result["toolchain"] is not None:
        print(json.dumps(result["toolchain"]["summary"], indent=2, sort_keys=True))
    if result["certificate"] is not None:
        print(json.dumps(result["certificate"]["summary"], indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
