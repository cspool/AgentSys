#!/usr/bin/env python3
"""Mixed-modality agent-loop serving: VisLM + LM + AudioLM on local engines.

Programs are call DAGs (same schema as pt_agentloop2 + per-call "modality").
Scheduling is per-call DAG (a call waits only on its parents) — the v3 prog
layer's parallel_dag_not_serialized gate applies.

Engines (all local, /data3/docker_model/AgentSys):
  lm    Qwen3-1.7B                 text reasoning / decision roles
  vis   Qwen2.5-VL-3B-Instruct     image understanding roles
  audio Qwen2-Audio-7B-Instruct    audio understanding roles

Assets are synthetic and generated on the fly (noise images, sine wavs):
content is irrelevant to serving cost; sizes are what matters and are
declared per call (image_hw, audio_s).
"""
import argparse
import asyncio
import collections
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

MODELS = {   # 全部 1.xB,三引擎同驻一张 24G 卡
    'lm': '/data3/docker_model/AgentSys/Qwen3-1.7B',
    'vis': '/data3/docker_model/AgentSys/InternVL2_5-1B',
    'audio': '/data3/docker_model/AgentSys/ultravox-v0_5-llama-3_2-1b',
}


def synth_image(hw, seed):
    from PIL import Image
    rng = np.random.default_rng(seed)
    return Image.fromarray(rng.integers(0, 255, (hw[0], hw[1], 3), dtype=np.uint8))


def synth_audio(seconds, seed, sr=16000):
    rng = np.random.default_rng(seed)
    t = np.linspace(0, seconds, int(sr * seconds), dtype=np.float32)
    f = 200 + 40 * (seed % 7)
    return (0.2 * np.sin(2 * np.pi * f * t)
            + 0.05 * rng.standard_normal(t.shape).astype(np.float32)), sr


