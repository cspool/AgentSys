from agentsys.model import Access, Engine, MemorySpan, Scope
from agentsys.tisa import TISAMode, TISASimulator, make_tile, semantic_hazards
from agentsys.workloads import tisa_model_workload


def test_semantic_hazard_serializes_alias_but_not_disjoint_scope() -> None:
    write = MemorySpan(0, 64, Access.WRITE, Scope.LOCAL, 0)
    read = MemorySpan(0, 64, Access.READ, Scope.LOCAL, 0)
    other = MemorySpan(0, 64, Access.READ, Scope.LOCAL, 1)
    older = make_tile("older", engine=Engine.ME, duration=20, sequence=0, operands=(write,))
    younger = make_tile("younger", engine=Engine.VE, duration=10, sequence=1, operands=(read,))
    independent = make_tile(
        "independent", engine=Engine.DE, duration=8, sequence=2, operands=(other,)
    )
    assert semantic_hazards(younger, older) == ("RAW",)
    assert semantic_hazards(independent, older) == ()

    result = TISASimulator(window=8, dispatch_latency=0).run(
        (older, younger, independent), TISAMode.DYNAMIC
    )
    issue = {item.tile_id: item for item in result.issues}
    assert issue["younger"].issue >= issue["older"].complete
    assert issue["independent"].issue == issue["older"].issue


def test_tisa_dynamic_preserves_work_and_overlaps_engines() -> None:
    workload = tisa_model_workload("bert", iterations=12)
    simulator = TISASimulator(window=8, dispatch_latency=7)
    naive = simulator.run(workload.tiles, TISAMode.NAIVE)
    static = simulator.run(workload.tiles, TISAMode.STATIC)
    dynamic = simulator.run(workload.tiles, TISAMode.DYNAMIC)

    expected = len(workload.tiles)
    assert naive.completed == static.completed == dynamic.completed == expected
    assert naive.busy_cycles == static.busy_cycles == dynamic.busy_cycles
    assert dynamic.cycles < naive.cycles
    assert dynamic.overlap_cycles["me_de"] > 0
    assert dynamic.dispatch_latency == 7

