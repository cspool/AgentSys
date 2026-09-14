#!/usr/bin/env python3
"""Per-model comparison report: three R10 timelines (end-to-end / high-latency /
concurrency-resource), each as a stacked pair — FCFS baseline above, agentix_core
below, full width. Interactive renderer adapted from the archives_final batch16
pages (section buttons, fold toggle, wheel zoom, drag pan, absolute-ns jump,
fitted trapezoid pile outlines, all members drawn — no sampling)."""
import argparse
import json
from pathlib import Path
from string import Template

JS = r"""
const NL = String.fromCharCode(10);
const NS = s => BigInt(s);
function relNs(abs, origin){ return Number(NS(abs) - NS(origin)); }
function fmtNs(n){
  const v = Number(n);
  if (Math.abs(v) >= 1e9) return (v/1e9).toFixed(3)+' s';
  if (Math.abs(v) >= 1e6) return (v/1e6).toFixed(2)+' ms';
  if (Math.abs(v) >= 1e3) return (v/1e3).toFixed(1)+' µs';
  return v.toFixed(0)+' ns';
}
const tip = document.getElementById('tip');
function showTip(ev, text){
  tip.textContent = text; tip.style.opacity = 1;
  let x = ev.clientX + 14, y = ev.clientY + 14;
  const r = tip.getBoundingClientRect();
  if (x + r.width > innerWidth) x = ev.clientX - r.width - 14;
  if (y + r.height > innerHeight) y = ev.clientY - r.height - 14;
  tip.style.left = x+'px'; tip.style.top = y+'px';
}
function hideTip(){ tip.style.opacity = 0; }
function makeMap(sec, breaks, folded){
  const lo = sec.lo, hi = sec.hi, pts = [];
  let t = lo, d = 0;
  if (folded) for (const br of breaks){
    const w = br.b - t;
    pts.push({t, d, k: 1}); d += w; t = br.b;
    pts.push({t, d, k: br.disp / Math.max(1, br.tru)});
    d += br.disp; t = br.e;
  }
  pts.push({t, d, k: 1}); d += hi - t;
  const total = d;
  function fwd(x){
    if (x <= lo) return 0;
    if (x >= hi) return total;
    let i = 0;
    while (i + 1 < pts.length && pts[i+1].t <= x) i++;
    return pts[i].d + (x - pts[i].t)*pts[i].k;
  }
  function inv(y){
    let i = 0;
    while (i + 1 < pts.length && pts[i+1].d <= y) i++;
    return pts[i].t + (y - pts[i].d)/(pts[i].k || 1e-9);
  }
  return {fwd, inv, total};
}
function mountBase(root, D, drawBody, rowCount, ROW){
  const st = {sec: 0, folded: true, zoom: 1, pan: 0};
  const svg = root.querySelector('svg');
  const LEFT = 250, RIGHT = 30, GAP = 12, TOP = 64;
  function cur(){
    const s = D.sections[st.sec];
    return {lo: relNs(s.begin_ns, D.origin), hi: relNs(s.end_ns, D.origin), meta: s};
  }
  function draw(){
    const s = cur();
    const brk = (D.breaks[st.sec]||[]).map(b => ({b: relNs(b.begin_ns, D.origin),
      e: relNs(b.end_ns, D.origin), tru: b.true_ns, disp: b.display_ns}));
    const map = makeMap(s, brk, st.folded);
    const W = svg.clientWidth || 1280, plotW = W - LEFT - RIGHT;
    const H = TOP + rowCount*(ROW+GAP) + 60;
    svg.setAttribute('viewBox', '0 0 '+W+' '+H);
    const X = t => LEFT + ((map.fwd(t)/map.total)*st.zoom + st.pan)*plotW;
    const out = ['<rect x="0" y="0" width="'+W+'" height="'+H+'" fill="#fff"/>'];
    for (let i = 0; i <= 10; i++){
      const disp = map.total*i/10, trueT = map.inv(disp);
      const x = LEFT + ((disp/map.total)*st.zoom + st.pan)*plotW;
      if (x < LEFT-1 || x > W-RIGHT+1) continue;
      out.push('<path d="M'+x.toFixed(1)+' '+(TOP-14)+' V'+(H-44)+'" stroke="#e6edf4"/>');
      out.push('<text x="'+x.toFixed(1)+'" y="'+(TOP-20)+'" font-size="11" text-anchor="middle" fill="#48607d">'+fmtNs(trueT - s.lo)+'</text>');
    }
    if (st.folded) for (const b of brk){
      const x = X(b.b), x2 = X(b.e);
      if (x2 < LEFT || x > W-RIGHT) continue;
      out.push('<rect class="brk" data-tru="'+b.tru+'" x="'+x.toFixed(1)+'" y="'+(TOP-14)+'" width="'+Math.max(1,x2-x).toFixed(1)+'" height="'+(H-44-(TOP-14))+'" fill="#f6f2e8"/>');
    }
    drawBody(out, {s, map, X, W, plotW, TOP, ROW, GAP, LEFT, RIGHT, H, st});
    out.push('<text x="10" y="'+(H-18)+'" font-size="11.5" fill="#48607d">段 '+s.meta.section+'/10 · 绝对区间 ['+s.meta.begin_ns+', '+s.meta.end_ns+') ns · '+(st.folded?'折叠（浅黄带为压缩空档）':'线性（时长严格成比例）')+' · 缩放 '+st.zoom.toFixed(1)+'×</text>');
    svg.innerHTML = out.join('');
    svg.querySelectorAll('.brk').forEach(el => {
      el.addEventListener('mousemove', ev => showTip(ev, '压缩空档 真实时长 '+fmtNs(+el.dataset.tru)));
      el.addEventListener('mouseleave', hideTip);
    });
    if (svg._post) svg._post(map, X, W, plotW);
  }
  root.querySelectorAll('.secbtn').forEach((b,i) => b.onclick = () => {
    st.sec = i; st.zoom = 1; st.pan = 0;
    root.querySelectorAll('.secbtn').forEach((x,k) => x.classList.toggle('on', k===i));
    draw();
  });
  const fbtn = root.querySelector('.fold');
  fbtn.onclick = () => { st.folded = !st.folded;
    fbtn.classList.toggle('on', st.folded);
    fbtn.textContent = st.folded ? '折叠：开' : '折叠：关'; draw(); };
  svg.addEventListener('wheel', ev => {
    ev.preventDefault();
    const rect = svg.getBoundingClientRect();
    const W = svg.clientWidth || 1280, plotW = W - LEFT - RIGHT;
    const at = ((ev.clientX - rect.left)*(W/rect.width) - LEFT)/plotW;
    const f = ev.deltaY < 0 ? 1.25 : 0.8;
    const nz = Math.min(4000, Math.max(1, st.zoom*f));
    st.pan = at - (at - st.pan)*(nz/st.zoom); st.zoom = nz;
    if (st.zoom === 1) st.pan = 0;
    draw();
  }, {passive:false});
  let drag = null;
  svg.addEventListener('mousedown', ev => drag = {x: ev.clientX, pan: st.pan});
  addEventListener('mouseup', () => drag = null);
  addEventListener('mousemove', ev => {
    if (!drag) return;
    const W = svg.clientWidth || 1280;
    st.pan = drag.pan + (ev.clientX - drag.x)/(W - LEFT - RIGHT);
    draw();
  });
  addEventListener('resize', draw);
  st.draw = draw;
  return st;
}
function mountPile(root, D){
  const st = mountBase(root, D, (out, ctx) => {
    const {X, W, TOP, ROW, GAP, LEFT, RIGHT, st} = ctx;
    D.piles.forEach((p, i) => {
      const y = TOP + i*(ROW+GAP);
      out.push('<text x="8" y="'+(y+15)+'" font-size="12">#'+p.rank+' '+p.type+'</text>');
      out.push('<text x="8" y="'+(y+30)+'" font-size="10.5" fill="#48607d">堆'+p.pile_index+' · '+p.count+'次 · 和 '+(p.sum_ns/1e9).toFixed(3)+'s · 单次 '+fmtNs(p.min_ns)+'–'+fmtNs(p.max_ns)+'</text>');
      const members = p.rows[st.sec] || [];
      if (!members.length){
        out.push('<text x="'+(LEFT+8)+'" y="'+(y+24)+'" font-size="10.5" fill="#8fa2b6">本段无该堆成员</text>');
        return;
      }
      const ms = members.slice().sort((a,b) => a[0]-b[0] || a[1]-b[1]);
      const n = ms.length, top = y + 6, bottom = y + ROW - 6;
      const frac = k => n === 1 ? 0.5 : k/(n-1);
      const ends = ms.map(m => [X(m[0]), Math.max(X(m[0]+m[1]), X(m[0])+0.6)]);
      let ls = 0, rs = 0;
      if (n > 1){
        ls = (ends[n-1][0]-ends[0][0])/(frac(n-1)-frac(0));
        rs = (ends[n-1][1]-ends[0][1])/(frac(n-1)-frac(0));
      }
      let li = Infinity, ri = -Infinity;
      for (let k = 0; k < n; k++){
        li = Math.min(li, ends[k][0] - ls*frac(k));
        ri = Math.max(ri, ends[k][1] - rs*frac(k));
      }
      li -= 4; ri += 4;
      out.push('<path d="M'+li.toFixed(1)+' '+top+' L'+ri.toFixed(1)+' '+top+' L'+(ri+rs).toFixed(1)+' '+bottom+' L'+(li+ls).toFixed(1)+' '+bottom+' Z" fill="#eef4fa" stroke="#8fb2ce"/>');
      const seg = [];
      for (let k = 0; k < n; k++){
        const yy = (top + frac(k)*(bottom-top)).toFixed(1);
        seg.push('M'+ends[k][0].toFixed(1)+' '+yy+'H'+ends[k][1].toFixed(1));
      }
      out.push('<path d="'+seg.join('')+'" stroke="'+(p.hl?'#b3462f':'#2f6f9f')+'" stroke-width="1" fill="none" opacity="0.8"/>');
      out.push('<rect class="hit" data-p="'+i+'" x="'+LEFT+'" y="'+y+'" width="'+(ctx.W-LEFT-RIGHT)+'" height="'+ROW+'" fill="transparent"/>');
    });
    ctx.st._hits = () => {
      root.querySelectorAll('.hit').forEach(el => {
        el.addEventListener('mousemove', ev => {
          const p = D.piles[+el.dataset.p];
          showTip(ev, '#'+p.rank+' '+p.type+' 堆'+p.pile_index+NL+'成员 '+p.count+' · 单次 '+fmtNs(p.min_ns)+' – '+fmtNs(p.max_ns)+NL+'堆总时长 '+(p.sum_ns/1e9).toFixed(4)+' s');
        });
        el.addEventListener('mouseleave', hideTip);
      });
    };
  }, D.piles.length, 96);
  root.querySelector('svg')._post = () => st._hits && st._hits();
  st.draw();
  return st;
}
function mountLanes(root, D){
  const LANE = 96;
  const st = mountBase(root, D, (out, ctx) => {
    const {X, W, TOP, LEFT, RIGHT, st} = ctx;
    const elig = (D.eligible_union[st.sec]||[]);
    D.lanes.forEach((ln, i) => {
      const y = TOP + i*(LANE+12), base = y + LANE - 8;
      out.push('<text x="8" y="'+(y+15)+'" font-size="12">'+ln.label+' ('+ln.unit+')</text>');
      out.push('<text x="8" y="'+(y+30)+'" font-size="10.5" fill="#48607d">'+ln.evidence+'</text>');
      out.push('<rect x="'+LEFT+'" y="'+y+'" width="'+(W-LEFT-RIGHT)+'" height="'+LANE+'" fill="#f2f2ef"/>');
      for (const w of elig){
        const x1 = X(w[0]), x2 = X(w[0]+w[1]);
        if (x2 < LEFT || x1 > W-RIGHT) continue;
        out.push('<rect x="'+Math.max(LEFT,x1).toFixed(1)+'" y="'+y+'" width="'+Math.max(0.5, Math.min(W-RIGHT,x2)-Math.max(LEFT,x1)).toFixed(1)+'" height="'+LANE+'" fill="#ffffff"/>');
      }
      const rows = ln.rows[st.sec]||[];
      let path = '';
      for (const r of rows){
        const x1 = X(r[0]), x2 = X(r[0]+r[1]);
        if (x2 < LEFT || x1 > W-RIGHT) continue;
        const h = (LANE-16)*Math.min(1, r[2]/ln.max);
        path += 'M'+x1.toFixed(1)+' '+base.toFixed(1)+' V'+(base-h).toFixed(1)+' H'+x2.toFixed(1)+' V'+base.toFixed(1);
      }
      out.push('<path d="'+path+'" stroke="'+ln.color+'" stroke-width="1" fill="none"/>');
      out.push('<rect class="lhit" data-l="'+i+'" x="'+LEFT+'" y="'+y+'" width="'+(W-LEFT-RIGHT)+'" height="'+LANE+'" fill="transparent"/>');
    });
    ctx.st._hits = (map) => {
      root.querySelectorAll('.lhit').forEach(el => {
        el.addEventListener('mousemove', ev => {
          const ln = D.lanes[+el.dataset.l];
          const rect = root.querySelector('svg').getBoundingClientRect();
          const W2 = root.querySelector('svg').clientWidth || 1280;
          const fracX = ((ev.clientX-rect.left)*(W2/rect.width) - 250)/(W2-250-30);
          const disp = (fracX - st.pan)/st.zoom * map.total;
          const t = map.inv(disp);
          const rows = ln.rows[st.sec]||[];
          let v = null;
          for (const r of rows) if (t >= r[0] && t < r[0]+r[1]) { v = r[2]; break; }
          showTip(ev, ln.label+NL+(v===null?'窗口外':v+' '+ln.unit)+NL+'灰底 = 未关联窗口（评审堆成员外）');
        });
        el.addEventListener('mouseleave', hideTip);
      });
    };
  }, D.lanes.length, 96);
  root.querySelector('svg')._post = (map) => st._hits && st._hits(map);
  st.draw();
  return st;
}
document.querySelectorAll('.panel').forEach(p => {
  const D = JSON.parse(document.getElementById(p.dataset.payload).textContent);
  if (p.dataset.kind === 'lanes') mountLanes(p, D); else mountPile(p, D);
});
"""

