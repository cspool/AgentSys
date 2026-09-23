"""窗口内趋势分析: MPK 的上下文在一次生成里从 prompt 长度涨到 max_seq_length,
受害者因此从"偏算力"漂移到"偏 DRAM"。看抢占者的速率随之怎么变。
正交性假设预测: TC 轴抢占者的斜率为正(受害者越 DRAM 越让出算力),
                DRAM 轴抢占者的斜率为负(争同一条带宽)。符号必须翻转。
"""
import json, statistics, sys

def load(path, solo_rate):
    d = json.load(open(path)); b = d['buckets']
    return d, b, solo_rate

def contended_window(b, solo_rate, thresh=0.6):
    """受害者在场的区间 = 速率掉到 solo 的 thresh 以下的连续段"""
    idx = [i for i, x in enumerate(b) if x['rate'] < thresh * solo_rate]
    if not idx: return None
    return idx[0], idx[-1]

def trend(b, lo, hi):
    """对受害者在场区间做最小二乘斜率(每秒的相对变化)"""
    xs = [b[i]['t'] for i in range(lo, hi + 1)]
    ys = [b[i]['rate'] for i in range(lo, hi + 1)]
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    num = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    den = sum((x-mx)**2 for x in xs) or 1.0
    slope = num/den
    return dict(n=n, t0=round(xs[0],1), t1=round(xs[-1],1),
                first=round(ys[0],1), last=round(ys[-1],1),
                median=round(statistics.median(ys),1),
                slope_per_s=round(slope,2),
                rel_slope_pct_per_s=round(100*slope/my, 3),
                total_change_pct=round(100*(ys[-1]-ys[0])/ys[0], 2))

if __name__ == '__main__':
    cases = [('TC 轴', 'out/corun_vs_mpk_mps.json', 27286.6),
             ('DRAM 轴', 'out/corun_vs_mpk_dram.json', 6527.4)]
    print(f"{'抢占者':<9}{'共驻区间':>14}{'起':>9}{'末':>9}{'中位':>9}{'G_p':>7}{'区间内变化':>11}{'斜率%/s':>10}")
    out={}
    for name, path, solo in cases:
        try: d, b, s = load(path, solo)
        except FileNotFoundError: print(f"{name:<9}  (未完成)"); continue
        w = contended_window(b, s)
        if not w: print(f"{name:<9}  未检出共驻区间"); continue
        t = trend(b, *w)
        gp = t['median']/s
        print(f"{name:<9}{f'{t[chr(116)+chr(48)]}-{t[chr(116)+chr(49)]}s':>14}{t['first']:>9}{t['last']:>9}"
              f"{t['median']:>9}{gp:>7.3f}{t['total_change_pct']:>10.2f}%{t['rel_slope_pct_per_s']:>10}")
        out[name]=dict(**t, G_p=round(gp,4), solo=s)
    json.dump(out, open('out/TREND.json','w'), ensure_ascii=False, indent=1)
