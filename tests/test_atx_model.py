from agentsys.atx_model import PROFILES, llc_task_size_speedup, organization_times, run_atx_audit


def test_atx_equations_and_monotonicity() -> None:
    for profile in PROFILES.values():
        times = organization_times(profile)
        assert times.atx <= times.atx_no_prefetch <= times.l2_oca
    sizes = [8, 16, 32, 64, 128]
    values = [llc_task_size_speedup(size) for size in sizes]
    assert all(left > right for left, right in zip(values, values[1:]))


def test_atx_registered_endpoints() -> None:
    result = run_atx_audit(run_id="test")
    assert result["summary"]["pass"]
    assert result["summary"]["endpoints"] == 18

