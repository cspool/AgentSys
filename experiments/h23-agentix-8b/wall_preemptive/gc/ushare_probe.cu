// ushare_probe.cu -- 角度2 验证: blocksize shaping 能否让"资源亲和互补"的两个 kernel 共驻同一 SM
// 依据本地笔记 μShare (TJU, Non-Intrusive Kernel Co-Locating on NVIDIA GPUs):
//   half-plus shaping —— 把受害者 blocksize 设成略超半个 SM 的线程容量(4090: 1536/2+32=800),
//   使同 kernel 两个 block 无法共存于同一 SM -> 被迫散开 -> 每 SM 余 736 线程给另一个 kernel。
//   μShare 报: 6 种硬件单元平均利用率 10.90%->15.10%, 吞吐 +19.94%, 纯 LD_PRELOAD 零改码。
// 本探针在 4090 上扫 victim blockDim, 测:
//   每 SM 驻留的 victim block 数 / 抢占者能否挤进同一 SM / 两者并发时各自耗时
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <thread>
#include <chrono>
#include <cuda_runtime.h>

#define RT(x) do{ cudaError_t e=(x); if(e!=cudaSuccess){ \
  fprintf(stderr,"[RT] %s:%d %s\n",__FILE__,__LINE__,cudaGetErrorString(e)); exit(1);} }while(0)

// 受害者: DRAM 流式, 低算术强度 (对标 wall 相位)
__global__ void mem_k(const float* __restrict__ x, float* __restrict__ y, size_t n,
                      int reps, int inner, unsigned *smid, unsigned long long *t0,
                      unsigned long long *t1)
{
    unsigned s; asm volatile("mov.u32 %0, %%smid;" : "=r"(s));
    unsigned long long a; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(a));
    if (threadIdx.x == 0) { smid[blockIdx.x] = s; t0[blockIdx.x] = a; }
    size_t stride = (size_t)gridDim.x * blockDim.x;
    for (int r = 0; r < reps; r++)
        for (size_t i = (size_t)blockIdx.x * blockDim.x + threadIdx.x; i < n; i += stride) {
            float v = x[i];
            for (int k = 0; k < inner; k++) v = v * 1.000001f + 0.000001f;
            y[i] = v;
        }
    unsigned long long b; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(b));
    if (threadIdx.x == 0) t1[blockIdx.x] = b;
}

// 抢占者: 纯寄存器 FMA, 不碰内存 (对标 burst)
__global__ void cmp_k(float* __restrict__ z, int reps, unsigned *smid,
                      unsigned long long *t0, unsigned long long *t1)
{
    unsigned s; asm volatile("mov.u32 %0, %%smid;" : "=r"(s));
    unsigned long long a; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(a));
    if (threadIdx.x == 0) { smid[blockIdx.x] = s; t0[blockIdx.x] = a; }
    float v = z[blockIdx.x * blockDim.x + threadIdx.x];
    for (int r = 0; r < reps; r++) v = v * 1.000001f + 0.000001f;
    z[blockIdx.x * blockDim.x + threadIdx.x] = v;
    unsigned long long b; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(b));
    if (threadIdx.x == 0) t1[blockIdx.x] = b;
}

struct Rec { std::vector<unsigned> smid; std::vector<unsigned long long> t0, t1; };

static double span_ms(const Rec &r) {
    auto a = *std::min_element(r.t0.begin(), r.t0.end());
    auto b = *std::max_element(r.t1.begin(), r.t1.end());
    return (b - a) / 1e6;
}
static void fetch(Rec &r, unsigned *ds, unsigned long long *da, unsigned long long *db, int nb) {
    r.smid.resize(nb); r.t0.resize(nb); r.t1.resize(nb);
    RT(cudaMemcpy(r.smid.data(), ds, nb*sizeof(unsigned), cudaMemcpyDeviceToHost));
    RT(cudaMemcpy(r.t0.data(), da, nb*sizeof(unsigned long long), cudaMemcpyDeviceToHost));
    RT(cudaMemcpy(r.t1.data(), db, nb*sizeof(unsigned long long), cudaMemcpyDeviceToHost));
}

