from agentsys.experiments import _point, _range


def test_point_and_range_error_gates() -> None:
    assert _point("x", 1.14, 1.0, 0.15)["pass"]
    assert not _point("x", 1.16, 1.0, 0.15)["pass"]
    assert _range("r", 2.2, [2.0, 2.4], 0.15)["pass"]
    assert _range("r", 1.8, [2.0, 2.4], 0.15)["pass"]
    assert not _range("r", 1.6, [2.0, 2.4], 0.15)["pass"]

