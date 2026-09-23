// mpk_probe.cu -- 角度3: SM 内驻留持久 kernel, 记录运行中各资源亲和类型的任务数,
//                 据此抓取互补类型的任务来拉高资源使用率 (SCG arbiter 的软件版)
// 依据本地笔记 MPK-tGraph-Mega-Kernel化(worker/scheduler SM 分工 + task/event 队列)
//             与 SCG-SM(arbiter 监控 SM 资源使用率找 hole 再申请 CTA)
//
// 三种核内调度策略, 同一份混合任务集(一半访存亲和, 一半算力亲和):
//   fifo      单队列先到先得 —— 亲和盲(基线)
//   affinity  每个 worker 看本 SM 上两类任务的在跑数, 取欠缺的那一类
//   alternate  每个 worker 严格交替取两类 —— 对照: 只做"混"而不看运行时状态
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <chrono>
#include <cuda_runtime.h>
#define RT(x) do{cudaError_t e=(x); if(e!=cudaSuccess){fprintf(stderr,"[RT]%s:%d %s\n",__FILE__,__LINE__,cudaGetErrorString(e));exit(1);}}while(0)

#define T_MEM 0
#define T_CMP 1

struct Task { int type; int arg0; int arg1; };

__device__ __forceinline__ void run_mem(const float* x, float* y, size_t base,
                                        size_t len, int inner)
{
    for (size_t i = threadIdx.x; i < len; i += blockDim.x) {
        float v = x[base + i];
        #pragma unroll
        for (int k = 0; k < 8; k++) v = v * 1.000001f + 0.000001f;
        y[base + i] = v;
    }
    (void)inner;
}
__device__ __forceinline__ void run_cmp(float* z, size_t base, int reps)
{
    float v = z[base + threadIdx.x];
    for (int r = 0; r < reps; r++) v = v * 1.000001f + 0.000001f;
    z[base + threadIdx.x] = v;
}

// head[0]=MEM 队列游标, head[1]=CMP 队列游标, head[2]=混合队列游标
__global__ void persist_k(const float* x, float* y, float* z,
                          const Task* qmem, int nmem, const Task* qcmp, int ncmp,
                          const Task* qmix, int nmix,
                          int* head, int* running, int policy, int* done_cnt)
{
    unsigned sm; asm volatile("mov.u32 %0, %%smid;" : "=r"(sm));
    __shared__ int s_idx, s_type;
    int turn = blockIdx.x & 1;
    while (true) {
        if (threadIdx.x == 0) {
            int t = -1, idx = -1;
            if (policy == 0) {                       // fifo: 单混合队列
                idx = atomicAdd(&head[2], 1);
                t = (idx < nmix) ? qmix[idx].type : -1;
                if (idx >= nmix) idx = -1;
            } else {
                int want;
                if (policy == 1) {                   // affinity: 看本 SM 在跑的两类任务数
                    // 用普通 volatile 读而非 atomicAdd(..,0), 否则读本身就是重原子操作
                    volatile int* rv = (volatile int*)running;
                    int m = rv[sm*2 + T_MEM], c = rv[sm*2 + T_CMP];
                    want = (m <= c) ? T_MEM : T_CMP;
                } else {                             // alternate: 严格交替
                    want = turn; turn ^= 1;
                }
                int other = want ^ 1;
                int n0 = want ? ncmp : nmem;
                idx = atomicAdd(&head[want], 1);
                if (idx < n0) { t = want; }
                else {
                    int n1 = other ? ncmp : nmem;
                    idx = atomicAdd(&head[other], 1);
                    if (idx < n1) t = other; else idx = -1;
                }
            }
            s_idx = idx; s_type = t;
            if (idx >= 0) atomicAdd(&running[sm*2 + t], 1);
        }
        __syncthreads();
        int idx = s_idx, t = s_type;
        if (idx < 0) break;
        const Task* q = (policy == 0) ? qmix : (t == T_MEM ? qmem : qcmp);
        Task tk = q[idx];
        if (t == T_MEM) run_mem(x, y, (size_t)tk.arg0 * tk.arg1, tk.arg1, 8);
        else            run_cmp(z, (size_t)blockIdx.x * blockDim.x, tk.arg0);
        __syncthreads();
        if (threadIdx.x == 0) {
            atomicSub(&running[sm*2 + t], 1);
            atomicAdd(done_cnt, 1);
        }
    }
}