CSS = """
:root{--ink:#1f2f45;--line:#c9d6e4;--panel:#f2f7fb;--accent:#2f6f9f}
*{box-sizing:border-box}
body{margin:0;font:14px/1.6 "Noto Sans CJK SC","WenQuanYi Zen Hei",system-ui,sans-serif;color:var(--ink);background:#fff}
header{padding:18px 22px;border-bottom:1px solid var(--line);background:var(--panel)}
h1{margin:0 0 6px;font-size:21px}
h2{font-size:17px;margin:34px 22px 4px;color:var(--accent)}
.sub,.note{font-size:13px;color:#48607d}
.sub{max-width:120ch}
.note{margin:8px 22px 0;max-width:120ch}
.panel{margin:12px 22px 4px;border:1px solid var(--line);border-radius:6px;overflow:hidden}
.pbar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding:8px 12px;border-bottom:1px solid var(--line);background:#fbfdff}
.ptag{font-size:12.5px;font-weight:600;padding:2px 10px;border-radius:99px;border:1px solid var(--line)}
.ptag.core{border-color:var(--accent);color:var(--accent)}
button{font:13px inherit;padding:3px 9px;border:1px solid var(--line);background:#fff;border-radius:4px;cursor:pointer;color:var(--ink)}
button.on{background:var(--accent);border-color:var(--accent);color:#fff}
svg{display:block;width:100%;height:auto;background:#fff}
table{border-collapse:collapse;font-size:12.5px;margin:10px 22px;width:calc(100% - 44px)}
td,th{border:1px solid var(--line);padding:4px 8px;text-align:left}
th{background:var(--panel)}
#tip{position:fixed;pointer-events:none;background:#1f2f45;color:#fff;padding:6px 9px;border-radius:4px;font-size:12px;opacity:0;transition:opacity .1s;max-width:48ch;z-index:9;white-space:pre-line}
"""


