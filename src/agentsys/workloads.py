from __future__ import annotations

from dataclasses import dataclass

from .agentix import CallSpec
from .model import Access, Engine, MemorySpan, Scope
from .tisa import make_tile


@dataclass(frozen=True, slots=True)
class TISAWorkload:
    name: str
    tiles: tuple
    engine_work: dict[str, int]


_MODEL_ENGINE_WORK = {
    # Target-independent decomposition: ME work is held fixed while VE/DE
    # pressure follows each model family's operator mix. Units are abstract
    # accelerator cycles and are split across the same seven-stage template.
    "resnet50": {"me": 200, "ve": 40, "de": 64},
    "bert": {"me": 200, "ve": 80, "de": 78},
    "gptj": {"me": 200, "ve": 70, "de": 78},
    "llama2": {"me": 200, "ve": 90, "de": 94},
    # FA3 head-dim 128 follows the paper's 1:8 vector:matrix compute ratio.
    "fa3_h128": {"me": 256, "ve": 32, "de": 80},
}


def tisa_model_workload(name: str, *, iterations: int = 32) -> TISAWorkload:
    if name not in _MODEL_ENGINE_WORK:
        raise ValueError(f"unknown TISA model workload: {name}")
    if iterations <= 0:
        raise ValueError("iterations must be positive")
    work = _MODEL_ENGINE_WORK[name]
    me_a = work["me"] // 2
    me_b = work["me"] - me_a
    ve_a = work["ve"] // 2
    ve_b = work["ve"] - ve_a
    de_a = work["de"] // 3
    de_b = work["de"] // 3
    de_c = work["de"] - de_a - de_b
    tiles = []
    sequence = 0

    for iteration in range(iterations):
        base = iteration * 0x10000
        spans = {
            "q": MemorySpan(base + 0x0000, 0x1000, Access.READ, Scope.DDR, 0),
            "k": MemorySpan(base + 0x1000, 0x1000, Access.READ, Scope.DDR, 1),
            "v": MemorySpan(base + 0x2000, 0x1000, Access.READ, Scope.DDR, 2),
            "p": MemorySpan(base + 0x3000, 0x1000, Access.WRITE, Scope.LOCAL, 0),
            "s": MemorySpan(base + 0x3000, 0x1000, Access.READ_WRITE, Scope.LOCAL, 0),
            "r": MemorySpan(base + 0x4000, 0x1000, Access.WRITE, Scope.LOCAL, 1),
            "o": MemorySpan(base + 0x4000, 0x1000, Access.READ_WRITE, Scope.LOCAL, 1),
            "out": MemorySpan(base + 0x5000, 0x1000, Access.WRITE, Scope.DDR, 3),
        }
        prefix = f"{name}-i{iteration}"
        static_group = iteration if name == "fa3_h128" else iteration // 2
        load = f"{prefix}-load-qk"
        gemm0 = f"{prefix}-gemm-qk"
        softmax = f"{prefix}-softmax"
        load_v = f"{prefix}-load-v"
        gemm1 = f"{prefix}-gemm-v"
        rescale = f"{prefix}-rescale"
        store = f"{prefix}-store"
        values = (
            (load, Engine.DE, de_a, (spans["q"], spans["k"]), (), "load"),
            (gemm0, Engine.ME, me_a, (spans["q"], spans["k"], spans["p"]), (load,), "gemm"),
            (softmax, Engine.VE, ve_a, (spans["s"],), (gemm0,), "softmax"),
            (load_v, Engine.DE, de_b, (spans["v"],), (), "load"),
            (
                gemm1,
                Engine.ME,
                me_b,
                (MemorySpan(spans["s"].base, spans["s"].size, Access.READ, Scope.LOCAL, 0), spans["v"], spans["r"]),
                (softmax, load_v),
                "gemm",
            ),
            (rescale, Engine.VE, ve_b, (spans["o"],), (gemm1,), "rescale"),
            (
                store,
                Engine.DE,
                de_c,
                (MemorySpan(spans["o"].base, spans["o"].size, Access.READ, Scope.LOCAL, 1), spans["out"]),
                (rescale,),
                "store",
            ),
        )
        for tile_id, engine, duration, operands, deps, op_type in values:
            tiles.append(
                make_tile(
                    tile_id,
                    engine=engine,
                    duration=duration,
                    sequence=sequence,
                    operands=operands,
                    deps=deps,
                    static_group=static_group,
                    op_type=op_type,
                    task_id=f"{prefix}-task",
                    flow_id=f"{prefix}-flow",
                    call_id=f"{prefix}-call",
                    program_id=f"{name}-program",
                )
            )
            sequence += 1
    return TISAWorkload(name=name, tiles=tuple(tiles), engine_work=dict(work))


def dynamic_agent_dag() -> tuple[CallSpec, ...]:
    """Representative tool-use + parallel MoA + reduce DAG."""

    return (
        CallSpec("react-plan", "react", 4, program_arrival=0),
        CallSpec("react-tool", "react", 1, deps=("react-plan",), external_delay=1),
        CallSpec("react-answer", "react", 3, deps=("react-tool",)),
        CallSpec("moa-map0", "moa", 3, program_arrival=0, thread_id="map0"),
        CallSpec("moa-map1", "moa", 5, program_arrival=0, thread_id="map1"),
        CallSpec("moa-map2", "moa", 2, program_arrival=0, thread_id="map2"),
        CallSpec(
            "moa-reduce",
            "moa",
            4,
            deps=("moa-map0", "moa-map1", "moa-map2"),
            thread_id="reduce",
        ),
        CallSpec("mcts-root", "mcts", 3, program_arrival=1, thread_id="root"),
        CallSpec("mcts-actor0", "mcts", 4, deps=("mcts-root",), thread_id="actor0"),
        CallSpec("mcts-actor1", "mcts", 2, deps=("mcts-root",), thread_id="actor1"),
        CallSpec("mcts-critic", "mcts", 3, deps=("mcts-actor0", "mcts-actor1"), thread_id="critic"),
    )
