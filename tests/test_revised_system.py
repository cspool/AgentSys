from __future__ import annotations

from agentsys.revised_system import parse_revised_output


def test_parse_revised_output_and_hardware_lineage() -> None:
    output = """
AGENTSYS_REVISED_LAUNCH call=0 dynamic=1
AGENTSYS_TISA_ISSUE cycle=2 index=0 AGENTSYS_REVISED_TRACE version=1 events=4 digest=0001 mir=0002
engine=me source=10 flow=0 stage=0 placement=0 preemptible=1 priority=0 duration=80
AGENTSYS_TISA_COMPLETE cycle=82 index=0 engine=me source=10 checksum=0000000000001234 app_digest=4347e5adb9552f70
AGENTSYS_REVISED_DONE call=0 dynamic=1 system=90 dma=20 backend=83 submitted=1 completed=1 overlap=0 hptpe_mac_ops=20480 checksum=1234 bytes=96
AGENTSYS_REVISED_TRACE version=1 events=4 digest=0001 mir=0002
AGENTSYS_REVISED_CALL index=0 program=react call=c0 kind=llm priority=0 flow=reactive deps=0000 first=1 last=1 release=1 mllm=2 agentxpu=3 config_start=4 config_end=5 launch=6 wait=90 xpu=91 dma=92 complete=93 tool_start=0 tool_end=0 xpu_cycles=83 hptpe_ops=20480 dma_cycles=20 dma_bytes=96
AGENTSYS_REVISED_PASS backend=dynamic abi=xpu_v2 programs=1 calls=1 llm_calls=1 tool_calls=0 launches=1 descriptors=1 trace_events=4 cpu_cycles=100 config_cycles=1 system_cycles=90 backend_cycles=83 dma_cycles=20 dma_bytes=96 me_busy=80 ve_busy=0 de_busy=0 overlap=0 hptpe_mac_ops=20480 priority_violations=0 flows=1/0 placements=1/0/0 checksum=0000000000001234 app_digest=0000000000000001 mir_digest=0000000000000002
"""
    parsed = parse_revised_output(output)
    assert parsed["summary"]["abi"] == "xpu_v2"
    assert parsed["summary"]["hptpe_mac_ops"] == 20480
    assert parsed["hardware"][0]["call_index"] == 0
    assert parsed["hardware"][0]["source"] == 10
    assert parsed["hardware"][1]["checksum"] == 0x1234
    assert parsed["transport"] == {"repaired_frames": 1, "complete": True}
