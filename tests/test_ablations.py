from agentsys.ablations import me_dataflow_ablation


def test_me_dataflow_ablation_conserves_macs() -> None:
    result = me_dataflow_ablation()
    assert result["macs"] == 32 * 2048 * 2048
    assert result["output_stationary"]["cycles"] > 0
    assert result["weight_stationary"]["cycles"] > 0
    assert result["ws_over_os_speedup"] > 0

