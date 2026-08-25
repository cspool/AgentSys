from agentsys.agentxpu import AgentXPUSimulator, XPUConfig, XPUmode, poisson_mixed_flows


def test_heg_preserves_work_and_improves_reactive_latency() -> None:
    flows = poisson_mixed_flows(
        duration_s=90.0,
        proactive_rate_min=6.0,
        reactive_rate_min=3.0,
        seed=7,
    )
    simulator = AgentXPUSimulator(XPUConfig(tick_s=0.01))
    igpu = simulator.run(flows, XPUmode.IGPU)
    heg = simulator.run(flows, XPUmode.HEG)

    assert igpu.completed == heg.completed == len(flows)
    assert igpu.logical_input_tokens == heg.logical_input_tokens
    assert igpu.logical_output_tokens == heg.logical_output_tokens
    assert heg.reactive_mean_latency_s is not None
    assert igpu.reactive_mean_latency_s is not None
    assert heg.reactive_mean_latency_s < igpu.reactive_mean_latency_s
    assert 0 <= heg.igpu_utilization <= 1
    assert 0 <= heg.npu_utilization <= 1
