from __future__ import annotations

from agentsys.revised_components import ACTIVE_COMPONENTS, audit_revised_components


def test_run025_active_component_certificate_excludes_atx() -> None:
    result = audit_revised_components(run_id="pytest")
    assert tuple(result["active_components"]) == ACTIVE_COMPONENTS
    assert result["excluded_components"] == ["atx"]
    assert result["summary"]["pass"]
    assert result["summary"]["components_passed"] == 5
    assert result["summary"]["endpoints_passed"] == 68
    assert result["summary"]["max_relative_error"] <= 0.15
