// smid_share.cu -- 两个 kernel 的 block 会不会落到同一颗 SM 上并同时驻留?
//   模式 plain : 同一 context 两条普通 stream (不分区)
//   模式 green : 两个 green context (不相交分区)
// 对每个 block 记录 %smid 和 %globaltimer 起止, 然后逐 SM 检查
// A 的 block 区间与 B 的 block 区间是否有时间重叠 = 真正的"同 SM 共驻"。
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <map>
#include <algorithm>
#include <thread>
#include <cuda.h>
#include <cuda_runtime.h>

#define DRV(x) do{ CUresult _r=(x); if(_r!=CUDA_SUCCESS){ const char*_s=0; cuGetErrorString(_r,&_s); \
  fprintf(stderr,"[DRV] %s:%d -> %d (%s)\n",__FILE__,__LINE__,(int)_r,_s?_s:"?"); exit(1);} }while(0)

__global__ void mark_k(unsigned *smid, unsigned long long *t0,
                       unsigned long long *t1, unsigned long long ns)
{
    unsigned s; asm volatile("mov.u32 %0, %%smid;" : "=r"(s));
    unsigned long long a; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(a));
    if (threadIdx.x == 0) { smid[blockIdx.x] = s; t0[blockIdx.x] = a; }
    unsigned long long b = a;
    while (b - a < ns) { asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(b)); }
    if (threadIdx.x == 0) t1[blockIdx.x] = b;
}

struct Side {
    const char *name; int blocks;
    unsigned *d_s; unsigned long long *d_a, *d_b;
    std::vector<unsigned> s; std::vector<unsigned long long> a, b;
    CUcontext ctx; CUstream st;
};

static void go(Side *x, unsigned long long ns) {
    if (x->ctx) DRV(cuCtxSetCurrent(x->ctx));
    mark_k<<<x->blocks, 128, 0, (cudaStream_t)x->st>>>(x->d_s, x->d_a, x->d_b, ns);
    DRV(cuStreamSynchronize(x->st));
}

int main(int argc, char **argv)
{
    const char *mode = (argc > 1) ? argv[1] : "plain";
    int nb = (argc > 2) ? atoi(argv[2]) : 256;
    double ms = (argc > 3) ? atof(argv[3]) : 20.0;
    unsigned long long ns = (unsigned long long)(ms * 1e6);

    DRV(cuInit(0));
    CUdevice dev; DRV(cuDeviceGet(&dev, 0));
    CUcontext primary; DRV(cuDevicePrimaryCtxRetain(&primary, dev));
    DRV(cuCtxSetCurrent(primary));
    int nsm = 0; DRV(cuDeviceGetAttribute(&nsm, CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT, dev));

    Side A{"A"}, B{"B"};
    A.blocks = B.blocks = nb;
    for (Side *x : {&A, &B}) {
        cudaMalloc(&x->d_s, nb*sizeof(unsigned));
        cudaMalloc(&x->d_a, nb*sizeof(unsigned long long));
        cudaMalloc(&x->d_b, nb*sizeof(unsigned long long));
    }

    if (!strcmp(mode, "green")) {
        CUdevResource whole; DRV(cuDeviceGetDevResource(dev, &whole, CU_DEV_RESOURCE_TYPE_SM));
        unsigned ng = 0;
        DRV(cuDevSmResourceSplitByCount(NULL, &ng, &whole, NULL, 0, 64));
        std::vector<CUdevResource> g(ng); CUdevResource rem; memset(&rem, 0, sizeof rem);
        DRV(cuDevSmResourceSplitByCount(g.data(), &ng, &whole, &rem, 0, 64));
        CUdevResourceDesc dA, dB; CUgreenCtx gA, gB;
        DRV(cuDevResourceGenerateDesc(&dA, &g[0], 1));
        DRV(cuDevResourceGenerateDesc(&dB, &g[1], 1));
        DRV(cuGreenCtxCreate(&gA, dA, dev, CU_GREEN_CTX_DEFAULT_STREAM));
        DRV(cuGreenCtxCreate(&gB, dB, dev, CU_GREEN_CTX_DEFAULT_STREAM));
        DRV(cuCtxFromGreenCtx(&A.ctx, gA)); DRV(cuCtxFromGreenCtx(&B.ctx, gB));
        DRV(cuGreenCtxStreamCreate(&A.st, gA, CU_STREAM_NON_BLOCKING, 0));
        DRV(cuGreenCtxStreamCreate(&B.st, gB, CU_STREAM_NON_BLOCKING, 0));
    } else {
        A.ctx = B.ctx = primary;
        DRV(cuStreamCreate(&A.st, CU_STREAM_NON_BLOCKING));
        DRV(cuStreamCreate(&B.st, CU_STREAM_NON_BLOCKING));
    }

    { std::thread t1(go, &A, 1000000ULL), t2(go, &B, 1000000ULL); t1.join(); t2.join(); }
    { std::thread t1(go, &A, ns), t2(go, &B, ns); t1.join(); t2.join(); }

    DRV(cuCtxSetCurrent(primary));
    for (Side *x : {&A, &B}) {
        x->s.resize(nb); x->a.resize(nb); x->b.resize(nb);
        cudaMemcpy(x->s.data(), x->d_s, nb*sizeof(unsigned), cudaMemcpyDeviceToHost);
        cudaMemcpy(x->a.data(), x->d_a, nb*sizeof(unsigned long long), cudaMemcpyDeviceToHost);
        cudaMemcpy(x->b.data(), x->d_b, nb*sizeof(unsigned long long), cudaMemcpyDeviceToHost);
    }

    std::map<unsigned, std::vector<int>> ma, mb;
    for (int i = 0; i < nb; i++) { ma[A.s[i]].push_back(i); mb[B.s[i]].push_back(i); }
    int shared_sm = 0, cores_sm = 0;
    for (auto &kv : ma) {
        if (!mb.count(kv.first)) continue;
        shared_sm++;
        bool ov = false;
        for (int i : kv.second) for (int j : mb[kv.first])
            if (A.a[i] < B.b[j] && B.a[j] < A.b[i]) { ov = true; break; }
        if (ov) cores_sm++;
    }
    printf("mode=%-6s blocks/side=%-4d  A 占 %zu 个SM, B 占 %zu 个SM (共 %d)\n",
           mode, nb, ma.size(), mb.size(), nsm);
    printf("  两边都落到的 SM: %d 个;  其中 A/B 的 block 时间上真正共驻的: %d 个\n",
           shared_sm, cores_sm);
    printf("  -> %s\n", cores_sm > 0
           ? "不同 kernel 的 block 会同时驻留在同一颗 SM (SM 内共享 warp slot)"
           : "不同 kernel 的 block 落在不相交的 SM, 从不共驻");
    return 0;
}
