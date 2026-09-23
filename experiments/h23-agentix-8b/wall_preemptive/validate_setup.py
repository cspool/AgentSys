"""短跑设置验证:在投入长跑前,逐条检查对照是否成立。
任何一条不通过,长跑的数据都没有意义。"""
import json, os, sys, statistics

prefix = sys.argv[1] if len(sys.argv) > 1 else 'wc'
mode_name = {'wc': '时间片', 'wm': 'MPS'}.get(prefix, prefix)
ok = True


def chk(name, cond, detail=''):
    global ok
    ok &= bool(cond)
    print(f"  [{'✓' if cond else '✗'}] {name}" + (f"  — {detail}" if detail else ''))


print(f"=== {mode_name} 模式设置验证 ===")
try:
    ctrl = json.load(open(f'{prefix}_ctrl.json'))
except FileNotFoundError:
    print("  ✗ ctrl 缺失"); sys.exit(1)

# 1) 受害者两相是否真的处在不同资源态(基线时长应相近,否则不是同一 kernel 族)
bw = sorted(i['ms'] for i in ctrl['iters'] if i['ph'] == 'w')
bs = sorted(i['ms'] for i in ctrl['iters'] if i['ph'] == 's')
chk('两相 kernel 时长可比(同一 kernel 族)',
    abs(bw[len(bw)//2] - bs[len(bs)//2]) / bw[len(bw)//2] < 0.15,
    f"墙 {bw[len(bw)//2]:.1f}ms vs 饱和 {bs[len(bs)//2]:.1f}ms")

# 2) 基线噪声带:同相内的离散度必须远小于待测效应
# 配对分析的噪声底:未命中迭代相对其局部中位的离散度(而非全局 CV,
# 全局 CV 含热漂移,配对法已免疫之)
def paired_noise(it_list):
    res=[]
    for k in range(8, len(it_list)):
        prev=[j['ms'] for j in it_list[max(0,k-40):k] if j['ph']==it_list[k]['ph']][-8:]
        if len(prev)>=4: res.append(it_list[k]['ms']-statistics.median(prev))
    return statistics.pstdev(res) if len(res)>10 else float('inf')
pn = paired_noise(ctrl['iters'])
# 判据应是分辨力而非绝对噪声:标准误须远小于待测效应
import os as _os
_K = int(_os.environ.get('CHK_K', '40'))
_se = pn / max((_K/3) ** 0.5, 1)      # 饱和命中约占 1/3
chk('分辨力足够(标准误 < 1.2ms)', _se < 1.2,
    f"σ_paired={pn:.2f}ms, K={_K} → SE≈{_se:.2f}ms")

for mode in ('valve', 'wall_aware'):
    try:
        v = json.load(open(f'{prefix}_{mode}_victim.json'))
        c = json.load(open(f'{prefix}_{mode}_ctl.json'))
        b = json.load(open(f'{prefix}_{mode}_burst.json'))
    except FileNotFoundError as e:
        chk(f'{mode} 数据齐备', False, os.path.basename(e.filename)); continue
    # 3) 等量:两臂 K 与 burst 工作必须相同
    chk(f'{mode}: K 达标', b['k'] == c['k'], f"burst {b['k']} / ctl {c['k']}")
    # 4) 受害者必须活过整个控制器窗口
    ctl_span = c['events'][-1]['t'] if c['events'] else 0
    chk(f'{mode}: 受害者覆盖控制器全程',
        v['makespan_s'] > ctl_span + 5, f"victim {v['makespan_s']:.0f}s > ctl {ctl_span:.0f}s")
    # 5) 强发比例必须低(否则策略没被执行)
    chk(f'{mode}: 强发比例 <10%', c['forced'] / c['k'] < 0.1, f"{c['forced']}/{c['k']}")
    # 6) 每次抢占都要真打中受害者(扰动为正)
    tot = 0.0
    for ph in ('w', 's'):
        vs = sorted(i['ms'] for i in v['iters'] if i['ph'] == ph)
        bl = vs[int(len(vs)*0.40)]
        tot += sum(i['ms'] for i in v['iters'] if i['ph'] == ph) - len(vs)*bl
    chk(f'{mode}: 扰动为正(抢占确实生效)', tot > 0, f"总超出 {tot/1000:.2f}s")

# 7) 落点纯度必须分化,否则对照无区分力
try:
    cv_ = json.load(open(f'{prefix}_valve_ctl.json'))
    cw_ = json.load(open(f'{prefix}_wall_aware_ctl.json'))
    chk('落点纯度分化(墙感知 > Valve + 20%)',
        cw_['hit_wall'] - cv_['hit_wall'] >= 0.2 * cw_['k'],
        f"{cw_['hit_wall']}/{cw_['k']} vs {cv_['hit_wall']}/{cv_['k']}")
except FileNotFoundError:
    chk('落点纯度分化', False, '控制器数据缺')

# 8) MPS 模式专属:burst 必须真并发(时长接近 solo)
if prefix == 'wm':
    try:
        b = json.load(open(f'{prefix}_wall_aware_burst.json'))
        bm = sorted(x['busy_ms'] for x in b['bursts'])
        chk('MPS 生效:墙态 burst 接近 solo(<16ms)', bm[len(bm)//2] < 16,
            f"中位 {bm[len(bm)//2]:.1f}ms (solo 12ms)")
    except FileNotFoundError:
        pass

print(f"\n{'设置通过,可投入长跑' if ok else '设置有问题,长跑无意义 —— 先修'}")
sys.exit(0 if ok else 1)
