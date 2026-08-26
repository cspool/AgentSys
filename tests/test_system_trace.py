import json
from pathlib import Path

from agentsys.system_trace import expand_system_events, parse_application_output


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_real_cpu_xpu_system_trace_artifact_and_parser() -> None:
    artifact = json.loads(
        (PROJECT_ROOT / "artifacts/results/system-trace-run_021.json").read_text()
    )
    assert artifact["summary"] == {"gates": 13, "passing": 13, "failing": 0, "pass": True}
    assert all(artifact["gates"].values())
    assert artifact["trace"] == {
        "events": 200,
        "layers": ["application", "cpu", "dma", "framework", "software", "xpu"],
    }
    static = parse_application_output(artifact["static"]["log"])
    dynamic = parse_application_output(artifact["dynamic"]["log"])
    assert static["summary"]["checksum"] == dynamic["summary"]["checksum"]
    assert static["summary"]["backend_cycles"] > dynamic["summary"]["backend_cycles"]
    events = expand_system_events("dynamic", dynamic["calls"])
    assert len(events) == 100
    assert all(left["cycle"] <= right["cycle"] for left, right in zip(events, events[1:]))