int main(int argc, char **argv)
{
    size_t N = 60ull * 1000 * 1000;
    int v_reps = (argc > 1) ? atoi(argv[1]) : 6;
    int v_inner = (argc > 2) ? atoi(argv[2]) : 8;
    int c_reps = (argc > 3) ? atoi(argv[3]) : 3000000;
    int v_mult = (argc > 4) ? atoi(argv[4]) : 1;
    cudaDeviceProp p; RT(cudaGetDeviceProperties(&p, 0));
    printf("%s SM=%d threads/SM=%d\n", p.name, p.multiProcessorCount, p.maxThreadsPerMultiProcessor);
    printf("受害者 = DRAM 流式(inner=%d), 抢占者 = 纯寄存器 FMA(128线程/块, 256块)\n", v_inner);
    printf("受害者 grid = %d SM x %d 块/SM, 无排队块\n\n", p.multiProcessorCount, v_mult);

    float *x, *y, *z;
    RT(cudaMalloc(&x, N*sizeof(float))); RT(cudaMalloc(&y, N*sizeof(float)));
    RT(cudaMalloc(&z, 256*1024*sizeof(float)));
    RT(cudaMemset(x, 1, N*sizeof(float))); RT(cudaMemset(z, 1, 256*1024*sizeof(float)));

    cudaStream_t sv, sc;
    RT(cudaStreamCreateWithFlags(&sv, cudaStreamNonBlocking));
    RT(cudaStreamCreateWithFlags(&sc, cudaStreamNonBlocking));

    const int C_BLK = 128, C_NB = 128 * 2;      // 抢占者: 小 block, 每 SM 想放 2 个
    unsigned *c_s; unsigned long long *c_a, *c_b;
    RT(cudaMalloc(&c_s, C_NB*sizeof(unsigned)));
    RT(cudaMalloc(&c_a, C_NB*sizeof(unsigned long long)));
    RT(cudaMalloc(&c_b, C_NB*sizeof(unsigned long long)));

    printf("%-10s %-8s %-11s %-11s %-9s %-9s %-11s %-9s\n",
           "v_block", "SM余线程", "v单独ms", "c单独ms", "v并发ms", "c并发ms", "真共驻SM", "合计ms");
    int blocks[] = {256, 320, 384, 448, 512};
    for (int bs : blocks) {
        if (bs > p.maxThreadsPerBlock) continue;
        // 受害者每 SM 恰好 1 个 block, 不留排队块(排队块会堵住 CWD, 掩盖 co-location)
        // 工作量由 grid-stride 循环按 N 决定, 与 grid 大小无关
        int v_nb = p.multiProcessorCount * v_mult;
        unsigned *v_s; unsigned long long *v_a, *v_b;
        RT(cudaMalloc(&v_s, v_nb*sizeof(unsigned)));
        RT(cudaMalloc(&v_a, v_nb*sizeof(unsigned long long)));
        RT(cudaMalloc(&v_b, v_nb*sizeof(unsigned long long)));

        auto launch_v = [&]{ mem_k<<<v_nb, bs, 0, sv>>>(x,y,N,v_reps,v_inner,v_s,v_a,v_b); };
        auto launch_c = [&]{ cmp_k<<<C_NB, C_BLK, 0, sc>>>(z,c_reps,c_s,c_a,c_b); };

        launch_v(); RT(cudaStreamSynchronize(sv));
        launch_c(); RT(cudaStreamSynchronize(sc));       // 预热

        launch_v(); RT(cudaStreamSynchronize(sv));
        Rec vs; fetch(vs, v_s, v_a, v_b, v_nb); double v_solo = span_ms(vs);
        launch_c(); RT(cudaStreamSynchronize(sc));
        Rec cs; fetch(cs, c_s, c_a, c_b, C_NB); double c_solo = span_ms(cs);

        // 受害者先发射并进入稳态, 再注入抢占者 —— 去掉发射竞态(这也是真实抢占的时序)
        { std::thread ta([&]{ launch_v(); cudaStreamSynchronize(sv); });
          std::this_thread::sleep_for(std::chrono::milliseconds(6));
          std::thread tb([&]{ launch_c(); cudaStreamSynchronize(sc); });
          ta.join(); tb.join(); }
        Rec vc, cc; fetch(vc, v_s, v_a, v_b, v_nb); fetch(cc, c_s, c_a, c_b, C_NB);

        // 按 SM 聚合区间, 求 (a) victim 同时驻留峰值 (b) 两 kernel 真共驻的 SM 数与时长
        std::map<unsigned, std::vector<std::pair<unsigned long long,unsigned long long>>> iv, ic;
        for (int i = 0; i < v_nb; i++) iv[vc.smid[i]].push_back({vc.t0[i], vc.t1[i]});
        for (int i = 0; i < C_NB; i++) ic[cc.smid[i]].push_back({cc.t0[i], cc.t1[i]});
        int peak_v = 0, cores = 0; double co_ms = 0;
        for (auto &kv : iv) {
            std::vector<std::pair<unsigned long long,int>> ev;
            for (auto &p2 : kv.second) { ev.push_back({p2.first,+1}); ev.push_back({p2.second,-1}); }
            std::sort(ev.begin(), ev.end());
            int cur = 0; for (auto &e : ev) { cur += e.second; peak_v = std::max(peak_v, cur); }
            if (!ic.count(kv.first)) continue;
            double best = 0;
            for (auto &p2 : kv.second) for (auto &q : ic[kv.first]) {
                long long o = (long long)std::min(p2.second,q.second) - (long long)std::max(p2.first,q.first);
                if (o > 0) best = std::max(best, o/1e6);
            }
            if (best > 0) { cores++; co_ms += best; }
        }
        double vcc = span_ms(vc), ccc = span_ms(cc);
        auto lo = std::min(*std::min_element(vc.t0.begin(),vc.t0.end()),
                           *std::min_element(cc.t0.begin(),cc.t0.end()));
        auto hi = std::max(*std::max_element(vc.t1.begin(),vc.t1.end()),
                           *std::max_element(cc.t1.begin(),cc.t1.end()));
        printf("%-10d %-8d %-11.1f %-11.1f %-9.1f %-9.1f %-11d %-9.1f  (v峰值驻留 %d 块/SM = %d 线程, 共驻时长中位 %.1fms)\n",
               bs, p.maxThreadsPerMultiProcessor - bs*v_mult, v_solo, c_solo, vcc, ccc, cores, (hi-lo)/1e6,
               peak_v, std::min(peak_v*bs, p.maxThreadsPerMultiProcessor), cores ? co_ms/cores : 0.0);
        cudaFree(v_s); cudaFree(v_a); cudaFree(v_b);
    }
    printf("\n串行基线 = v单独 + c单独;  合计ms < 串行基线 说明共驻真的省了时间\n");
    return 0;
}
