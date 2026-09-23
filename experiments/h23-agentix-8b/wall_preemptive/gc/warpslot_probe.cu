// warpslot_probe.cu -- blockDim>=512 为何杀死跨 kernel 共驻?
// 假设: Ada SM 有 4 个 sub-partition, 每个 12 个 warp slot。一个 block 的 warp 按
// round-robin 分到 sub-partition, 因此 block 需要 ceil(warps/4) 个 slot/sub-partition。
// 若受害者 blockDim=512(16 warp)=每 sub-partition 4 slot, 仍余 8 slot, 按理能容纳抢占者。
// 本探针把"是谁挡住谁"拆开: 分别扫 受害者 blockDim 与 抢占者 blockDim, 看阈值挂在哪一侧。
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <map>
#include <algorithm>
#include <thread>
#include <chrono>
#include <cuda_runtime.h>

#define RT(x) do{ cudaError_t e=(x); if(e!=cudaSuccess){ \
  fprintf(stderr,"[RT] %s:%d %s\n",__FILE__,__LINE__,cudaGetErrorString(e)); exit(1);} }while(0)

__global__ void mem_k(const float* __restrict__ x, float* __restrict__ y, size_t n,
                      int reps, unsigned *smid, unsigned long long *t0, unsigned long long *t1)
{
    unsigned s; asm volatile("mov.u32 %0, %%smid;" : "=r"(s));
    unsigned long long a; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(a));
    if (threadIdx.x == 0) { smid[blockIdx.x] = s; t0[blockIdx.x] = a; }
    size_t stride = (size_t)gridDim.x * blockDim.x;
    for (int r = 0; r < reps; r++)
        for (size_t i = (size_t)blockIdx.x*blockDim.x + threadIdx.x; i < n; i += stride) {
            float v = x[i];
            for (int k = 0; k < 8; k++) v = v*1.000001f + 0.000001f;
            y[i] = v;
        }
    unsigned long long b; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(b));
    if (threadIdx.x == 0) t1[blockIdx.x] = b;
}
__global__ void cmp_k(float* __restrict__ z, int reps, unsigned *smid,
                      unsigned long long *t0, unsigned long long *t1)
{
    unsigned s; asm volatile("mov.u32 %0, %%smid;" : "=r"(s));
    unsigned long long a; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(a));
    if (threadIdx.x == 0) { smid[blockIdx.x] = s; t0[blockIdx.x] = a; }
    float v = z[blockIdx.x*blockDim.x + threadIdx.x];
    for (int r = 0; r < reps; r++) v = v*1.000001f + 0.000001f;
    z[blockIdx.x*blockDim.x + threadIdx.x] = v;
    unsigned long long b; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(b));
    if (threadIdx.x == 0) t1[blockIdx.x] = b;
}

struct Buf { unsigned *s; unsigned long long *a,*b; int nb; };
static Buf mk(int nb){ Buf x{}; x.nb=nb;
    RT(cudaMalloc(&x.s,nb*sizeof(unsigned)));
    RT(cudaMalloc(&x.a,nb*sizeof(unsigned long long)));
    RT(cudaMalloc(&x.b,nb*sizeof(unsigned long long))); return x; }
static void get(Buf&x, std::vector<unsigned>&s, std::vector<unsigned long long>&a,
                std::vector<unsigned long long>&b){
    s.resize(x.nb); a.resize(x.nb); b.resize(x.nb);
    RT(cudaMemcpy(s.data(),x.s,x.nb*sizeof(unsigned),cudaMemcpyDeviceToHost));
    RT(cudaMemcpy(a.data(),x.a,x.nb*sizeof(unsigned long long),cudaMemcpyDeviceToHost));
    RT(cudaMemcpy(b.data(),x.b,x.nb*sizeof(unsigned long long),cudaMemcpyDeviceToHost)); }

int main(int argc,char**argv)
{
    size_t N=60ull*1000*1000; int v_reps=(argc>1)?atoi(argv[1]):60;
    int c_reps=(argc>2)?atoi(argv[2]):11000000;
    cudaDeviceProp p; RT(cudaGetDeviceProperties(&p,0));
    int NSM=p.multiProcessorCount;
    float *x,*y,*z; RT(cudaMalloc(&x,N*sizeof(float))); RT(cudaMalloc(&y,N*sizeof(float)));
    RT(cudaMalloc(&z,NSM*1536*sizeof(float)));
    RT(cudaMemset(x,1,N*sizeof(float))); RT(cudaMemset(z,1,NSM*1536*sizeof(float)));
    cudaStream_t sv,sc;
    RT(cudaStreamCreateWithFlags(&sv,cudaStreamNonBlocking));
    RT(cudaStreamCreateWithFlags(&sc,cudaStreamNonBlocking));

    printf("%s SM=%d threads/SM=%d  (每 SM 4 个 sub-partition, 共 48 warp slot)\n\n",
           p.name, NSM, p.maxThreadsPerMultiProcessor);
    printf("%-9s %-9s %-7s %-7s %-10s %-10s\n","v_block","c_block","v_warp","c_warp","真共驻SM","合计ms");
    int vbs[]={512,768,1024};
    int cbs[]={96,128,160,192,224,256,288};
    for(int vb:vbs) for(int cb:cbs){
        int v_nb=NSM, c_nb=NSM*2;
        Buf V=mk(v_nb), C=mk(c_nb);
        auto lv=[&]{ mem_k<<<v_nb,vb,0,sv>>>(x,y,N,v_reps,V.s,V.a,V.b); };
        auto lc=[&]{ cmp_k<<<c_nb,cb,0,sc>>>(z,c_reps,C.s,C.a,C.b); };
        lv(); RT(cudaStreamSynchronize(sv)); lc(); RT(cudaStreamSynchronize(sc));
        { std::thread ta([&]{lv(); cudaStreamSynchronize(sv);});
          std::this_thread::sleep_for(std::chrono::milliseconds(6));
          std::thread tb([&]{lc(); cudaStreamSynchronize(sc);});
          ta.join(); tb.join(); }
        std::vector<unsigned> vs,cs; std::vector<unsigned long long> va,vb2,ca,cb2;
        get(V,vs,va,vb2); get(C,cs,ca,cb2);
        std::map<unsigned,std::vector<std::pair<unsigned long long,unsigned long long>>> iv,ic;
        for(int i=0;i<v_nb;i++) iv[vs[i]].push_back({va[i],vb2[i]});
        for(int i=0;i<c_nb;i++) ic[cs[i]].push_back({ca[i],cb2[i]});
        int cores=0;
        for(auto&kv:iv){ if(!ic.count(kv.first)) continue;
            bool ov=false;
            for(auto&q1:kv.second) for(auto&q2:ic[kv.first])
                if(q1.first<q2.second && q2.first<q1.second){ov=true;break;}
            if(ov) cores++; }
        auto lo=std::min(*std::min_element(va.begin(),va.end()),*std::min_element(ca.begin(),ca.end()));
        auto hi=std::max(*std::max_element(vb2.begin(),vb2.end()),*std::max_element(cb2.begin(),cb2.end()));
        printf("%-9d %-9d %-7d %-7d %-10d %-10.1f\n",vb,cb,vb/32,cb/32,cores,(hi-lo)/1e6);
        cudaFree(V.s);cudaFree(V.a);cudaFree(V.b);cudaFree(C.s);cudaFree(C.a);cudaFree(C.b);
    }
    return 0;
}
