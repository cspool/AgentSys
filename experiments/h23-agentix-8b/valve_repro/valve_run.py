"""Valve reproduction orchestrator: synchronises on ENGINE-SERVING events,
not on blind sleeps (the previous bash version let the offline finish before
the online even loaded its model)."""
import argparse, json, os, signal, subprocess, sys, time
from pathlib import Path

ROOT = Path('/workspace/AgentSys')
VR = ROOT / 'experiments/h23-agentix-8b/valve_repro'
PY = str(ROOT / '.venv-vllm/bin/python')
SWAP = str(ROOT / 'experiments/h23-agentix-8b/astra_repro/astra_swap.py')
WLD = ROOT / 'experiments/h23-agentix-8b/workloads'
Q17 = '/data3/docker_model/AgentSys/Qwen3-1.7B'
ON_FLAG = '/tmp/wf_online.json'
OFF_FLAG = '/tmp/wf_offline.json'
PAUSEF = '/tmp/valve_pause_offline'


def launch(side, workload, outdir, extra_env=None, flag=None):
    env = dict(os.environ)
    env.update({'CUDA_VISIBLE_DEVICES': ARGS.device,
                'VLLM_ENABLE_V1_MULTIPROCESSING': '0',
                'LD_LIBRARY_PATH': '/usr/local/cuda-12.8/lib64:' + env.get('LD_LIBRARY_PATH', '')})
    if flag:
        env.update({'AGENTIX_WALLFLAG': '1', 'AGENTIX_WALLFLAG_PATH': flag})
    stream = VR / f'{outdir}.stream.jsonl'
    if stream.exists():
        stream.unlink()
    env['AGENTIX_STREAM_CALLS'] = str(stream)
    if extra_env:
        env.update(extra_env)
    cmd = [PY, SWAP, '--workload', str(WLD / f'{workload}.json'),
           '--output-dir', str(VR / outdir), '--policy',
           'atlas' if side == 'on' else 'fcfs', '--enforce-eager',
           '--model-dir', Q17, '--gpu-memory-utilization', '0.40']
    log = open(VR / f'{outdir}.log', 'w')
    # start_new_session:自成进程组,终止时可整树杀掉
    # (否则 fork 出的 EngineCore 会成为孤儿,继续占用 ~9.6GB 显存 —— 2026-09-21 实测)
    return subprocess.Popen(cmd, env=env, stdout=log, stderr=subprocess.STDOUT,
                            cwd=str(ROOT), start_new_session=True)


def kill_tree(proc, timeout=40):
    """整进程组终止并等显存归还。"""
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except Exception:
        proc.kill()
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        pass
    # 等驱动回收(最多 60s)
    t0 = time.time()
    while time.time() - t0 < 60:
        try:
            out = subprocess.run(['nvidia-smi', '--query-gpu=memory.used',
                                  '--format=csv,noheader,nounits', '-i', ARGS.device],
                                 capture_output=True, text=True, timeout=10).stdout.strip()
            if int(out.splitlines()[0]) < 800:
                return True
        except Exception:
            pass
        time.sleep(2)
    return False


def wait_serving(flag, proc, timeout=180):
    """等引擎真正开始服务(wallflag 出现且 n_running>0 过一次)。"""
    t0 = time.time()
    while time.time() - t0 < timeout:
        if proc.poll() is not None:
            return False
        try:
            if json.load(open(flag)).get('n_running', 0) > 0:
                return True
        except Exception:
            pass
        time.sleep(0.2)
    return False


ap = argparse.ArgumentParser()
ap.add_argument('--arm', choices=['on_solo', 'off_solo', 'naive', 'channel', 'iter'],
                required=True)
ap.add_argument('--cool', type=float, default=0.074)
ap.add_argument('--device', default='1')
ARGS = ap.parse_args()
# 开跑前清理上一轮可能遗留的 EngineCore(vLLM 改了进程名,按名精确清)
subprocess.run(['pkill', '-9', '-x', 'VLLM::EngineCor'], capture_output=True)
time.sleep(3)
for f in (ON_FLAG, OFF_FLAG, PAUSEF):
    try: os.remove(f)
    except FileNotFoundError: pass

meta = {'arm': ARGS.arm, 'cool_s': ARGS.cool}
if ARGS.arm == 'on_solo':
    p = launch('on', 'pt_valve_online', f'v4_on_solo', flag=ON_FLAG)
    tw = subprocess.Popen([PY, str(VR / 'tcool_watch.py'), ON_FLAG, str(VR / 'v4_t_cool.json')])
    p.wait(); tw.terminate()
elif ARGS.arm == 'off_solo':
    p = launch('off', 'pt_valve_offline', 'v4_off_solo', flag=OFF_FLAG)
    time.sleep(200); kill_tree(p)
else:
    env = {'AGENTIX_PAUSE_FILE': PAUSEF} if ARGS.arm == 'iter' else None
    off = launch('off', 'pt_valve_offline', f'v4_off_{ARGS.arm}', extra_env=env, flag=OFF_FLAG)
    if not wait_serving(OFF_FLAG, off):
        sys.exit('offline 未进入服务')
    meta['offline_serving_at'] = time.time()
    on = launch('on', 'pt_valve_online', f'v4_on_{ARGS.arm}', flag=ON_FLAG)
    if not wait_serving(ON_FLAG, on):
        kill_tree(off); sys.exit('online 未进入服务')
    meta['online_serving_at'] = time.time()
    ctl = None
    if ARGS.arm == 'channel':
        ctl = subprocess.Popen([PY, str(VR / 'valve_ctl.py'), '--offline-pid', str(off.pid),
                                '--flag', ON_FLAG, '--cool', str(ARGS.cool),
                                '--online-pid', str(on.pid),
                                '--out', str(VR / f'v4_{ARGS.arm}_events.json')])
    elif ARGS.arm == 'iter':
        ctl = subprocess.Popen([PY, str(VR / 'iter_ctl.py'), ON_FLAG, PAUSEF,
                                str(ARGS.cool), str(VR / f'v4_{ARGS.arm}_events.json'),
                                str(on.pid)])
    on.wait()
    meta['online_done_at'] = time.time()
    if ctl: ctl.wait(timeout=30)
    kill_tree(off)
json.dump(meta, open(VR / f'v4_{ARGS.arm}_meta.json', 'w'), indent=1)
print(f"arm={ARGS.arm} done", json.dumps({k: v for k, v in meta.items() if k != 'arm'}))