def panel(pid, kind, tag, cls=""):
    btns = "".join(
        f'<button class="secbtn{" on" if i == 0 else ""}">段{i + 1}</button>' for i in range(10))
    return (f'<div class="panel" data-payload="{pid}" data-kind="{kind}">'
            f'<div class="pbar"><span class="ptag {cls}">{tag}</span>{btns}'
            f'<button class="fold on">折叠：开</button></div><svg height="400"></svg></div>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-key", required=True)
    ap.add_argument("--model-name", required=True)
    ap.add_argument("--fcfs-payload", type=Path, required=True)
    ap.add_argument("--core-payload", type=Path, required=True)
    ap.add_argument("--facts", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    pf = json.loads(a.fcfs_payload.read_text())
    pc = json.loads(a.core_payload.read_text())
    d = json.loads(a.facts.read_text())
    e, s, q, w, ml = d["endpoint"], d["endpoint"]["speedup"], d["queue"], d["class_wait_ms"], d["mlfq"]

    def emb(pid, obj):
        return f'<script id="{pid}" type="application/json">{json.dumps(obj)}</script>'

    wait_rows = "".join(
        f"<tr><td>{c}</td><td>{w['fcfs'][c]['mean']:.0f} / {w['fcfs'][c]['p90']:.0f}</td>"
        f"<td>{w['core'][c]['mean']:.0f} / {w['core'][c]['p90']:.0f}</td>"
        f"<td>{100*(1-w['core'][c]['mean']/w['fcfs'][c]['mean']):+.0f} %</td></tr>"
        for c in ("bfcl", "sharegpt", "lats"))
    hidden_f = ", ".join(f"#{r}" for r in pf["cu"]["hidden_ranks"]) or "无"
    hidden_c = ", ".join(f"#{r}" for r in pc["cu"]["hidden_ranks"]) or "无"

    html = Template("""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>$name · baseline vs agentix_core 时间线对照报告</title><style>$css</style></head><body>
<header><h1>$name · baseline (FCFS) vs agentix_core 时间线对照报告</h1>
<div class="sub">排队制 cap16 · r0.5 冻结负载 · 同 nsys 栈同参，唯一变量调度策略。
端侧：ptl mean $fm → $cm ms（<b>$sm×</b>），p90 $fp → $cp ms（<b>$sp×</b>），p99 $s99×。
三种时间线均为 Process 视角：每条横线是一个 Process 实例的真实起止；梯形外框只表成员归属，不表连续执行。
十段制 · 折叠模式压缩大空档（浅黄带，提示保留真实时长）· 滚轮缩放 · 拖拽平移。契约与实现参照
archives_final/batch16 R10 页（process-resource-contract.md）。</div></header>

<h2>① 端到端 Process 时间线（请求级宇宙：每个 LLM 调用一个实例，按类别分堆）</h2>
$e2e_f
$e2e_c
<p class="note"><b>对照读法：</b>两图同为 2,440 个调用实例、同一负载。baseline 中 bfcl/sharegpt 堆的成员线明显更长
（等待被计入调用窗口）；agentix_core 中这两类的重堆整体变短、lats 堆不变——这就是收益的请求级形态。
分类别等待（提交→首token，ms，mean/p90）：</p>
<table><tr><th>类别</th><th>FCFS</th><th>agentix_core</th><th>Δmean</th></tr>$wait_rows</table>

<h2>② 高延迟 Process 时间线（scope 宇宙：>10% 类型 × 5 堆对数时长聚类，全局排名）</h2>
$hl_f
$hl_c
<p class="note"><b>对照读法：</b>两图堆拓扑同构——同样的入选类型（forward/preprocess）、全局第 1 名都是重
forward 堆；agentix_core 侧重堆多出的质量（成员/时长增量）是量子切块 continuation 的机制签名。
尾延迟的机器侧形态（少数大 batch/prefill forward 步）不因策略改变；GPU 在做同样的事。
MLFQ 账本（core 调用记录）：入队 Q0–Q3 = $adm，降级 $demo 次，多量子调用 $multiq 个，β 提升 $promo 次。</p>

<h2>③ 并发 / 资源分析时间线（lanes 仅在已关联窗口内绘制；灰底 = 未关联）</h2>
$cu_f
$cu_c
<p class="note"><b>对照读法：</b>GPU busy 与 gemm 占比两侧几乎同形（资源墙不动，family 级 NCU 中位数
L2≈76% / SM≈49% / DRAM 14–20%）；差异在"在飞调用数"lane：baseline 长期贴顶（cap 上方累计 $qf s），
agentix_core 相同（$qc s）但队内成员不同——结合 ① 可见短程序先出队。隐藏堆保留排名：
baseline $hidden_f；core $hidden_c（preprocess 堆无 gemm 关联，按契约隐藏）。折叠上限 =
max(2×中位时长, 段宽/2000)——只压大空洞，微间隙保持线性，几何不失真（适配声明）。</p>

<p class="note">记账：全部成员绘制、未抽样；硬件关联 family 级非逐实例；trace 开销两侧同担；
payload 内含绝对 ns（BigInt 处理，无精度损失）。数字出处 gain_facts_$key.json 与两侧 payload。</p>
<div id="tip"></div>
$payloads
<script>$js</script></body></html>""").substitute(
        name=a.model_name, css=CSS, js=JS, key=a.model_key,
        fm=f"{e['fcfs']['ptl']['mean']:.1f}", cm=f"{e['core']['ptl']['mean']:.1f}",
        sm=f"{s['mean']:.2f}", fp=f"{e['fcfs']['ptl']['p90']:.1f}",
        cp=f"{e['core']['ptl']['p90']:.1f}", sp=f"{s['p90']:.2f}", s99=f"{s['p99']:.2f}",
        e2e_f=panel("pl-e2e-f", "pile", "FCFS baseline"),
        e2e_c=panel("pl-e2e-c", "pile", "agentix_core", "core"),
        hl_f=panel("pl-hl-f", "pile", "FCFS baseline"),
        hl_c=panel("pl-hl-c", "pile", "agentix_core", "core"),
        cu_f=panel("pl-cu-f", "lanes", "FCFS baseline"),
        cu_c=panel("pl-cu-c", "lanes", "agentix_core", "core"),
        wait_rows=wait_rows,
        adm="/".join(str(v) for v in ml["admission"].values()),
        demo=ml["demotions"], promo=ml["promotions"], multiq=ml["multi_quantum_calls"],
        qf=f"{q['fcfs']['ms_above_cap']/1e3:.1f}", qc=f"{q['core']['ms_above_cap']/1e3:.1f}",
        hidden_f=hidden_f, hidden_c=hidden_c,
        payloads="\n".join([emb("pl-e2e-f", pf["e2e"]), emb("pl-e2e-c", pc["e2e"]),
                            emb("pl-hl-f", pf["hl"]), emb("pl-hl-c", pc["hl"]),
                            emb("pl-cu-f", pf["cu"]), emb("pl-cu-c", pc["cu"])]))
    a.out.write_text(html)
    print("wrote", a.out, a.out.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