int main(int argc, char** argv)
{
    int NT   = (argc > 1) ? atoi(argv[1]) : 1024;      // 每类任务数
    int CREP = (argc > 2) ? atoi(argv[2]) : 260000;    // CMP 任务的 FMA 次数
    int BS   = (argc > 3) ? atoi(argv[3]) : 256;
    int WPS  = (argc > 4) ? atoi(argv[4]) : 4;         // 每 SM 常驻 worker 数
    cudaDeviceProp p; RT(cudaGetDeviceProperties(&p, 0));
    int NSM = p.multiProcessorCount, NB = NSM * WPS;
    size_t N = 240ull * 1000 * 1000, SLICE = N / NT;   // 两类任务总时长配平

    float *x, *y, *z;
    RT(cudaMalloc(&x, N*sizeof(float))); RT(cudaMalloc(&y, N*sizeof(float)));
    RT(cudaMalloc(&z, (size_t)NB*BS*sizeof(float)));
    RT(cudaMemset(x, 1, N*sizeof(float))); RT(cudaMemset(z, 1, (size_t)NB*BS*sizeof(float)));

    std::vector<Task> hm(NT), hc(NT), hx(2*NT);
    for (int i = 0; i < NT; i++) { hm[i] = {T_MEM, i, (int)SLICE}; hc[i] = {T_CMP, CREP, 0}; }
    // 成块到达: 先全部访存任务, 再全部算力任务 —— 像真实的 prefill/decode 相位
    // (交错混合会让 FIFO 基线白白拿到完美配比, 不公平)
    for (int i = 0; i < NT; i++) hx[i] = hm[i];
    for (int i = 0; i < NT; i++) hx[NT+i] = hc[i];
    Task *dm, *dc, *dx;
    RT(cudaMalloc(&dm, NT*sizeof(Task))); RT(cudaMalloc(&dc, NT*sizeof(Task)));
    RT(cudaMalloc(&dx, 2*NT*sizeof(Task)));
    RT(cudaMemcpy(dm, hm.data(), NT*sizeof(Task), cudaMemcpyHostToDevice));
    RT(cudaMemcpy(dc, hc.data(), NT*sizeof(Task), cudaMemcpyHostToDevice));
    RT(cudaMemcpy(dx, hx.data(), 2*NT*sizeof(Task), cudaMemcpyHostToDevice));

    int *head, *running, *done;
    RT(cudaMalloc(&head, 3*sizeof(int)));
    RT(cudaMalloc(&running, NSM*2*sizeof(int)));
    RT(cudaMalloc(&done, sizeof(int)));

    printf("%s SM=%d  常驻 %d 块/SM x %d 线程  任务: %d 访存 + %d 算力\n",
           p.name, NSM, WPS, BS, NT, NT);
    printf("单任务规模: 访存 %zu 元素, 算力 %d FMA\n\n", SLICE, CREP);
    printf("%-12s %-12s %-10s\n", "核内策略", "makespan", "vs fifo");
    double base = 0;
    const char* names[] = {"fifo", "affinity", "alternate"};
    for (int rep = 0; rep < 2; rep++) {
      for (int pol = 0; pol < 3; pol++) {
        RT(cudaMemset(head, 0, 3*sizeof(int)));
        RT(cudaMemset(running, 0, NSM*2*sizeof(int)));
        RT(cudaMemset(done, 0, sizeof(int)));
        auto t0 = std::chrono::steady_clock::now();
        persist_k<<<NB, BS>>>(x, y, z, dm, NT, dc, NT, dx, 2*NT, head, running, pol, done);
        RT(cudaDeviceSynchronize());
        double ms = std::chrono::duration<double,std::milli>(
                        std::chrono::steady_clock::now()-t0).count();
        int hd; RT(cudaMemcpy(&hd, done, sizeof(int), cudaMemcpyDeviceToHost));
        if (rep == 0) { if (pol == 0) base = ms; continue; }   // 第一轮预热
        if (pol == 0) base = ms;
        printf("%-12s %8.1f ms   %6.2f×   (完成 %d/%d 任务)\n",
               names[pol], ms, base/ms, hd, 2*NT);
      }
    }
    return 0;
}
