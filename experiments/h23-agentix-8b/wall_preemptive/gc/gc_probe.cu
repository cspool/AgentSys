// gc_probe.cu -- 验证 CUDA Green Context 能否在 RTX 4090 (Ada, cc8.9) 上替代 MPS
// 作为 wall_preemptive 的空间共享基底。
//
// 验证四件事:
//   V1 分区是否成功建立, 每个 green ctx 实际拿到几个 SM
//   V2 分区是否真的绑定到不相交的物理 SM (读 %smid)
//   V3 两个 green ctx 的 kernel 是否真并发 (读 %globaltimer 求区间交集)
//   V4 重分区代价 (建/销毁 green ctx 的耗时)
//
// 用法: ./gc_probe [unit_sm=16] [k_groups_for_A=6] [spin_ms=20]
//   unit_sm : cuDevSmResourceSplitByCount 的 minCount, Ada 要求 >=4 且为 2 的倍数
//   k       : 前 k 个 group 归 A(victim), 其余归 B(preemptor)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <set>
#include <thread>
#include <chrono>
#include <cuda.h>
#include <cuda_runtime.h>

#define DRV(x) do{ CUresult _r=(x); if(_r!=CUDA_SUCCESS){ const char*_s=0; cuGetErrorString(_r,&_s); \
  fprintf(stderr,"[DRV FAIL] %s:%d %s -> %d (%s)\n",__FILE__,__LINE__,#x,(int)_r,_s?_s:"?"); exit(1);} }while(0)
#define RT(x) do{ cudaError_t _e=(x); if(_e!=cudaSuccess){ \
  fprintf(stderr,"[RT FAIL] %s:%d %s -> %s\n",__FILE__,__LINE__,#x,cudaGetErrorString(_e)); exit(1);} }while(0)

__global__ void probe_k(unsigned *smid, unsigned long long *t0,
                        unsigned long long *t1, unsigned long long spin_ns)
{
    unsigned s; asm volatile("mov.u32 %0, %%smid;" : "=r"(s));
    unsigned long long a; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(a));
    if (threadIdx.x == 0) { smid[blockIdx.x] = s; t0[blockIdx.x] = a; }
    unsigned long long b = a;
    while (b - a < spin_ns) { asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(b)); }
    if (threadIdx.x == 0) t1[blockIdx.x] = b;
}

struct Arm {
    const char   *name;
    CUgreenCtx    gctx;
    CUcontext     ctx;
    CUstream      stream;
    unsigned      sm_provisioned;
    int           blocks;
    unsigned           *d_smid;
    unsigned long long *d_t0, *d_t1;
    std::vector<unsigned>           smid;
    std::vector<unsigned long long> t0, t1;
};

static void run_arm(Arm *a, unsigned long long spin_ns)
{
    DRV(cuCtxSetCurrent(a->ctx));
    probe_k<<<a->blocks, 256, 0, (cudaStream_t)a->stream>>>(a->d_smid, a->d_t0, a->d_t1, spin_ns);
    RT(cudaGetLastError());
    DRV(cuStreamSynchronize(a->stream));
}

