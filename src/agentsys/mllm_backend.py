from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .model import Access, Engine, MemorySpan, Priority, Scope, Tile
from .tisa import TISAMode, TISASimulator


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MLLM_ROOT = PROJECT_ROOT / ".references" / "mllm"
OP_RE = re.compile(r"linalg\.([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)")
TENSOR_RE = re.compile(
    r"%(\d+):tensor<\[([^\]]*)\],\s*([^,>]+),\s*([A-Za-z0-9_]+)>"
)


ME_OPS = {"LinearOp", "MatMulOp", "EmbeddingOp", "FlashAttention2Op", "GroupedQueryAttentionDecodeOp"}
DE_OPS = {
    "ViewOp",
    "ReshapeOp",
    "TransposeOp",
    "SliceOp",
    "ConcatOp",
    "RepeatOp",
    "PermuteOp",
    "CastTypeOp",
    "CopyOp",
    "CloneOp",
    "IndexOp",
    "KVCacheOp",
    "ContiguousOp",
    "SplitOp",
    "StackOp",
}


DTYPE_BYTES = {
    "Float64": 8,
    "Float32": 4,
    "Int32": 4,
    "Float16": 2,
    "BFloat16": 2,
    "UInt16PerTensor": 2,
    "Int16": 2,
    "UInt8PerTensor": 1,
    "Int8": 1,
    "UInt8": 1,
    "Int4": 1,
    "UInt4": 1,
}


@dataclass(frozen=True, slots=True)
class TensorRef:
    ssa: str
    shape: tuple[int, ...]
    dtype: str
    device: str

    @property
    def elements(self) -> int:
        return math.prod(self.shape) if self.shape else 1

    @property
    def bytes(self) -> int:
        return self.elements * DTYPE_BYTES.get(self.dtype, 4)


@dataclass(frozen=True, slots=True)
class MllmOperator:
    index: int
    device: str
    op_type: str
    engine: Engine
    inputs: tuple[TensorRef, ...]
    outputs: tuple[TensorRef, ...]
    deps: tuple[int, ...]
    duration: int
    source_line: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "device": self.device,
            "op_type": self.op_type,
            "engine": self.engine.value,
            "inputs": [
                {"ssa": tensor.ssa, "shape": tensor.shape, "dtype": tensor.dtype, "bytes": tensor.bytes}
                for tensor in self.inputs
            ],
            "outputs": [
                {"ssa": tensor.ssa, "shape": tensor.shape, "dtype": tensor.dtype, "bytes": tensor.bytes}
                for tensor in self.outputs
            ],
            "deps": self.deps,
            "duration": self.duration,
            "source_line": self.source_line,
        }


def _tensor_refs(text: str) -> tuple[TensorRef, ...]:
    refs: list[TensorRef] = []
    for match in TENSOR_RE.finditer(text):
        dims = tuple(int(item.strip()) for item in match.group(2).split(",") if item.strip())
        refs.append(TensorRef(match.group(1), dims, match.group(3).strip(), match.group(4)))
    return tuple(refs)


def engine_for_op(op_type: str) -> Engine:
    if op_type in ME_OPS or "Attention" in op_type:
        return Engine.ME
    if op_type in DE_OPS:
        return Engine.DE
    return Engine.VE


def duration_for_op(engine: Engine, outputs: tuple[TensorRef, ...]) -> int:
    elements = sum(tensor.elements for tensor in outputs) or 1
    bytes_count = sum(tensor.bytes for tensor in outputs) or 1
    if engine is Engine.ME:
        return min(2048, max(16, math.ceil(elements / 16384)))
    if engine is Engine.VE:
        return min(512, max(4, math.ceil(elements / 32768)))
    return min(256, max(2, math.ceil(bytes_count / 65536)))


def parse_mir(path: Path, *, max_ops: int | None = None) -> tuple[MllmOperator, ...]:
    producers: dict[str, int] = {}
    operators: list[MllmOperator] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            op_match = OP_RE.search(line)
            if op_match is None:
                continue
            if max_ops is not None and len(operators) >= max_ops:
                break
            arrow = line.find("->", op_match.end())
            if arrow < 0:
                raise ValueError(f"malformed MIR operation at {path}:{line_number}")
            inputs = _tensor_refs(line[op_match.end() : arrow])
            outputs = _tensor_refs(line[arrow + 2 :])
            deps = tuple(sorted({producers[tensor.ssa] for tensor in inputs if tensor.ssa in producers}))
            engine = engine_for_op(op_match.group(2))
            operator = MllmOperator(
                index=len(operators),
                device=op_match.group(1),
                op_type=op_match.group(2),
                engine=engine,
                inputs=inputs,
                outputs=outputs,
                deps=deps,
                duration=duration_for_op(engine, outputs),
                source_line=line_number,
            )
            operators.append(operator)
            for tensor in outputs:
                producers[tensor.ssa] = operator.index
    return tuple(operators)


