from agentsys.agentix_serving_simulator import (
    WORKLOAD_CONFIGS,
    ServingMode,
    build_serving_trace,
    simulate_offline_batch,
)


def test_agentix_serving_trace_is_deterministic_and_mode_conserving() -> None:
    config = WORKLOAD_CONFIGS["mixed"]
    shapes = set()
    for mode in ServingMode:
        calls, arrivals, tokens = build_serving_trace(config, 10, mode)
        calls_again, arrivals_again, tokens_again = build_serving_trace(config, 10, mode)
        assert calls == calls_again
        assert arrivals == arrivals_again
        assert tokens == tokens_again
        shapes.add((len(calls), len(arrivals), sum(tokens.values())))
    assert len(shapes) == 1


def test_agentix_bulk_swap_offline_reduction_is_monotonic() -> None:
    results = [simulate_offline_batch(programs) for programs in (1000, 2000, 3000, 4000)]
    reductions = [item["reduction"] for item in results]
    assert all(0.10 <= item <= 0.40 for item in reductions)
    assert all(left < right for left, right in zip(reductions, reductions[1:]))
