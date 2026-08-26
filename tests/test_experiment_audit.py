from agentsys.experiments import _point, _range


def test_point_and_range_error_gates() -> None:
    assert _point("x", 1.09, 1.0, 0.10)["pass"]
    assert not _point("x", 1.11, 1.0, 0.10)["pass"]
    assert _range("r", 2.2, [2.0, 2.4], 0.10)["pass"]
    assert _range("r", 1.8, [2.0, 2.4], 0.10)["pass"]
    assert not _range("r", 1.79, [2.0, 2.4], 0.10)["pass"]