def _span(tensor: TensorRef, access: Access) -> MemorySpan:
    # SSA IDs are stable integers in mllm MIR. Reuse the address for in-place
    # views so TileMem detects real aliases across rewritten shapes.
    base = int(tensor.ssa) * 0x100000
    return MemorySpan(base, max(1, tensor.bytes), access, Scope.LOCAL, int(tensor.ssa) % 4)


def lower_to_tiles(
    operators: Iterable[MllmOperator],
    *,
    program_id: str = "mllm-program",
    call_id: str = "mllm-call",
    priority: Priority = Priority.NORMAL,
) -> tuple[Tile, ...]:
    ops = tuple(operators)
    tiles: list[Tile] = []
    for operator in ops:
        operands = tuple(_span(tensor, Access.READ) for tensor in operator.inputs)
        operands += tuple(_span(tensor, Access.WRITE) for tensor in operator.outputs)
        tiles.append(
            Tile(
                tile_id=f"mllm-op-{operator.index}",
                task_id=f"mllm-task-{operator.index // 8}",
                flow_id="mllm-flow",
                call_id=call_id,
                program_id=program_id,
                engine=operator.engine,
                duration=operator.duration,
                priority=priority,
                op_type=operator.op_type,
                sequence=operator.index,
                operands=operands,
                deps=tuple(f"mllm-op-{dep}" for dep in operator.deps),
                metadata={"static_group": operator.index, "mllm_source_line": operator.source_line},
            )
        )
    return tuple(tiles)


def operator_digest(operators: Iterable[MllmOperator]) -> str:
    payload = json.dumps([operator.to_dict() for operator in operators], sort_keys=True).encode()
    return hashlib.sha256(payload).hexdigest()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_head(path: Path) -> str:
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()


def run_mllm_backend(
    *,
    model_ops: int = 160,
    run_id: str = "run_005",
) -> dict[str, Any]:
    upstream_smoke = MLLM_ROOT / "tests/compile/ir/TraceFooNetTest.mir"
    upstream_model = MLLM_ROOT / "examples/qwen3_qnn_aot/qwen3_qnn_aot_1.7B.mir"
    fixture = PROJECT_ROOT / "integrations/mllm/fixtures/transformer_slice.mir"
    for path in (upstream_smoke, upstream_model, fixture):
        if not path.is_file():
            raise FileNotFoundError(path)

    smoke = parse_mir(upstream_smoke)
    model = parse_mir(upstream_model, max_ops=model_ops)
    model_repeat = parse_mir(upstream_model, max_ops=model_ops)
    slice_ops = parse_mir(fixture)
    slice_tiles = lower_to_tiles(slice_ops)
    simulator = TISASimulator(window=8, dispatch_latency=7)
    static = simulator.run(slice_tiles, TISAMode.STATIC)
    dynamic = simulator.run(slice_tiles, TISAMode.DYNAMIC)

    counts = {
        engine.value: sum(operator.engine is engine for operator in model)
        for engine in (Engine.ME, Engine.VE, Engine.DE)
    }
    model_tiles = lower_to_tiles(model)
    model_work = {
        engine.value: sum(tile.duration for tile in model_tiles if tile.engine is engine)
        for engine in (Engine.ME, Engine.VE, Engine.DE)
    }
    gates = {
        "smoke_four_linear_me": len(smoke) == 4
        and all(operator.op_type == "LinearOp" and operator.engine is Engine.ME for operator in smoke),
        "model_count": len(model) == model_ops,
        "model_all_engines": all(value > 0 for value in counts.values()),
        "deterministic": operator_digest(model) == operator_digest(model_repeat),
        "deps_precede": all(all(dep < operator.index for dep in operator.deps) for operator in model),
        "same_work": static.busy_cycles == dynamic.busy_cycles,
        "dynamic_overlap": sum(dynamic.overlap_cycles.values()) > 0,
        "dynamic_faster": dynamic.cycles < static.cycles,
    }
    return {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "native_mllm_mir_trace_to_agentsys_simulator_backend",
        "mllm": {
            "commit": _git_head(MLLM_ROOT),
            "smoke_path": str(upstream_smoke),
            "smoke_sha256": _sha256(upstream_smoke),
            "model_path": str(upstream_model),
            "model_sha256": _sha256(upstream_model),
        },
        "smoke": {"operators": len(smoke), "digest": operator_digest(smoke)},
        "model": {
            "selected_operators": len(model),
            "engine_counts": counts,
            "engine_work": model_work,
            "digest": operator_digest(model),
            "operators": [operator.to_dict() for operator in model],
        },
        "decoder_slice": {
            "source": str(fixture),
            "operators": [operator.to_dict() for operator in slice_ops],
            "static": static.to_dict(),
            "dynamic": dynamic.to_dict(),
            "speedup": static.cycles / dynamic.cycles,
        },
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "pass": all(gates.values()),
        },
    }


def write_operator_jsonl(operators: Iterable[MllmOperator], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for operator in operators:
            handle.write(json.dumps(operator.to_dict(), sort_keys=True) + "\n")

