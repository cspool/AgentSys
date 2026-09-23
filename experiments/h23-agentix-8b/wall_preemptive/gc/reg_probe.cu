// reg_probe.cu -- 阶梯是线程几何决定的, 还是占用率(寄存器)决定的?
// 固定 blockDim, 只抬受害者的寄存器压力使其理论占用率下降, 看 c_min 是否移动。
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <map>
#include <thread>
#include <chrono>
#include <cuda_runtime.h>
#define RT(x) do{cudaError_t e=(x); if(e!=cudaSuccess){fprintf(stderr,"[RT]%s:%d %s\n",__FILE__,__LINE__,cudaGetErrorString(e));exit(1);}}while(0)

template<int R>
__global__ void spin_r(unsigned* smid, unsigned long long* t0, unsigned long long* t1,
                       unsigned long long ns, float* sink)
{
    unsigned s; asm volatile("mov.u32 %0, %%smid;" : "=r"(s));
    unsigned long long a; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(a));
    if (threadIdx.x == 0) { smid[blockIdx.x] = s; t0[blockIdx.x] = a; }
    float acc[R];
    #pragma unroll
    for (int i = 0; i < R; i++) acc[i] = (float)(threadIdx.x + i);
    unsigned long long b = a;
    while (b - a < ns) {
        #pragma unroll
        for (int i = 0; i < R; i++) acc[i] = acc[i]*1.000001f + 1e-6f;
        asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(b));
    }
    float sum = 0;
    #pragma unroll
    for (int i = 0; i < R; i++) sum += acc[i];
    if (threadIdx.x == 0) { t1[blockIdx.x] = b; sink[blockIdx.x] = sum; }
}
__global__ void spin_c(unsigned* smid, unsigned long long* t0, unsigned long long* t1,
                       unsigned long long ns)
{
    unsigned s; asm volatile("mov.u32 %0, %%smid;" : "=r"(s));
    unsigned long long a; asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(a));
    if (threadIdx.x == 0) { smid[blockIdx.x] = s; t0[blockIdx.x] = a; }
    unsigned long long b = a;
    while (b - a < ns) { asm volatile("mov.u64 %0, %%globaltimer;" : "=l"(b)); }
    if (threadIdx.x == 0) t1[blockIdx.x] = b;
}

template<int R>
void row(int NSM,int vb,cudaStream_t s1,cudaStream_t s2,float* sink){
    int nm=0; cudaOccupancyMaxActiveBlocksPerMultiprocessor(&nm,(void*)spin_r<R>,vb,0);
    cudaFuncAttributes fa; cudaFuncGetAttributes(&fa,(void*)spin_r<R>);
    printf("R=%-3d v_block=%-5d 寄存器=%-3d 理论块/SM=%-2d  c_min: ",R,vb,fa.numRegs,nm);
    int cs[]={32,64,96,128,160,192,224,256};
    int found=0;
    for(int cb:cs){
        if(found) break;
        unsigned *vs,*css; unsigned long long *va,*vb2,*ca,*cb2;
        RT(cudaMalloc(&vs,NSM*4)); RT(cudaMalloc(&va,NSM*8)); RT(cudaMalloc(&vb2,NSM*8));
        RT(cudaMalloc(&css,NSM*4)); RT(cudaMalloc(&ca,NSM*8)); RT(cudaMalloc(&cb2,NSM*8));
        auto lv=[&]{ spin_r<R><<<NSM,vb,0,s1>>>(vs,va,vb2,25000000ull,sink); };
        auto lc=[&]{ spin_c<<<NSM,cb,0,s2>>>(css,ca,cb2,10000000ull); };
        lv(); cudaStreamSynchronize(s1); lc(); cudaStreamSynchronize(s2);
        { std::thread ta([&]{lv(); cudaStreamSynchronize(s1);});
          std::this_thread::sleep_for(std::chrono::milliseconds(5));
          std::thread tb([&]{lc(); cudaStreamSynchronize(s2);});
          ta.join(); tb.join(); }
        std::vector<unsigned> hv(NSM),hc(NSM);
        std::vector<unsigned long long> ha(NSM),hb(NSM),hca(NSM),hcb(NSM);
        cudaMemcpy(hv.data(),vs,NSM*4,cudaMemcpyDeviceToHost);
        cudaMemcpy(ha.data(),va,NSM*8,cudaMemcpyDeviceToHost);
        cudaMemcpy(hb.data(),vb2,NSM*8,cudaMemcpyDeviceToHost);
        cudaMemcpy(hc.data(),css,NSM*4,cudaMemcpyDeviceToHost);
        cudaMemcpy(hca.data(),ca,NSM*8,cudaMemcpyDeviceToHost);
        cudaMemcpy(hcb.data(),cb2,NSM*8,cudaMemcpyDeviceToHost);
        std::map<unsigned,std::pair<unsigned long long,unsigned long long>> mv;
        for(int k=0;k<NSM;k++) mv[hv[k]]={ha[k],hb[k]};
        int co=0;
        for(int k=0;k<NSM;k++){ auto it=mv.find(hc[k]); if(it==mv.end()) continue;
            if(it->second.first<hcb[k] && hca[k]<it->second.second) co++; }
        if(co>=NSM/2){ printf("%d\n",cb); found=1; }
        cudaFree(vs);cudaFree(va);cudaFree(vb2);cudaFree(css);cudaFree(ca);cudaFree(cb2);
    }
    if(!found) printf(">256\n");
}
int main(){
    cudaDeviceProp p; RT(cudaGetDeviceProperties(&p,0));
    int NSM=p.multiProcessorCount;
    float* sink; RT(cudaMalloc(&sink,NSM*4));
    cudaStream_t s1,s2;
    RT(cudaStreamCreateWithFlags(&s1,cudaStreamNonBlocking));
    RT(cudaStreamCreateWithFlags(&s2,cudaStreamNonBlocking));
    printf("固定 v_block, 只抬受害者寄存器压力, 看 c_min 是否移动\n\n");
    for(int vb : {256, 512}){
        row<4>(NSM,vb,s1,s2,sink);
        row<16>(NSM,vb,s1,s2,sink);
        row<40>(NSM,vb,s1,s2,sink);
        row<80>(NSM,vb,s1,s2,sink);
        printf("\n");
    }
    return 0;
}
