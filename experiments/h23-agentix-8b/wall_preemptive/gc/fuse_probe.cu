// fuse_probe.cu -- 角度1: 混合负载打包进一个 kernel 的三个层级
// 对标 POD-Attention Table 2 (Streams / CTA / Warp(HFuse) / Intra-thread)
//   serial      顺序执行(基线)
//   streams     两条流并发           (GC=✗ 不保证共位, WQ=✓)
//   cta_fused   一个 kernel 按 blockIdx 分工  (GC=✗, WQ=✓, 负载均衡容易)
//   warp_fused  一个 kernel 按 warp 分工(HFuse) (GC=✓ 保证共位, WQ=✗ straggler)
// 受害者=DRAM 流式(访存墙), 抢占者=纯寄存器 FMA(算力), 资源亲和互补
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <chrono>
#include <thread>
#include <cuda_runtime.h>
#define RT(x) do{cudaError_t e=(x); if(e!=cudaSuccess){fprintf(stderr,"[RT]%s:%d %s\n",__FILE__,__LINE__,cudaGetErrorString(e));exit(1);}}while(0)

__device__ __forceinline__ void mem_body(const float*x,float*y,size_t n,int reps,
                                         size_t gid,size_t stride){
    for(int r=0;r<reps;r++)
        for(size_t i=gid;i<n;i+=stride){
            float v=x[i];
            #pragma unroll
            for(int k=0;k<8;k++) v=v*1.000001f+0.000001f;
            y[i]=v;
        }
}
__device__ __forceinline__ void cmp_body(float*z,int reps,size_t gid){
    float v=z[gid];
    for(int r=0;r<reps;r++) v=v*1.000001f+0.000001f;
    z[gid]=v;
}
__global__ void mem_k(const float*x,float*y,size_t n,int reps){
    mem_body(x,y,n,reps,(size_t)blockIdx.x*blockDim.x+threadIdx.x,
             (size_t)gridDim.x*blockDim.x);
}
__global__ void cmp_k(float*z,int reps){
    cmp_body(z,reps,(size_t)blockIdx.x*blockDim.x+threadIdx.x);
}
// CTA 级融合: 前 vnb 个 block 干受害者活, 其余干抢占者活
__global__ void cta_fused_k(const float*x,float*y,size_t n,int v_reps,
                            float*z,int c_reps,int vnb){
    if(blockIdx.x<vnb)
        mem_body(x,y,n,v_reps,(size_t)blockIdx.x*blockDim.x+threadIdx.x,
                 (size_t)vnb*blockDim.x);
    else
        cmp_body(z,c_reps,(size_t)(blockIdx.x-vnb)*blockDim.x+threadIdx.x);
}
// Warp 级融合(HFuse): 每个 block 内前 vw 个 warp 干受害者活, 其余干抢占者活
__global__ void warp_fused_k(const float*x,float*y,size_t n,int v_reps,
                             float*z,int c_reps,int vw){
    int w=threadIdx.x>>5, lane=threadIdx.x&31;
    int nw=blockDim.x>>5;
    if(w<vw){
        size_t gid=((size_t)blockIdx.x*vw+w)*32+lane;
        mem_body(x,y,n,v_reps,gid,(size_t)gridDim.x*vw*32);
    }else{
        size_t gid=((size_t)blockIdx.x*(nw-vw)+(w-vw))*32+lane;
        cmp_body(z,c_reps,gid);
    }
}

int main(int argc,char**argv){
    size_t N=60ull*1000*1000;
    int v_reps=(argc>1)?atoi(argv[1]):60;
    int c_reps=(argc>2)?atoi(argv[2]):11000000;
    int BS=(argc>3)?atoi(argv[3]):256;
    cudaDeviceProp p; RT(cudaGetDeviceProperties(&p,0));
    int NSM=p.multiProcessorCount;
    int VNB=NSM, CNB=NSM*2;                       // 受害者 1 块/SM, 抢占者 2 块/SM
    float *x,*y,*z;
    RT(cudaMalloc(&x,N*sizeof(float))); RT(cudaMalloc(&y,N*sizeof(float)));
    RT(cudaMalloc(&z,(size_t)(CNB+VNB)*BS*4*sizeof(float)));
    RT(cudaMemset(x,1,N*sizeof(float)));
    RT(cudaMemset(z,1,(size_t)(CNB+VNB)*BS*4*sizeof(float)));
    cudaStream_t s1,s2;
    RT(cudaStreamCreateWithFlags(&s1,cudaStreamNonBlocking));
    RT(cudaStreamCreateWithFlags(&s2,cudaStreamNonBlocking));
    auto tick=[&](const char*name, auto fn){
        fn(); RT(cudaDeviceSynchronize());                     // 预热
        auto t0=std::chrono::steady_clock::now();
        fn(); RT(cudaDeviceSynchronize());
        double ms=std::chrono::duration<double,std::milli>(
            std::chrono::steady_clock::now()-t0).count();
        printf("%-14s %8.1f ms\n",name,ms); return ms;
    };
    printf("blockDim=%d  受害者 %d 块  抢占者 %d 块  (SM=%d)\n\n",BS,VNB,CNB,NSM);
    double v_solo=tick("victim单独",[&]{ mem_k<<<VNB,BS>>>(x,y,N,v_reps); });
    double c_solo=tick("burst单独", [&]{ cmp_k<<<CNB,BS>>>(z,c_reps); });
    printf("%-14s %8.1f ms  <- 基线\n","serial",v_solo+c_solo);
    tick("streams",[&]{ mem_k<<<VNB,BS,0,s1>>>(x,y,N,v_reps);
                        cmp_k<<<CNB,BS,0,s2>>>(z,c_reps); });
    tick("cta_fused",[&]{ cta_fused_k<<<VNB+CNB,BS>>>(x,y,N,v_reps,z,c_reps,VNB); });
    int nw=BS/32;
    for(int vw : {nw/4, nw/2, 3*nw/4}){
        if(vw<1||vw>=nw) continue;
        char nm[64]; snprintf(nm,sizeof nm,"warp_fused %d/%d",vw,nw);
        tick(nm,[&]{ warp_fused_k<<<VNB,BS>>>(x,y,N,v_reps,z,c_reps,vw); });
    }
    return 0;
}
