from agentsys.chipyard import parse_elf_result


def test_parse_chipyard_result_line() -> None:
    line = (
        "AGENTSYS_ELF_PASS backend=dynamic wait=26 host_config=198 "
        "host_launch_wait=322 system=287 dma=36 kernel=249 submitted=8 "
        "issued=8 completed=8 canceled=0 me_busy=160 ve_busy=80 de_busy=80 "
        "dep_stall=227 resource_stall=80 pair_overlap=79 triple_overlap=0 "
        "decisions=8 prefetch=1/1 dma_bytes=96 checksum=a42f89ec1a613914 "
        "priority_violations=0 engine_issues=2/2/4\n"
    )
    result = parse_elf_result(line)
    assert result["verdict"] == "PASS"
    assert result["backend"] == "dynamic"
    assert result["engine_issues"] == [2, 2, 4]
    assert result["prefetch_hits"] == result["prefetch_requests"] == 1
    assert result["checksum_hex"] == "a42f89ec1a613914"

