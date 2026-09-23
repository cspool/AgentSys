// scg_probe.cu -- 查 SCG 相关的用户态接口在本机的可用性
//  A. CiG (CUDA in Graphics): cuCtxCreate_v4 + CUctxCigParam —— 官方 SCG 接口
//  B. Exec Affinity (CU_EXEC_AFFINITY_TYPE_SM_COUNT): green context 的前身, CUDA 11.4 起
//     若可用, 测两个受限 ctx 能否真并发 + %smid 是否不相交
#include <cstdio>
#include <cstring>
#include <vector>
#include <set>
#include <thread>
#include <algorithm>
#include <cuda.h>
#include <cuda_runtime.h>

#define Q(x) ({ CUresult _r=(x); _r; })
#define MUST(x) do{ CUresult _r=(x); if(_r!=CUDA_SUCCESS){const char*_s=0;cuGetErrorString(_r,&_s);\
  fprintf(stderr,"[FAIL] %s:%d -> %d (%s)\n",__FILE__,__LINE__,(int)_r,_s?_s:"?");exit(1);} }while(0)

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

struct Arm { CUcontext ctx; CUstream st; int blocks;
             CUdeviceptr ds, da, db; std::vector<unsigned> s;
             std::vector<unsigned long long> a, b; };

int main(int argc, char **argv)
{
    int smA = (argc>1)?atoi(argv[1]):96, smB = (argc>2)?atoi(argv[2]):32;
    double ms = (argc>3)?atof(argv[3]):20.0;
    unsigned long long ns = (unsigned long long)(ms*1e6);
    MUST(cuInit(0));
    CUdevice dev; MUST(cuDeviceGet(&dev, 0));
    char nm[256]; MUST(cuDeviceGetName(nm,sizeof nm,dev));
    int nsm=0; MUST(cuDeviceGetAttribute(&nsm, CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT, dev));
    printf("device: %s  SM=%d\n\n", nm, nsm);

    // ---- A. CiG ----
    int cig = -1;
    CUresult rc = Q(cuDeviceGetAttribute(&cig, CU_DEVICE_ATTRIBUTE_D3D12_CIG_SUPPORTED, dev));
    printf("[A] CiG (CUDA in Graphics)\n");
    printf("    CU_DEVICE_ATTRIBUTE_D3D12_CIG_SUPPORTED = %d  (query rc=%d)\n", cig, (int)rc);
    printf("    可用的 CIG 数据类型: 仅 CIG_DATA_TYPE_D3D12_COMMAND_QUEUE (=0x1)\n");
    printf("    -> %s\n\n", cig == 1 ? "本机可用" :
           "本机不可用: CIG 只接受 D3D12 命令队列句柄, 是 Windows 路径; Linux 无对应 Vulkan 入口");

    // ---- B. Exec Affinity ----
    int ea = -1;
    rc = Q(cuDeviceGetExecAffinitySupport(&ea, CU_EXEC_AFFINITY_TYPE_SM_COUNT, dev));
    printf("[B] Exec Affinity (CU_EXEC_AFFINITY_TYPE_SM_COUNT, green context 的前身)\n");
    printf("    cuDeviceGetExecAffinitySupport = %d  (rc=%d)\n", ea, (int)rc);
    if (ea != 1) { printf("    -> 本机不支持\n"); return 0; }

    CUexecAffinityParam pa{}, pb{};
    pa.type = CU_EXEC_AFFINITY_TYPE_SM_COUNT; pa.param.smCount.val = smA;
    pb.type = CU_EXEC_AFFINITY_TYPE_SM_COUNT; pb.param.smCount.val = smB;
    Arm A{}, B{};
    rc = Q(cuCtxCreate_v3(&A.ctx, &pa, 1, 0, dev));
    if (rc != CUDA_SUCCESS) { const char*s=0; cuGetErrorString(rc,&s);
        printf("    cuCtxCreate_v3(SM=%d) 失败: %d (%s)\n", smA, (int)rc, s?s:"?");
        printf("    -> exec affinity 在本设备/本模式下不可用 (历史上它只在 MPS client 里生效)\n");
        return 0; }
    MUST(cuCtxCreate_v3(&B.ctx, &pb, 1, 0, dev));
    CUexecAffinityParam ga{}, gb{};
    MUST(cuCtxSetCurrent(A.ctx)); MUST(cuCtxGetExecAffinity(&ga, CU_EXEC_AFFINITY_TYPE_SM_COUNT));
    MUST(cuCtxSetCurrent(B.ctx)); MUST(cuCtxGetExecAffinity(&gb, CU_EXEC_AFFINITY_TYPE_SM_COUNT));
    printf("    ctx A 请求 %d -> 实得 %d SM;  ctx B 请求 %d -> 实得 %d SM\n",
           smA, ga.param.smCount.val, smB, gb.param.smCount.val);

    for (Arm *x : {&A, &B}) {
        MUST(cuCtxSetCurrent(x->ctx));
        x->blocks = (x == &A ? ga.param.smCount.val : gb.param.smCount.val) * 4;
        MUST(cuMemAlloc(&x->ds, x->blocks*sizeof(unsigned)));
        MUST(cuMemAlloc(&x->da, x->blocks*sizeof(unsigned long long)));
        MUST(cuMemAlloc(&x->db, x->blocks*sizeof(unsigned long long)));
        MUST(cuStreamCreate(&x->st, CU_STREAM_NON_BLOCKING));
    }
    // 运行时启动会在 current ctx 下自动加载模块
    auto go = [&](Arm *x) {
        cuCtxSetCurrent(x->ctx);
        probe_k<<<x->blocks,128,0,(cudaStream_t)x->st>>>(
            (unsigned*)x->ds,(unsigned long long*)x->da,(unsigned long long*)x->db, ns);
        cuStreamSynchronize(x->st);
    };
    { std::thread t1(go,&A), t2(go,&B); t1.join(); t2.join(); }   // 预热
    { std::thread t1(go,&A), t2(go,&B); t1.join(); t2.join(); }

    for (Arm *x : {&A,&B}) {
        MUST(cuCtxSetCurrent(x->ctx));
        x->s.resize(x->blocks); x->a.resize(x->blocks); x->b.resize(x->blocks);
        MUST(cuMemcpyDtoH(x->s.data(), x->ds, x->blocks*sizeof(unsigned)));
        MUST(cuMemcpyDtoH(x->a.data(), x->da, x->blocks*sizeof(unsigned long long)));
        MUST(cuMemcpyDtoH(x->b.data(), x->db, x->blocks*sizeof(unsigned long long)));
    }
    std::set<unsigned> sa(A.s.begin(),A.s.end()), sb(B.s.begin(),B.s.end());
    int inter=0; for(unsigned v:sa) if(sb.count(v)) inter++;
    unsigned long long a0=*std::min_element(A.a.begin(),A.a.end()), a1=*std::max_element(A.b.begin(),A.b.end());
    unsigned long long b0=*std::min_element(B.a.begin(),B.a.end()), b1=*std::max_element(B.b.begin(),B.b.end());
    double ov=(double)((long long)std::min(a1,b1)-(long long)std::max(a0,b0))/1e6;
    double spanA=(a1-a0)/1e6, spanB=(b1-b0)/1e6, den=std::min(spanA,spanB);
    printf("    A 实占 %zu 个物理 SM, B 实占 %zu 个, 交集 %d\n", sa.size(), sb.size(), inter);
    printf("    A 区间 %.2fms, B 区间 %.2fms, 重叠 %.2fms (%.1f%%)\n", spanA, spanB, ov,
           den>0?ov/den*100:0);
    printf("    -> SM 绑定: %s | 真并发: %s\n",
           inter==0?"不相交":"重叠",
           (den>0 && ov/den>0.8)?"是(两个受限 ctx 同时跑)":"否(退化为时间片轮转)");
    return 0;
}
