// bmap_probe.cu -- 共驻边界的二维图谱
// 两侧用**完全相同**的 spin kernel(消掉寄存器/指令/访存差异), 只变 blockDim 与 grid。
// 受害者先发射并进入稳态, 抢占者后注入; 逐 SM 求跨 kernel 的区间重叠。
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <map>
#include <algorithm>
#include <thread>
#include <chrono>
#include <cuda_runtime.h>
#define RT(x) do{cudaError_t e=(x); if(e!=cudaSuccess){fprintf(stderr,"[RT]%s:%d %s\n",__FILE__,__LINE__,cudaGetErrorString(e));exit(1);}}while(0)

__global__ void spin_k(unsigned* smid, unsigned long long* t0, unsigned long long* t1,
                       unsigned long long ns)
{
    unsigned s; asm volatile("mov.u32 %0, %%smid;" : "=r"(s));
    unsigned long long a; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(a));
    if (threadIdx.x == 0) { smid[blockIdx.x] = s; t0[blockIdx.x] = a; }
    unsigned long long b = a;
    while (b - a < ns) { asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(b)); }
    if (threadIdx.x == 0) t1[blockIdx.x] = b;
}

struct B { unsigned* s; unsigned long long *a,*b; int nb; };
static B mk(int nb){ B x{}; x.nb=nb;
    RT(cudaMalloc(&x.s,nb*sizeof(unsigned)));
    RT(cudaMalloc(&x.a,nb*sizeof(unsigned long long)));
    RT(cudaMalloc(&x.b,nb*sizeof(unsigned long long))); return x; }
static void fr(B&x){ cudaFree(x.s); cudaFree(x.a); cudaFree(x.b); }

int main(int argc,char**argv)
{
    int cmul=(argc>1)?atoi(argv[1]):1;       // 抢占者 grid = NSM * cmul
    int vmul=(argc>2)?atoi(argv[2]):1;       // 受害者 grid = NSM * vmul
    cudaDeviceProp p; RT(cudaGetDeviceProperties(&p,0));
    int NSM=p.multiProcessorCount, MAXT=p.maxThreadsPerMultiProcessor;
    cudaStream_t s1,s2;
    RT(cudaStreamCreateWithFlags(&s1,cudaStreamNonBlocking));
    RT(cudaStreamCreateWithFlags(&s2,cudaStreamNonBlocking));
    int bs[]={32,64,96,128,160,192,224,256,288,320,416,448,480,512,544,640};
    int NB=sizeof(bs)/sizeof(int);
    printf("SM=%d threads/SM=%d  受害者 grid=NSM*%d  抢占者 grid=NSM*%d\n",NSM,MAXT,vmul,cmul);
    printf("行=受害者 blockDim, 列=抢占者 blockDim;  #=共驻(>=64 SM)  .=不共驻  x=容量不足(v*vmul+c>%d)\n\n",MAXT);
    printf("%6s","v\\c");
    for(int j=0;j<NB;j++) printf("%5d",bs[j]);
    printf("\n");
    for(int i=0;i<NB;i++){
        int vb=bs[i];
        if(vb*vmul>MAXT){ continue; }
        printf("%6d",vb);
        for(int j=0;j<NB;j++){
            int cb=bs[j];
            if(vb*vmul+cb>MAXT){ printf("%5s","x"); continue; }
            B V=mk(NSM*vmul), C=mk(NSM*cmul);
            auto lv=[&]{ spin_k<<<NSM*vmul,vb,0,s1>>>(V.s,V.a,V.b,25000000ull); };
            auto lc=[&]{ spin_k<<<NSM*cmul,cb,0,s2>>>(C.s,C.a,C.b,10000000ull); };
            lv(); RT(cudaStreamSynchronize(s1)); lc(); RT(cudaStreamSynchronize(s2));
            { std::thread ta([&]{lv(); cudaStreamSynchronize(s1);});
              std::this_thread::sleep_for(std::chrono::milliseconds(5));
              std::thread tb([&]{lc(); cudaStreamSynchronize(s2);});
              ta.join(); tb.join(); }
            std::vector<unsigned> vs(V.nb),cs(C.nb);
            std::vector<unsigned long long> va(V.nb),vb2(V.nb),ca(C.nb),cb2(C.nb);
            RT(cudaMemcpy(vs.data(),V.s,V.nb*4,cudaMemcpyDeviceToHost));
            RT(cudaMemcpy(va.data(),V.a,V.nb*8,cudaMemcpyDeviceToHost));
            RT(cudaMemcpy(vb2.data(),V.b,V.nb*8,cudaMemcpyDeviceToHost));
            RT(cudaMemcpy(cs.data(),C.s,C.nb*4,cudaMemcpyDeviceToHost));
            RT(cudaMemcpy(ca.data(),C.a,C.nb*8,cudaMemcpyDeviceToHost));
            RT(cudaMemcpy(cb2.data(),C.b,C.nb*8,cudaMemcpyDeviceToHost));
            std::map<unsigned,std::vector<std::pair<unsigned long long,unsigned long long>>> iv,ic;
            for(int k=0;k<V.nb;k++) iv[vs[k]].push_back({va[k],vb2[k]});
            for(int k=0;k<C.nb;k++) ic[cs[k]].push_back({ca[k],cb2[k]});
            int co=0;
            for(auto&kv:iv){ if(!ic.count(kv.first)) continue; bool o=false;
                for(auto&q1:kv.second) for(auto&q2:ic[kv.first])
                    if(q1.first<q2.second&&q2.first<q1.second){o=true;break;}
                if(o) co++; }
            printf("%5s", co>=NSM/2 ? "#" : ".");
            fflush(stdout); fr(V); fr(C);
        }
        printf("\n");
    }
    return 0;
}
