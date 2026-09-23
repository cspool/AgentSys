// gc_cost.cu -- green context 的代价与粒度测量
//  C1 建 green ctx 的分步代价 (generateDesc / create / destroy)
//  C2 预建池 + 切换的代价 (这才是调度器每次抢占真正要付的)
//  C3 粒度扫描: Ada 上能切出哪些分区, 含 IGNORE_SM_COSCHEDULING
//  C4 最小抢占者分区能不能真跑 (4 SM 的 preemptor)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <algorithm>
#include <chrono>
#include <cuda.h>
#include <cuda_runtime.h>

#define DRV(x) do{ CUresult _r=(x); if(_r!=CUDA_SUCCESS){ const char*_s=0; cuGetErrorString(_r,&_s); \
  fprintf(stderr,"[DRV FAIL] %s:%d %s -> %d (%s)\n",__FILE__,__LINE__,#x,(int)_r,_s?_s:"?"); exit(1);} }while(0)
#define DRVQ(x) ({ CUresult _r=(x); _r; })
#define RT(x) do{ cudaError_t _e=(x); if(_e!=cudaSuccess){ \
  fprintf(stderr,"[RT FAIL] %s:%d %s -> %s\n",__FILE__,__LINE__,#x,cudaGetErrorString(_e)); exit(1);} }while(0)

using clk = std::chrono::steady_clock;
static double us_since(clk::time_point t) {
    return std::chrono::duration<double, std::micro>(clk::now() - t).count();
}

__global__ void tiny_k(unsigned *out) { if (threadIdx.x == 0) out[blockIdx.x] = blockIdx.x; }
__global__ void smid_k(unsigned *out) {
    unsigned s; asm volatile("mov.u32 %0, %%smid;" : "=r"(s));
    if (threadIdx.x == 0) out[blockIdx.x] = s;
}

int main(int argc, char **argv)
{
    DRV(cuInit(0));
    CUdevice dev; DRV(cuDeviceGet(&dev, 0));
    int nsm = 0;
    DRV(cuDeviceGetAttribute(&nsm, CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT, dev));
    CUcontext primary; DRV(cuDevicePrimaryCtxRetain(&primary, dev));
    DRV(cuCtxSetCurrent(primary));
    printf("device SM=%d\n\n", nsm);

    CUdevResource whole;
    DRV(cuDeviceGetDevResource(dev, &whole, CU_DEV_RESOURCE_TYPE_SM));

    // ================= C3 粒度扫描 =================
    printf("== C3 粒度扫描 ==\n");
    printf("%-10s %-8s %-8s %-10s\n", "minCount", "flags", "ngroups", "per-group");
    for (unsigned flags : {0u, (unsigned)CU_DEV_SM_RESOURCE_SPLIT_IGNORE_SM_COSCHEDULING}) {
        for (unsigned mc : {1u, 2u, 4u, 6u, 8u, 16u, 32u, 64u}) {
            unsigned ng = 0;
            CUresult r = cuDevSmResourceSplitByCount(NULL, &ng, &whole, NULL, flags, mc);
            if (r != CUDA_SUCCESS) { printf("%-10u %-8s  (err %d)\n", mc, flags?"IGNORE":"0", (int)r); continue; }
            std::vector<CUdevResource> g(ng ? ng : 1);
            CUdevResource rem; memset(&rem, 0, sizeof rem);
            unsigned ng2 = ng;
            if (ng) DRV(cuDevSmResourceSplitByCount(g.data(), &ng2, &whole, &rem, flags, mc));
            printf("%-10u %-8s %-8u %-10u (remaining=%u)\n", mc, flags ? "IGNORE" : "0", ng,
                   ng ? g[0].sm.smCount : 0,
                   rem.type == CU_DEV_RESOURCE_TYPE_SM ? rem.sm.smCount : 0);
        }
    }

    // ================= C1 分步代价 =================
    printf("\n== C1 建 green ctx 分步代价 (minCount=16, 取 1 group) ==\n");
    unsigned ng = 0;
    DRV(cuDevSmResourceSplitByCount(NULL, &ng, &whole, NULL, 0, 16));
    std::vector<CUdevResource> groups(ng);
    CUdevResource rem; memset(&rem, 0, sizeof rem);
    DRV(cuDevSmResourceSplitByCount(groups.data(), &ng, &whole, &rem, 0, 16));

    const int REP = 100;
    double t_desc = 0, t_create = 0, t_destroy = 0;
    for (int i = 0; i < REP; i++) {
        CUdevResourceDesc d; CUgreenCtx g;
        auto t = clk::now(); DRV(cuDevResourceGenerateDesc(&d, groups.data(), 2)); t_desc += us_since(t);
        t = clk::now(); DRV(cuGreenCtxCreate(&g, d, dev, CU_GREEN_CTX_DEFAULT_STREAM)); t_create += us_since(t);
        t = clk::now(); DRV(cuGreenCtxDestroy(g)); t_destroy += us_since(t);
    }
    printf("generateDesc %8.2f us\ncreate       %8.2f us\ndestroy      %8.2f us\n合计         %8.2f us\n",
           t_desc/REP, t_create/REP, t_destroy/REP, (t_desc+t_create+t_destroy)/REP);

    // ================= C2 预建池 + 切换代价 =================
    printf("\n== C2 预建池 + 切换代价 (调度器每次抢占真正付的) ==\n");
    // 建一个 "preemptor 拿 k 个 group" 的池: k = 1..ng-1
    struct Slot { CUgreenCtx g; CUcontext c; CUstream s; unsigned sm; };
    std::vector<Slot> pool;
    auto tpool = clk::now();
    for (unsigned k = 1; k < ng; k++) {
        Slot sl{};
        CUdevResourceDesc d;
        DRV(cuDevResourceGenerateDesc(&d, groups.data(), k));
        DRV(cuGreenCtxCreate(&sl.g, d, dev, CU_GREEN_CTX_DEFAULT_STREAM));
        DRV(cuCtxFromGreenCtx(&sl.c, sl.g));
        DRV(cuGreenCtxStreamCreate(&sl.s, sl.g, CU_STREAM_NON_BLOCKING, 0));
        CUdevResource r; DRV(cuGreenCtxGetDevResource(sl.g, &r, CU_DEV_RESOURCE_TYPE_SM));
        sl.sm = r.sm.smCount;
        pool.push_back(sl);
    }
    printf("池: %zu 个分区 (", pool.size());
    for (auto &s : pool) printf("%u ", s.sm);
    printf("SM), 一次性建池 %.2f us\n", us_since(tpool));

    unsigned *dout; DRV(cuCtxSetCurrent(primary)); RT(cudaMalloc(&dout, 1024 * sizeof(unsigned)));
    // 预热每个 slot
    for (auto &s : pool) {
        DRV(cuCtxSetCurrent(s.c));
        tiny_k<<<1, 32, 0, (cudaStream_t)s.s>>>(dout);
        DRV(cuStreamSynchronize(s.s));
    }
    // 切换代价 = cuCtxSetCurrent + 在该分区流上发射 (不含 kernel 执行)
    double t_switch = 0, t_launch = 0;
    const int REP2 = 2000;
    for (int i = 0; i < REP2; i++) {
        Slot &s = pool[i % pool.size()];
        auto t = clk::now(); DRV(cuCtxSetCurrent(s.c)); t_switch += us_since(t);
        t = clk::now(); tiny_k<<<1, 32, 0, (cudaStream_t)s.s>>>(dout); t_launch += us_since(t);
    }
    for (auto &s : pool) { DRV(cuCtxSetCurrent(s.c)); DRV(cuStreamSynchronize(s.s)); }
    printf("cuCtxSetCurrent  %7.3f us\n异步 launch      %7.3f us\n切换总计         %7.3f us\n",
           t_switch/REP2, t_launch/REP2, (t_switch+t_launch)/REP2);

    // ================= C4 最小分区可用性 =================
    printf("\n== C4 最小 preemptor 分区 ==\n");
    for (unsigned mc : {4u, 8u, 16u}) {
        unsigned n2 = 0;
        if (cuDevSmResourceSplitByCount(NULL, &n2, &whole, NULL, 0, mc) != CUDA_SUCCESS || n2 < 2) {
            printf("minCount=%u 不可用\n", mc); continue;
        }
        std::vector<CUdevResource> g2(n2);
        CUdevResource rm; memset(&rm, 0, sizeof rm);
        DRV(cuDevSmResourceSplitByCount(g2.data(), &n2, &whole, &rm, 0, mc));
        CUdevResourceDesc d; CUgreenCtx gc; CUcontext cc; CUstream ss;
        DRV(cuDevResourceGenerateDesc(&d, g2.data(), 1));
        DRV(cuGreenCtxCreate(&gc, d, dev, CU_GREEN_CTX_DEFAULT_STREAM));
        DRV(cuCtxFromGreenCtx(&cc, gc));
        DRV(cuGreenCtxStreamCreate(&ss, gc, CU_STREAM_NON_BLOCKING, 0));
        CUdevResource r; DRV(cuGreenCtxGetDevResource(gc, &r, CU_DEV_RESOURCE_TYPE_SM));
        int blocks = (int)r.sm.smCount * 4;
        DRV(cuCtxSetCurrent(cc));
        smid_k<<<blocks, 256, 0, (cudaStream_t)ss>>>(dout);
        DRV(cuStreamSynchronize(ss));
        std::vector<unsigned> h(blocks);
        RT(cudaMemcpy(h.data(), dout, blocks * sizeof(unsigned), cudaMemcpyDeviceToHost));
        std::sort(h.begin(), h.end());
        h.erase(std::unique(h.begin(), h.end()), h.end());
        printf("minCount=%-3u 分到 %2u SM, 实测占用 %2zu 个物理 SM -> %s\n",
               mc, r.sm.smCount, h.size(), h.size() == r.sm.smCount ? "精确" : "不符");
        DRV(cuGreenCtxDestroy(gc));
    }
    return 0;
}
