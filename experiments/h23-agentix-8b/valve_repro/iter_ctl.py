import json, os, sys, time
"""Iteration-gate controller (KernelPreempt/TGS proxy).
Liveness by online PID; stale flag = idle, not ended."""
flag, pausef, cool, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
online_pid = int(sys.argv[5]) if len(sys.argv) > 5 else 0
log, paused, idle_since, t0 = [], False, None, time.time()
def alive():
    return online_pid <= 0 or os.path.exists(f'/proc/{online_pid}')
def busy():
    try:
        if time.time() - os.path.getmtime(flag) > 0.5: return False
        return json.load(open(flag)).get('n_running', 0) > 0
    except Exception: return False
while alive():
    b = busy(); now = time.time()
    if b:
        idle_since = None
        if not paused:
            open(pausef, 'w').close(); paused = True
            log.append({'t': now-t0, 'ev': 'pause'})
    else:
        if idle_since is None: idle_since = now
        elif paused and now - idle_since >= cool:
            try: os.remove(pausef)
            except FileNotFoundError: pass
            paused = False
            log.append({'t': now-t0, 'ev': 'resume'})
    time.sleep(0.01)
if paused:
    try: os.remove(pausef)
    except FileNotFoundError: pass
json.dump({'events': log, 'preemptions': sum(1 for e in log if e['ev']=='pause')}, open(out,'w'))
print(f"iter_ctl: {sum(1 for e in log if e['ev']=='pause')} preemptions")
