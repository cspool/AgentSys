from agentsys.mllm_backend import parse_mir
from agentsys.ramulator import PROJECT_ROOT, config_text, generate_load_store_records


def test_ramulator_trace_generation_and_config() -> None:
    fixture = PROJECT_ROOT / "integrations/mllm/fixtures/transformer_slice.mir"
    records, metadata = generate_load_store_records(parse_mir(fixture), max_records=10000)
    assert metadata["records"] == len(records) > 0
    assert metadata["loads"] > 0 and metadata["stores"] > 0
    assert all(record.startswith(("LD ", "ST ")) for record in records)
    config = config_text(PROJECT_ROOT / "trace.txt", 2)
    assert "impl: LoadStoreTrace" in config
    assert "channel: 2" in config

