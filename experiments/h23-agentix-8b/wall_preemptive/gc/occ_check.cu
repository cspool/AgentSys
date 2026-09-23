#include <cstdio>
#include <cuda_runtime.h>
__global__ void mem_k(const float*x,float*y,size_t n,int r,unsigned*s,unsigned long long*a,unsigned long long*b){
    float v=x[0]; for(int i=0;i<r;i++) v=v*1.000001f+1e-6f; y[0]=v; }
__global__ void cmp_k(float*z,int r,unsigned*s,unsigned long long*a,unsigned long long*b){
    float v=z[0]; for(int i=0;i<r;i++) v=v*1.000001f+1e-6f; z[0]=v; }
int main(){
    cudaDeviceProp p; cudaGetDeviceProperties(&p,0);
    printf("threads/SM=%d  maxBlocks/SM=%d  regs/SM=%d\n\n",
           p.maxThreadsPerMultiProcessor, p.maxBlocksPerMultiProcessor, p.regsPerMultiprocessor);
    printf("%-8s %-14s %-14s %-12s\n","blockDim","mem_k块/SM","cmp_k块/SM","线程占用");
    for(int bs:{32,64,96,128,160,192,224,256,288,384,448,480,512,576,640,768,1024}){
        int nm=0,nc=0;
        cudaOccupancyMaxActiveBlocksPerMultiprocessor(&nm,(void*)mem_k,bs,0);
        cudaOccupancyMaxActiveBlocksPerMultiprocessor(&nc,(void*)cmp_k,bs,0);
        printf("%-8d %-14d %-14d %d/%d\n",bs,nm,nc,nm*bs,p.maxThreadsPerMultiProcessor);
    }
    return 0;
}