int main(int argc, char **argv)
{
    unsigned unit    = (argc > 1) ? (unsigned)atoi(argv[1]) : 16u;
    unsigned k_for_A = (argc > 2) ? (unsigned)atoi(argv[2]) : 6u;
    double   spin_ms = (argc > 3) ? atof(argv[3]) : 20.0;
    unsigned long long spin_ns = (unsigned long long)(spin_ms * 1e6);

    DRV(cuInit(0));
    CUdevice dev; DRV(cuDeviceGet(&dev, 0));
    char devname[256]; DRV(cuDeviceGetName(devname, sizeof devname, dev));
    int cc_major = 0, cc_minor = 0, nsm = 0;
    DRV(cuDeviceGetAttribute(&cc_major, CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MAJOR, dev));
    DRV(cuDeviceGetAttribute(&cc_minor, CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MINOR, dev));
    DRV(cuDeviceGetAttribute(&nsm, CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT, dev));
    printf("device : %s  cc%d.%d  SM=%d\n", devname, cc_major, cc_minor, nsm);
    printf("split  : unit=%u  k_for_A=%u  spin=%.1fms\n\n", unit, k_for_A, spin_ms);

    CUcontext primary; DRV(cuDevicePrimaryCtxRetain(&primary, dev));
    DRV(cuCtxSetCurrent(primary));

    // ---- V1: 切分 SM ----
    CUdevResource whole;
    DRV(cuDeviceGetDevResource(dev, &whole, CU_DEV_RESOURCE_TYPE_SM));
    printf("[V1] 整卡资源 smCount=%u\n", whole.sm.smCount);

    unsigned ngroups = 0;
    DRV(cuDevSmResourceSplitByCount(NULL, &ngroups, &whole, NULL, 0, unit));
    printf("[V1] minCount=%u 时可切出 %u 个 group\n", unit, ngroups);
    if (ngroups < 2) { fprintf(stderr, "[V1] group 数 <2, 换更小的 unit\n"); return 2; }
    if (k_for_A >= ngroups) k_for_A = ngroups - 1;

    std::vector<CUdevResource> groups(ngroups);
    CUdevResource remaining; memset(&remaining, 0, sizeof remaining);
    DRV(cuDevSmResourceSplitByCount(groups.data(), &ngroups, &whole, &remaining, 0, unit));
    for (unsigned i = 0; i < ngroups; i++)
        printf("       group[%u].smCount=%u\n", i, groups[i].sm.smCount);
    if (remaining.type == CU_DEV_RESOURCE_TYPE_SM)
        printf("       remaining.smCount=%u\n", remaining.sm.smCount);

    // A = group[0..k-1], B = group[k..n-1]
    CUdevResourceDesc descA, descB;
    DRV(cuDevResourceGenerateDesc(&descA, groups.data(), k_for_A));
    DRV(cuDevResourceGenerateDesc(&descB, groups.data() + k_for_A, ngroups - k_for_A));

    Arm A{}, B{};
    A.name = "A(victim)";  B.name = "B(preemptor)";
    DRV(cuGreenCtxCreate(&A.gctx, descA, dev, CU_GREEN_CTX_DEFAULT_STREAM));
    DRV(cuGreenCtxCreate(&B.gctx, descB, dev, CU_GREEN_CTX_DEFAULT_STREAM));
    DRV(cuCtxFromGreenCtx(&A.ctx, A.gctx));
    DRV(cuCtxFromGreenCtx(&B.ctx, B.gctx));
    DRV(cuGreenCtxStreamCreate(&A.stream, A.gctx, CU_STREAM_NON_BLOCKING, 0));
    DRV(cuGreenCtxStreamCreate(&B.stream, B.gctx, CU_STREAM_NON_BLOCKING, 0));

    CUdevResource ra, rb;
    DRV(cuGreenCtxGetDevResource(A.gctx, &ra, CU_DEV_RESOURCE_TYPE_SM));
    DRV(cuGreenCtxGetDevResource(B.gctx, &rb, CU_DEV_RESOURCE_TYPE_SM));
    A.sm_provisioned = ra.sm.smCount;
    B.sm_provisioned = rb.sm.smCount;
    printf("\n[V1] green ctx A 分到 %u SM,  B 分到 %u SM,  合计 %u / %d\n",
           A.sm_provisioned, B.sm_provisioned, A.sm_provisioned + B.sm_provisioned, nsm);

    // ---- 缓冲区在 primary ctx 下分配, green ctx 共享同一地址空间 ----
    DRV(cuCtxSetCurrent(primary));
    for (Arm *a : {&A, &B}) {
        a->blocks = (int)a->sm_provisioned * 4;
        RT(cudaMalloc(&a->d_smid, a->blocks * sizeof(unsigned)));
        RT(cudaMalloc(&a->d_t0,   a->blocks * sizeof(unsigned long long)));
        RT(cudaMalloc(&a->d_t1,   a->blocks * sizeof(unsigned long long)));
        RT(cudaMemset(a->d_smid, 0xff, a->blocks * sizeof(unsigned)));
    }

    // 预热, 排除 module load 与首次 launch 开销
    { std::thread ta(run_arm, &A, 1000000ULL), tb(run_arm, &B, 1000000ULL); ta.join(); tb.join(); }

    // ---- V2 + V3: 同时发射, 读 smid 与 globaltimer ----
    auto wall0 = std::chrono::steady_clock::now();
    { std::thread ta(run_arm, &A, spin_ns), tb(run_arm, &B, spin_ns); ta.join(); tb.join(); }
    double wall_ms = std::chrono::duration<double, std::milli>(
                         std::chrono::steady_clock::now() - wall0).count();

    DRV(cuCtxSetCurrent(primary));
    for (Arm *a : {&A, &B}) {
        a->smid.resize(a->blocks); a->t0.resize(a->blocks); a->t1.resize(a->blocks);
        RT(cudaMemcpy(a->smid.data(), a->d_smid, a->blocks * sizeof(unsigned), cudaMemcpyDeviceToHost));
        RT(cudaMemcpy(a->t0.data(),   a->d_t0,   a->blocks * sizeof(unsigned long long), cudaMemcpyDeviceToHost));
        RT(cudaMemcpy(a->t1.data(),   a->d_t1,   a->blocks * sizeof(unsigned long long), cudaMemcpyDeviceToHost));
    }

    std::set<unsigned> sa(A.smid.begin(), A.smid.end()), sb(B.smid.begin(), B.smid.end());
    std::vector<unsigned> inter;
    for (unsigned s : sa) if (sb.count(s)) inter.push_back(s);
    printf("\n[V2] A 实际占用 %zu 个物理 SM, B 实际占用 %zu 个, 交集 %zu 个\n",
           sa.size(), sb.size(), inter.size());
    printf("[V2] 判定: %s\n", inter.empty()
           ? "PASS 分区绑定到不相交的物理 SM (MPS 的百分比做不到这一点)"
           : "FAIL 分区重叠, green ctx 未真正绑定 SM");
    if (!inter.empty()) {
        printf("       重叠 smid:");
        for (size_t i = 0; i < inter.size() && i < 16; i++) printf(" %u", inter[i]);
        printf("%s\n", inter.size() > 16 ? " ..." : "");
    }

    unsigned long long a0 = ~0ULL, a1 = 0, b0 = ~0ULL, b1 = 0;
    for (int i = 0; i < A.blocks; i++) { a0 = std::min(a0, A.t0[i]); a1 = std::max(a1, A.t1[i]); }
    for (int i = 0; i < B.blocks; i++) { b0 = std::min(b0, B.t0[i]); b1 = std::max(b1, B.t1[i]); }
    double spanA = (a1 - a0) / 1e6, spanB = (b1 - b0) / 1e6;
    double ov = (double)((long long)std::min(a1, b1) - (long long)std::max(a0, b0)) / 1e6;
    printf("\n[V3] A 区间 %.2fms, B 区间 %.2fms, 重叠 %.2fms, 墙钟 %.2fms\n",
           spanA, spanB, ov, wall_ms);
    double denom = std::min(spanA, spanB);
    printf("[V3] 重叠占较短一方的 %.1f%% -> %s\n", denom > 0 ? ov / denom * 100 : 0,
           (denom > 0 && ov / denom > 0.8)
           ? "PASS 两个 green ctx 真并发 (非时间片轮转)"
           : "FAIL 未并发, 退化为时间片");

    // ---- V4: 重分区代价 ----
    DRV(cuCtxSetCurrent(primary));
    const int REP = 200;
    auto r0 = std::chrono::steady_clock::now();
    for (int i = 0; i < REP; i++) {
        unsigned kk = 1 + (unsigned)(i % (ngroups - 1));
        CUdevResourceDesc d; CUgreenCtx g;
        DRV(cuDevResourceGenerateDesc(&d, groups.data(), kk));
        DRV(cuGreenCtxCreate(&g, d, dev, CU_GREEN_CTX_DEFAULT_STREAM));
        DRV(cuGreenCtxDestroy(g));
    }
    double rep_us = std::chrono::duration<double, std::micro>(
                        std::chrono::steady_clock::now() - r0).count() / REP;
    printf("\n[V4] 重分区 (generateDesc+create+destroy) 均摊 %.2f us/次  (Bullet 报 4.1us)\n", rep_us);

    printf("\n== 结论 ==\n");
    printf("分区绑定: %s | 真并发: %s | 重分区: %.2fus\n",
           inter.empty() ? "PASS" : "FAIL",
           (denom > 0 && ov / denom > 0.8) ? "PASS" : "FAIL", rep_us);
    return 0;
}
