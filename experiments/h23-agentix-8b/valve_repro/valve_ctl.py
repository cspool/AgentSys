"""Valve reproduction controller (declared proxy):
busy-triggered offline freeze (SIGSTOP) + cooldown wake (SIGCONT).

Online busy signal: online engine's wallflag file (n_running > 0).
T_cool per paper rule: ~2x max decode-iteration gap (we use --cool seconds).
Logs every transition for the rate metric."""
import argparse, json, os, signal, time

ap = argparse.ArgumentParser()
ap.add_argument('--offline-pid', type=int, required=True)
ap.add_argument('--flag', default='/tmp/agentix_wallflag_online.json')
ap.add_argument('--cool', type=float, default=1.0)
ap.add_argument('--online-pid', type=int, default=0)
ap.add_argument('--out', required=True)
a = ap.parse_args()

def online_alive():
    """在线是否还在运行 —— 用进程存活判定,不用 flag 陈旧度。
    flag 停更只代表引擎空闲(波与波之间),不代表结束(2026-09-21 实测缺陷)。"""
    if a.online_pid <= 0:
        return True
    return os.path.exists(f'/proc/{a.online_pid}')


def online_busy():
    try:
        # 陈旧 flag = 空闲(引擎无请求时不 step),不是结束
        if time.time() - os.path.getmtime(a.flag) > 0.5:
            return False
        return json.load(open(a.flag)).get('n_running', 0) > 0
    except Exception:
        return False

def stop_tree(sig):
    """对离线整进程组发信号。vLLM 的 EngineCore 是 fork 出的独立进程,
    只对父进程 SIGSTOP 完全无效(父进程只负责提交请求)。"""
    try:
        os.killpg(os.getpgid(a.offline_pid), sig)
    except Exception:
        try:
            os.kill(a.offline_pid, sig)
        except ProcessLookupError:
            pass


log = []
stopped = False
idle_since = None
t0 = time.time()
while online_alive():
    b = online_busy()
    now = time.time()
    if b:
        idle_since = None
        if not stopped:
            stop_tree(signal.SIGSTOP)
            stopped = True
            log.append({'t': now - t0, 'ev': 'stop'})
    else:
        if idle_since is None:
            idle_since = now
        elif stopped and now - idle_since >= a.cool:
            stop_tree(signal.SIGCONT)
            stopped = False
            log.append({'t': now - t0, 'ev': 'cont'})
    time.sleep(0.02)
if stopped:
    stop_tree(signal.SIGCONT)
    log.append({'t': time.time() - t0, 'ev': 'final_cont'})
json.dump({'events': log, 'preemptions': sum(1 for e in log if e['ev'] == 'stop')},
          open(a.out, 'w'))
print(f"controller: {sum(1 for e in log if e['ev']=='stop')} preemptions")
