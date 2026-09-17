#!/usr/bin/env python3
"""Manual serial executor for Adapt Goals (user directive: goals are the
steps, Claude executes them). Transport-only replacement for the app-server
scheduler; every contract field, hash pin, ordering and immutability rule from
references/adapt-goal-contract.md is enforced here.

Usage:
  prep   <Axx>  : verify pinned source hashes, print sources + output path
  commit <Axx> --migrations <json>  : validate skill, write handoff, append ledger
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "manifests/adapt_goals.json"
RUN_ID = "adapt-agentix-manual-001"
RUN = ROOT / "manual_runs" / RUN_ID
HAND = RUN / "handoffs"
LEDGER = RUN / "ledger.json"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_plan():
    return json.loads(PLAN.read_text())


def goal_of(plan, gid):
    for g in plan["goals"]:
        if g["id"] == gid:
            return g
    sys.exit(f"no goal {gid}")


def ledger():
    return json.loads(LEDGER.read_text()) if LEDGER.exists() else {"run_id": RUN_ID, "entries": []}


def prep(gid):
    plan = load_plan()
    g = goal_of(plan, gid)
    led = ledger()
    done = [e["adapt_goal"] for e in led["entries"]]
    expect = f"A{len(done)+1:02d}"
    if gid != expect:
        sys.exit(f"serial order violation: next goal is {expect}, not {gid}")
    wf = g["workflow_input"]
    assert sha(Path(wf["path"])) == wf["sha256"], "workflow hash drift"
    for r in g.get("reference_skill_inputs", []):
        assert sha(Path(r["path"])) == r["sha256"], f"reference hash drift: {r['path']}"
    print(json.dumps({
        "goal": gid, "mode": g["mode"], "focus": g.get("focus", "")[:400],
        "workflow": wf["path"],
        "references": [r["path"] for r in g.get("reference_skills", [])],
        "output_skill": g["output_skill_path"],
        "runtime": {k: g[k] for k in ("runtime_branch", "runtime_goal", "runtime_predecessors")},
        "previous_handoff": (str(HAND / f"{done[-1]}.json") if done else None),
    }, indent=1, ensure_ascii=False))


def commit(gid, migrations_file):
    plan = load_plan()
    g = goal_of(plan, gid)
    led = ledger()
    done = [e["adapt_goal"] for e in led["entries"]]
    if gid in done:
        sys.exit("handoff already committed; never overwrite")
    if gid != f"A{len(done)+1:02d}":
        sys.exit("serial order violation")
    out = Path(g["output_skill_path"])
    assert out.is_file(), "output skill missing"
    text = out.read_text()
    assert "## Serial Runtime Contract" in text, "missing Serial Runtime Contract section"
    for key in ("runtime_branch=", "runtime_goal=", "runtime_predecessors=",
                "runtime_artifact_root=", "runtime_handoff_output=",
                "advance_only_after=complete"):
        assert key in text, f"runtime contract key missing: {key}"
    assert f"runtime_goal={g['runtime_goal']}" in text, "runtime_goal mismatch"
    mig = json.loads(Path(migrations_file).read_text())
    wf = g["workflow_input"]
    assert sha(Path(wf["path"])) == wf["sha256"]
    refs = []
    for r in g.get("reference_skill_inputs", []):
        assert sha(Path(r["path"])) == r["sha256"]
        refs.append({"requested_name": r["requested_name"],
                     "resolved_name": r["resolved_name"], "path": r["path"],
                     "sha256": r["sha256"], "resolution": r["resolution"]})
    prev = (str(HAND / f"{done[-1]}.json") if done else None)
    handoff = {
        "schema_version": 1,
        "adapt_run_id": RUN_ID,
        "adapt_goal": gid,
        "status": "complete",
        "mode": g["mode"],
        "workflow_execution_performed": False,
        "project_skill_execution_performed": False,
        "executor": "claude-session (user-directed manual serial execution; "
                    "app-server transport replaced, contract enforced here)",
        "inputs": {
            "workflow_files": [{"path": wf["path"], "sha256": wf["sha256"]}],
            "reference_skills": refs,
            "previous_adapt_handoff": prev,
        },
        "project_skill": {"name": g["output_skill"], "path": str(out),
                          "sha256": sha(out)},
        "text_migrations": mig.get("text_migrations", []),
        "uncovered_constraints_packaged": mig.get("uncovered_constraints_packaged", []),
        "runtime_contract": {
            "branch": g["runtime_branch"],
            "runtime_goal": g["runtime_goal"],
            "runtime_predecessors": g["runtime_predecessors"],
            "advance_only_after": "complete",
        },
        "validation": {
            "skill_structure_valid": True,
            "serial_runtime_contract_valid": True,
            "source_hashes_valid": True,
        },
        "committed_at": datetime.now(timezone.utc).isoformat(),
    }
    HAND.mkdir(parents=True, exist_ok=True)
    hp = HAND / f"{gid}.json"
    assert not hp.exists(), "handoff exists; immutable"
    hp.write_text(json.dumps(handoff, indent=1, ensure_ascii=False))
    led["entries"].append({"adapt_goal": gid, "handoff": str(hp),
                           "handoff_sha256": sha(hp),
                           "project_skill_sha256": handoff["project_skill"]["sha256"]})
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(led, indent=1, ensure_ascii=False))
    print(json.dumps({"committed": gid, "ledger_entries": len(led["entries"])}))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["prep", "commit"])
    ap.add_argument("goal")
    ap.add_argument("--migrations")
    a = ap.parse_args()
    if a.cmd == "prep":
        prep(a.goal)
    else:
        commit(a.goal, a.migrations)
