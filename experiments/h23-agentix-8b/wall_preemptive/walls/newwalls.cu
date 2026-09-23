#include <cstring>
// newwalls.cu -- 构造 L2 墙与 shared-memory 墙 (RTX 4090: L2=72MB, smem/SM=100KB, smem/block<=48KB)
//
// 目的: 补齐墙的类型学, 按"饱和资源是否 GPU 全局共享"分两组
//   每 SM 私有: smem / warp slot / 寄存器 / TC+发射带宽   -> 预测空间分区能隔离
//   GPU 全局  : L2 / DRAM 带宽 / 板级功耗                 -> 预测空间分区无效
//
// W5 L2 墙 : 工作集落在 72MB L2 内, 反复流式 -> L2 带宽饱和, DRAM 近零, 算力低
// W6 smem 墙: 全局访问极小, 流量压在 shared memory, 无 bank conflict
#include <cstdio>
#include <cstdlib>
#include <chrono>
#include <cuda_runtime.h>
#define RT(x) do{cudaError_t e=(x); if(e!=cudaSuccess){fprintf(stderr,"[RT]%s:%d %s\n",__FILE__,__LINE__,cudaGetErrorString(e));exit(1);}}while(0)

// ---- W5: L2 墙 ---- 4 路 ILP 保证吞吐受限而非延迟受限; 算术强度压到最低
__global__ void l2_wall_k(const float* __restrict__ x, float* __restrict__ y,
                          size_t n, int reps)
{
    size_t stride = (size_t)gridDim.x * blockDim.x * 4;
    for (int r = 0; r < reps; r++) {
        for (size_t i = ((size_t)blockIdx.x*blockDim.x + threadIdx.x)*4; i < n; i += stride) {
            size_t i0=i, i1=i+1, i2=i+2, i3=i+3;
            if (i3 < n) {
                float v0=x[i0], v1=x[i1], v2=x[i2], v3=x[i3];
                y[i0]=v0*1.000001f+1e-6f; y[i1]=v1*1.000001f+1e-6f;
                y[i2]=v2*1.000001f+1e-6f; y[i3]=v3*1.000001f+1e-6f;
            }
        }
    }
}

// ---- W6: smem 墙 ---- 每 block 一块 smem, 4 条独立链做 read-modify-write
// 索引用奇数步长避开 bank conflict; 结果写回 global 防止被优化掉
template<int SMEM_FLOATS>
__global__ void smem_wall_k(float* __restrict__ out, int iters)
{
    __shared__ float s[SMEM_FLOATS];
    const int tid = threadIdx.x, nt = blockDim.x;
    for (int i = tid; i < SMEM_FLOATS; i += nt) s[i] = (float)(i & 1023) + 1.0f;
    __syncthreads();
    const int M = SMEM_FLOATS - 1;                 // SMEM_FLOATS 必须是 2 的幂
    int i0 = tid & M, i1 = (tid*7+11) & M, i2 = (tid*13+29) & M, i3 = (tid*19+53) & M;
    float a0=0.f,a1=0.f,a2=0.f,a3=0.f;
    for (int it = 0; it < iters; it++) {
        float v0=s[i0], v1=s[i1], v2=s[i2], v3=s[i3];   // 4 条独立读
        a0+=v0; a1+=v1; a2+=v2; a3+=v3;
        i0=(i0+33)&M; i1=(i1+33)&M; i2=(i2+33)&M; i3=(i3+33)&M;  // 奇数步长, 无 bank conflict
        s[i0]=v0*1.000001f; s[i1]=v1*1.000001f;                   // 4 条独立写
        s[i2]=v2*1.000001f; s[i3]=v3*1.000001f;
    }
    if (tid == 0) out[blockIdx.x] = a0+a1+a2+a3;
}

static double bench(void(*launch)(void*,int,int), void* arg, int a, int b, int warm=2, int rep=5)
{ (void)launch;(void)arg;(void)a;(void)b;(void)warm;(void)rep; return 0; }

