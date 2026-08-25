from pathlib import Path

from agentsys.mllm_backend import engine_for_op, lower_to_tiles, operator_digest, parse_mir
from agentsys.model import Engine


FIXTURE = Path(__file__).resolve().parents[1] / "integrations/mllm/fixtures/transformer_slice.mir"


def test_mllm_fixture_parsing_and_lowering_is_deterministic() -> None:
    first = parse_mir(FIXTURE)
    second = parse_mir(FIXTURE)
    assert len(first) == 8
    assert operator_digest(first) == operator_digest(second)
    assert {operator.engine for operator in first} == {Engine.ME, Engine.VE, Engine.DE}
    tiles = lower_to_tiles(first)
    assert len(tiles) == len(first)
    assert all(all(int(dep.rsplit("-", 1)[1]) < tile.sequence for dep in tile.deps) for tile in tiles)


def test_mllm_engine_mapping() -> None:
    assert engine_for_op("LinearOp") is Engine.ME
    assert engine_for_op("SoftmaxOp") is Engine.VE
    assert engine_for_op("TransposeOp") is Engine.DE

