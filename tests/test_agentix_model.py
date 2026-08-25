from agentsys.agentix_model import PROFILES, offline_makespan, run_agentix_aggregate, throughput_ratios


def test_agentix_component_equations_and_offline_monotonicity() -> None:
    assert all(all(value >= 1 for value in throughput_ratios(profile).values()) for profile in PROFILES.values())
    offline = [offline_makespan(count)["reduction"] for count in (1000, 2000, 3000, 4000)]
    assert all(left < right for left, right in zip(offline, offline[1:]))


def test_agentix_aggregate_registered_endpoints() -> None:
    result = run_agentix_aggregate(run_id="test")
    assert result["summary"]["pass"]
    assert result["summary"]["endpoints"] == 13

