// smctrl_probe.cu -- libsmctrl 的 TPC mask 与 green context 的正面对比
//  同一 context 内两条普通 stream, 各设一个不相交的 TPC mask:
//   S1 分区是否绑定到不相交的物理 SM (%smid)
//   S2 是否真并发 (%globaltimer)
//   S3 换 mask 的代价 (对标 green context 预建池切换的 4.26us)
// 需要 MASK_OFF=288 (本机驱动 595.91.07 / CUDA 13.2, 2026-09-22 扫描所得)
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <set>
#include <algorithm>
#include <chrono>
#include <thread>
#include <cuda_runtime.h>
#include <libsmctrl.h>

#define RT(x) do{ cudaError_t e=(x); if(e!=cudaSuccess){ \
  fprintf(stderr,"[RT] %s:%d %s\n",__FILE__,__LINE__,cudaGetErrorString(e)); exit(1);} }while(0)

__global__ void probe_k(unsigned *smid, unsigned long long *t0,
                        unsigned long long *t1, unsigned long long ns)
{
    unsigned s; asm volatile("mov.u32 %0, %%smid;" : "=r"(s));
    unsigned long long a; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(a));
    if (threadIdx.x == 0) { smid[blockIdx.x] = s; t0[blockIdx.x] = a; }
    unsigned long long b = a;
    while (b - a < ns) { asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(b)); }
    if (threadIdx.x == 0) t1[blockIdx.x] = b;
}

struct Side { cudaStream_t st; int blocks; unsigned *ds;
              unsigned long long *da, *db;
              std::vector<unsigned> s; std::vector<unsigned long long> a, b; };

static void go(Side *x, unsigned long long ns) {
    probe_k<<<x->blocks, 128, 0, x->st>>>(x->ds, x->da, x->db, ns);
    cudaStreamSynchronize(x->st);
}

int main(int argc, char **argv)
{
    int tpcA = (argc > 1) ? atoi(argv[1]) : 48;    // A 拿前 48 个 TPC (96 SM)
    double ms = (argc > 2) ? atof(argv[2]) : 20.0;
    unsigned long long ns = (unsigned long long)(ms * 1e6);
    if (!getenv("MASK_OFF")) { fprintf(stderr, "请设置 MASK_OFF=288\n"); return 2; }

    int nsm = 0; cudaDeviceGetAttribute(&nsm, cudaDevAttrMultiProcessorCount, 0);
    uint32_t ntpc = 0;
    int rc = libsmctrl_get_tpc_info_cuda(&ntpc, 0);
    printf("SM=%d  libsmctrl 报 TPC=%u (rc=%d)\n", nsm, ntpc, rc);
    if (rc || !ntpc) ntpc = nsm / 2;
    if (tpcA >= (int)ntpc) tpcA = ntpc / 2;

    uint64_t maskA = ~0ull, maskB = ~0ull;
    for (int i = 0; i < tpcA; i++)        maskA &= ~(1ull << i);   // 清零=允许
    for (int i = tpcA; i < (int)ntpc; i++) maskB &= ~(1ull << i);
    printf("A 允许 TPC[0,%d) = %d 个 (%d SM);  B 允许 TPC[%d,%u) = %d 个 (%d SM)\n\n",
           tpcA, tpcA, tpcA*2, tpcA, ntpc, (int)ntpc-tpcA, ((int)ntpc-tpcA)*2);

    Side A{}, B{};
    A.blocks = tpcA * 2 * 4; B.blocks = ((int)ntpc - tpcA) * 2 * 4;
    for (Side *x : {&A, &B}) {
        RT(cudaStreamCreateWithFlags(&x->st, cudaStreamNonBlocking));
        RT(cudaMalloc(&x->ds, x->blocks*sizeof(unsigned)));
        RT(cudaMalloc(&x->da, x->blocks*sizeof(unsigned long long)));
        RT(cudaMalloc(&x->db, x->blocks*sizeof(unsigned long long)));
    }
    libsmctrl_set_stream_mask(A.st, maskA);
    libsmctrl_set_stream_mask(B.st, maskB);

    { std::thread t1(go,&A,1000000ull), t2(go,&B,1000000ull); t1.join(); t2.join(); }
    auto w0 = std::chrono::steady_clock::now();
    { std::thread t1(go,&A,ns), t2(go,&B,ns); t1.join(); t2.join(); }
    double wall = std::chrono::duration<double,std::milli>(
                      std::chrono::steady_clock::now()-w0).count();

    for (Side *x : {&A,&B}) {
        x->s.resize(x->blocks); x->a.resize(x->blocks); x->b.resize(x->blocks);
        RT(cudaMemcpy(x->s.data(), x->ds, x->blocks*sizeof(unsigned), cudaMemcpyDeviceToHost));
        RT(cudaMemcpy(x->a.data(), x->da, x->blocks*sizeof(unsigned long long), cudaMemcpyDeviceToHost));
        RT(cudaMemcpy(x->b.data(), x->db, x->blocks*sizeof(unsigned long long), cudaMemcpyDeviceToHost));
    }
    std::set<unsigned> sa(A.s.begin(),A.s.end()), sb(B.s.begin(),B.s.end());
    int inter=0; for(unsigned v:sa) if(sb.count(v)) inter++;
    unsigned long long a0=*std::min_element(A.a.begin(),A.a.end()), a1=*std::max_element(A.b.begin(),A.b.end());
    unsigned long long b0=*std::min_element(B.a.begin(),B.a.end()), b1=*std::max_element(B.b.begin(),B.b.end());
    double spanA=(a1-a0)/1e6, spanB=(b1-b0)/1e6;
    double ov=(double)((long long)std::min(a1,b1)-(long long)std::max(a0,b0))/1e6;
    double den=std::min(spanA,spanB);
    printf("[S1] A 实占 %zu 个物理 SM, B 实占 %zu 个, 交集 %d -> %s\n",
           sa.size(), sb.size(), inter, inter==0 ? "PASS 不相交" : "FAIL 重叠");
    printf("[S2] A %.2fms, B %.2fms, 重叠 %.2fms (%.1f%%), 墙钟 %.2fms -> %s\n",
           spanA, spanB, ov, den>0?ov/den*100:0, wall,
           (den>0 && ov/den>0.8) ? "PASS 真并发" : "FAIL 未并发");

    const int REP = 20000;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < REP; i++)
        libsmctrl_set_stream_mask(A.st, (i & 1) ? maskA : maskB);
    double us = std::chrono::duration<double,std::micro>(
                    std::chrono::steady_clock::now()-t0).count() / REP;
    libsmctrl_set_stream_mask(A.st, maskA);
    printf("[S3] 换 mask 代价 %.4f us/次  (green context 预建池切换 4.26us)\n", us);
    return 0;
}
