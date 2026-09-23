// conn_probe.cu -- channel/connection 层是否限制 stream 并发?
// 每条 stream 只发 4 个 block(远小于 128 SM), 所以 SM 绝不是瓶颈;
// 若只有 K 条 stream 真并发, K 就是硬件工作队列(HyperQ connection)数。
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <cuda_runtime.h>
#include <cuda.h>

__global__ void spin_k(unsigned long long *t0, unsigned long long *t1,
                       unsigned long long ns, int sid)
{
    unsigned long long a; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(a));
    if (threadIdx.x == 0 && blockIdx.x == 0) t0[sid] = a;
    unsigned long long b = a;
    while (b - a < ns) { asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(b)); }
    if (threadIdx.x == 0 && blockIdx.x == 0) t1[sid] = b;
}

int main(int argc, char **argv)
{
    int N = (argc > 1) ? atoi(argv[1]) : 16;
    double ms = (argc > 2) ? atof(argv[2]) : 30.0;
    unsigned long long ns = (unsigned long long)(ms * 1e6);
    const char *env = getenv("CUDA_DEVICE_MAX_CONNECTIONS");
    unsigned long long *t0, *t1;
    cudaMalloc(&t0, N * sizeof(*t0)); cudaMalloc(&t1, N * sizeof(*t1));
    std::vector<cudaStream_t> s(N);
    for (int i = 0; i < N; i++) cudaStreamCreateWithFlags(&s[i], cudaStreamNonBlocking);
    // 预热
    for (int i = 0; i < N; i++) spin_k<<<4, 32, 0, s[i]>>>(t0, t1, 1000000ULL, i);
    cudaDeviceSynchronize();
    for (int i = 0; i < N; i++) spin_k<<<4, 32, 0, s[i]>>>(t0, t1, ns, i);
    cudaDeviceSynchronize();
    std::vector<unsigned long long> h0(N), h1(N);
    cudaMemcpy(h0.data(), t0, N*sizeof(*t0), cudaMemcpyDeviceToHost);
    cudaMemcpy(h1.data(), t1, N*sizeof(*t1), cudaMemcpyDeviceToHost);
    // 最大同时重叠数 = 扫描线
    std::vector<std::pair<unsigned long long,int>> ev;
    for (int i = 0; i < N; i++) { ev.push_back({h0[i], +1}); ev.push_back({h1[i], -1}); }
    std::sort(ev.begin(), ev.end());
    int cur = 0, mx = 0;
    for (auto &e : ev) { cur += e.second; mx = std::max(mx, cur); }
    unsigned long long lo = *std::min_element(h0.begin(), h0.end());
    unsigned long long hi = *std::max_element(h1.begin(), h1.end());
    printf("CUDA_DEVICE_MAX_CONNECTIONS=%-4s streams=%-3d 每条%.0fms  "
           "最大并发=%-3d  总墙钟=%.1fms (串行则应为%.0fms)\n",
           env ? env : "unset", N, ms, mx, (hi - lo) / 1e6, ms * N);
    return 0;
}