int main(int argc, char** argv)
{
    const char* mode = (argc>1)?argv[1]:"l2";
    cudaDeviceProp p; RT(cudaGetDeviceProperties(&p,0));
    int NSM = p.multiProcessorCount;
    printf("%s  SM=%d  L2=%.0fMB  smem/SM=%.0fKB\n", p.name, NSM,
           p.l2CacheSize/1048576.0, p.sharedMemPerMultiprocessor/1024.0);

    if (!strcmp(mode,"l2")) {
        // 扫工作集大小: x+y 两块各 SZ_MB/2, 总和要 < 72MB 才可能常驻 L2
        printf("\n%-10s %-10s %-9s %-12s %-10s\n","总工作集","n(百万)","grid","单次ms","有效GB/s");
        for (double tot_mb : {8.0, 16.0, 24.0, 32.0, 40.0, 48.0, 56.0, 64.0, 96.0, 192.0, 480.0}) {
            size_t n = (size_t)(tot_mb*1048576.0/2/4);     // x 与 y 各占一半
            n = (n/4096)*4096;
            float *x,*y; RT(cudaMalloc(&x,n*4)); RT(cudaMalloc(&y,n*4));
            RT(cudaMemset(x,1,n*4));
            int grid = NSM*8, blk = 256, reps = 20;
            l2_wall_k<<<grid,blk>>>(x,y,n,2); RT(cudaDeviceSynchronize());
            auto t0=std::chrono::steady_clock::now();
            l2_wall_k<<<grid,blk>>>(x,y,n,reps); RT(cudaDeviceSynchronize());
            double ms=std::chrono::duration<double,std::milli>(std::chrono::steady_clock::now()-t0).count();
            double bytes = (double)n*4*2*reps;             // 读 x + 写 y
            printf("%-10.0f %-10.1f %-9d %-12.2f %-10.0f\n",
                   tot_mb, n/1e6, grid, ms/reps, bytes/(ms/1000)/1e9);
            cudaFree(x); cudaFree(y);
        }
    } else if (!strcmp(mode,"prof")) {
        // NCU 专用: 每种墙各发射一次, 用选定的配置
        const char* which = (argc>2)?argv[2]:"l2";
        if (!strcmp(which,"l2")) {
            size_t n=(size_t)(32.0*1048576.0/2/4); n=(n/4096)*4096;
            float *x,*y; RT(cudaMalloc(&x,n*4)); RT(cudaMalloc(&y,n*4)); RT(cudaMemset(x,1,n*4));
            l2_wall_k<<<NSM*8,256>>>(x,y,n,4); RT(cudaDeviceSynchronize());   // 预热
            l2_wall_k<<<NSM*8,256>>>(x,y,n,40); RT(cudaDeviceSynchronize());  // 被 profile 的那次
        } else {
            float* out; RT(cudaMalloc(&out,NSM*16*4));
            smem_wall_k<8192><<<NSM*3,256>>>(out,200); RT(cudaDeviceSynchronize());
            smem_wall_k<8192><<<NSM*3,256>>>(out,20000); RT(cudaDeviceSynchronize());
        }
    } else {
        // 扫 smem 大小与 block 数: smem/block<=48KB, 每 SM 100KB
        printf("\n%-12s %-9s %-9s %-11s %-12s\n","smem/block","blockDim","blocks/SM","单次ms","smem GB/s");
        float* out; RT(cudaMalloc(&out,NSM*16*4));
        int iters = 20000;
        #define TRY(SF, BD) { \
            int smem_b = SF*4; int bps = 102400/smem_b; if(bps>16) bps=16; \
            int grid = NSM*bps; \
            smem_wall_k<SF><<<grid,BD>>>(out, 200); RT(cudaDeviceSynchronize()); \
            auto t0=std::chrono::steady_clock::now(); \
            smem_wall_k<SF><<<grid,BD>>>(out, iters); RT(cudaDeviceSynchronize()); \
            double ms=std::chrono::duration<double,std::milli>(std::chrono::steady_clock::now()-t0).count(); \
            double bytes=(double)grid*BD*iters*8*4; \
            printf("%-12d %-9d %-9d %-11.2f %-12.0f\n", smem_b/1024, BD, bps, ms, bytes/(ms/1000)/1e9); }
        TRY(2048, 256)   // 8KB
        TRY(4096, 256)   // 16KB
        TRY(8192, 256)   // 32KB
        TRY(8192, 512)
        TRY(4096, 512)
        TRY(4096, 128)
        cudaFree(out);
    }
    return 0;
}
