#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

#include "mlx_runtime.h"

#ifndef MLX_WORKLOAD_HEADER
#error "MLX_WORKLOAD_HEADER must name a generated workload header"
#endif
#include MLX_WORKLOAD_HEADER

#define AGENTSYS_MLX_ABI_MAGIC UINT64_C(0x4d4c5801)

static uint64_t mlx_output[MLX_OUTPUT_VECTORS][8] __attribute__((aligned(64)));

int main(void) {
  uint64_t config_start;
  uint64_t config_end;
  uint64_t total_start;
  uint64_t total_end;
  uint64_t wait_status;
  uint64_t status[15];
  unsigned index;
  unsigned beat;
  unsigned mismatches = 0;

  for (index = 0; index < MLX_OUTPUT_VECTORS; ++index)
    for (beat = 0; beat < 8; ++beat)
      mlx_output[index][beat] = UINT64_C(0xdeadbeefdeadbeef);

  config_start = mlx_read_cycle();
  for (index = 0; index < MLX_PROGRAM_ENTRIES; ++index)
    mlx_config(mlx_program[index].pe, mlx_program[index].index,
               mlx_program[index].word);
  for (index = 0; index < 16; ++index)
    mlx_config(16, index, mlx_instruction_counts[index]);
  mlx_config(31, 0, MLX_INPUT_VECTORS);
  mlx_config(31, 1, MLX_OUTPUT_VECTORS);
  mlx_config(31, 2, MLX_OUTPUT_SPM_BASE);
  config_end = mlx_read_cycle();

  total_start = mlx_read_cycle();
  mlx_launch(mlx_input, mlx_output);
  wait_status = mlx_wait();
  total_end = mlx_read_cycle();

  for (index = 0; index < 15; ++index)
    status[index] = mlx_status(index);
  if (status[14] != AGENTSYS_MLX_ABI_MAGIC)
    ++mismatches;
  for (index = 0; index < MLX_OUTPUT_VECTORS; ++index) {
    for (beat = 0; beat < 8; ++beat) {
      if (mlx_output[index][beat] != mlx_golden[index][beat])
        ++mismatches;
    }
  }

  printf("AGENTSYS_MLX_SMOKE_%s workload=%s backend=%s wait=%" PRIu64
         " host_config=%" PRIu64 " host_launch_wait=%" PRIu64
         " system=%" PRIu64 " dma=%" PRIu64 " kernel=%" PRIu64
         " instructions=%" PRIu64 " load=%" PRIu64 " store=%" PRIu64
         " compute=%" PRIu64 " xfer=%" PRIu64 " sync_stall=%" PRIu64
         " hops=%" PRIu64 " conflicts=%" PRIu64 " dma_bytes=%" PRIu64
         " abi=%08" PRIx64 " mismatches=%u\n",
         mismatches == 0 ? "PASS" : "FAIL", MLX_WORKLOAD_NAME,
         (status[0] & 8) ? "rtl" : "cycle", wait_status,
         config_end - config_start, total_end - total_start, status[1], status[3],
         status[4], status[5], status[6], status[7], status[8], status[9],
         status[10], status[11], status[12], status[13], status[14], mismatches);
  return mismatches == 0 ? 0 : 1;
}