def build_prompt(call, prog, filler='分析 '):
    # deterministic filler to the declared prompt budget; modality attachments
    # carry their own encoder cost on top.
    n = max(call['prompt_tokens'] - 32, 8)
    return (f"[{prog['program_id']}#{call['index']} {call.get('role','')}] "
            + filler * n)


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--workload', type=Path, required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--engines', default='lm,vis,audio',
                    help='comma list; audio 可去掉以便双模态先行')
    ap.add_argument('--devices', default='lm:1,vis:1,audio:1',
                    help='modality:gpu 映射;默认三引擎同驻一张卡(ModServe 论证的单体形态)')
    ap.add_argument('--gpu-frac', default='lm:0.20,vis:0.16,audio:0.24')
    ap.add_argument('--max-model-len', type=int, default=4096)
    ap.add_argument('--enforce-eager', action='store_true')
    args = ap.parse_args()

    os.environ.setdefault('VLLM_ENABLE_V1_MULTIPROCESSING', '0')
    # 步级 NVTX 探针必须在引擎构建前安装(fork 传播到三个 EngineCore 子进程)
    if os.environ.get('AGENTIX_W_INSTRUMENT', '0') == '1':
        sys.path.insert(0, str(Path(__file__).parent))
        import w_instrument
        w_instrument.install()
    from vllm import AsyncLLMEngine, SamplingParams
    from vllm.engine.arg_utils import AsyncEngineArgs

    wl = json.loads(args.workload.read_text())
    wanted = args.engines.split(',')
    dev = dict(kv.split(':') for kv in args.devices.split(','))
    frac = {k: float(v) for k, v in (kv.split(':') for kv in args.gpu_frac.split(','))}

    ncu_target = os.environ.get('AGENTIX_NCU_TARGET', '')
    if ncu_target:
        print(f'[mm] NCU target={ncu_target}, installing gate', flush=True)
        # NCU 门控是按进程的:在 fork 前打补丁,fork 时 env 决定哪个子进程自触发
        # w_instrument 的经验:AsyncLLM 路径不走 EngineCore.step,
        # 已验证的调用点是 EngineCoreProc._process_engine_step
        from vllm.v1.engine import core as _core
        _orig_pes = _core.EngineCoreProc._process_engine_step

        def _gated_pes(self, *a, **k):
            if (os.environ.get('AGENTIX_SELF_TRIGGER') == '1'
                    and not getattr(self, '_ncu_trig', False)):
                sched = getattr(self, 'scheduler', None)
                if sched is not None and getattr(sched, 'running', None):
                    import torch
                    torch.cuda.profiler.start()
                    self._ncu_trig = True
                    print('[mm] engine-side cudaProfilerStart', flush=True)
            return _orig_pes(self, *a, **k)
        _core.EngineCoreProc._process_engine_step = _gated_pes

    # SpaceServe 式分区(近似):MPS 每客户端 SM 百分比帽,fork 时按引擎生效
    mps_shares = {}
    if os.environ.get('AGENTIX_MPS_SHARES'):
        mps_shares = dict(kv.split(':') for kv in
                          os.environ['AGENTIX_MPS_SHARES'].split(','))
    engines: dict[str, Any] = {}
    for m in wanted:
        os.environ['CUDA_VISIBLE_DEVICES'] = dev[m]
        if ncu_target:
            os.environ['AGENTIX_SELF_TRIGGER'] = '1' if m == ncu_target else '0'
        if m in mps_shares:
            os.environ['CUDA_MPS_ACTIVE_THREAD_PERCENTAGE'] = mps_shares[m]
        else:
            os.environ.pop('CUDA_MPS_ACTIVE_THREAD_PERCENTAGE', None)
        ea = AsyncEngineArgs(
            model=MODELS[m], dtype='bfloat16', max_model_len=args.max_model_len,
            gpu_memory_utilization=frac[m], enforce_eager=args.enforce_eager,
            disable_log_stats=True, seed=0,
            trust_remote_code=(m in ('vis', 'audio')),  # InternVL 与 ultravox 都需要
            limit_mm_per_prompt={'image': 1} if m == 'vis'
                else ({'audio': 1} if m == 'audio' else None))
        engines[m] = AsyncLLMEngine.from_engine_args(ea)
        print(f'[mm] engine {m} up on GPU{dev[m]}', flush=True)

    t0 = time.monotonic_ns()
    rows = []
    inflight = collections.Counter()
    trig = {'armed': os.environ.get('AGENTIX_MM_TRIGGER', '0') == '1',
            'fired': False, 'since': None}

    def trig_check():
        # 引擎均已 fork,此刻父进程初始化 CUDA 不再毒化 fork
        if not trig['armed'] or trig['fired']:
            return
        n = sum(1 for v in inflight.values() if v > 0)
        now = time.monotonic_ns()
        if n >= 2:
            if trig['since'] is None:
                trig['since'] = now
            elif now - trig['since'] >= 1e9:
                import torch
                torch.cuda.profiler.start()
                trig['fired'] = True
                print('[mm] cudaProfilerStart(>=2 modalities in flight 1s)', flush=True)
        else:
            trig['since'] = None

    async def run_call(prog, call):
        m = call.get('modality', 'lm')
        prompt = build_prompt(call, prog)
        # vLLM 要求 prompt 含模型的模态占位符
        if m == 'vis':
            prompt = '<image>\n' + prompt
        elif m == 'audio':
            prompt = '<|audio|>\n' + prompt
        mm = {}
        seed = hash((prog['program_id'], call['index'])) & 0xffff
        if m == 'vis':
            mm = {'image': synth_image(call.get('image_hw', [448, 448]), seed)}
        elif m == 'audio':
            mm = {'audio': synth_audio(call.get('audio_s', 4.0), seed)}
        sp = SamplingParams(max_tokens=call['output_tokens'], temperature=0.0,
                            ignore_eos=True)
        req = {'prompt': prompt}
        if mm:
            req['multi_modal_data'] = mm
        inflight[m] += 1
        trig_check()
        sub = time.monotonic_ns()
        first = None
        gen = engines[m].generate(req, sp, request_id=f"{prog['program_id']}-{call['index']}")
        n_out = 0
        async for out in gen:
            if first is None and out.outputs and out.outputs[0].token_ids:
                first = time.monotonic_ns()
            n_out = len(out.outputs[0].token_ids) if out.outputs else n_out
        fin = time.monotonic_ns()
        inflight[m] -= 1
        rows.append({'program_id': prog['program_id'], 'call_index': call['index'],
                     'wave': call.get('wave', call['index']), 'modality': m,
                     'parents': call.get('parents', []),
                     'submitted_rel_ms': (sub - t0) / 1e6,
                     'first_token_rel_ms': ((first or fin) - t0) / 1e6,
                     'finished_rel_ms': (fin - t0) / 1e6,
                     'call_latency_ms': (fin - sub) / 1e6,
                     'ttft_ms': ((first or fin) - sub) / 1e6,
                     'prompt_tokens': call['prompt_tokens'],
                     'output_tokens': n_out, 'produced_tokens': n_out,
                     'role': call.get('role', '')})
        return fin

    async def run_program(prog):
        arr = t0 + prog['arrival_ns']
        now = time.monotonic_ns()
        if arr > now:
            await asyncio.sleep((arr - now) / 1e9)
        done = {c['index']: asyncio.Event() for c in prog['llm_calls']}
        fin_of = {}

        async def one(c):
            for i in c.get('parents', []):
                await done[i].wait()
            delay = c.get('tool_delay_ns', 0) / 1e9
            if delay:
                await asyncio.sleep(delay)
            fin_of[c['index']] = await run_call(prog, c)
            done[c['index']].set()

        await asyncio.gather(*(one(c) for c in prog['llm_calls']))

    await asyncio.gather(*(run_program(p) for p in wl['programs']))
    if trig.get('fired'):
        import torch
        torch.cuda.profiler.stop()
    wall = (time.monotonic_ns() - t0) / 1e9
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'calls_mm.jsonl').write_text(
        ''.join(json.dumps(r, sort_keys=True) + '\n' for r in rows))
    summ = {'wall_s': wall,
            'throughput_tokens_per_s': sum(r['produced_tokens'] for r in rows) / wall,
            'calls': len(rows),
            'by_modality': {m: sum(1 for r in rows if r['modality'] == m)
                            for m in ('lm', 'vis', 'audio')}}
    (args.output_dir / 'summary_mm.json').write_text(json.dumps(summ, indent=1) + '\n')
    print(json.dumps(summ, indent=1), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(asyncio.run(main()))
