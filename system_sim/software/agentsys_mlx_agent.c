#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

#include "mlx_runtime.h"

#ifndef AGENTSYS_MLX_AGENT_HEADER
#error "AGENTSYS_MLX_AGENT_HEADER must name the generated Agent call header"
#endif
#include AGENTSYS_MLX_AGENT_HEADER

#ifndef MLX_WORKLOAD_HEADER
#error "MLX_WORKLOAD_HEADER must name the generated MLX spatial template"
#endif
#include MLX_WORKLOAD_HEADER

#define AGENTSYS_MLX_ABI_MAGIC UINT64_C(0x4d4c5801)

static uint64_t mlx_output[MLX_OUTPUT_VECTORS][8] __attribute__((aligned(64)));

static uint64_t mix_checksum(uint64_t checksum, uint64_t value) {
  checksum ^= value + UINT64_C(0x9e3779b97f4a7c15) + (checksum << 6) +
              (checksum >> 2);
  return checksum;
}

static uint64_t execute_tool(const agentsys_mlx_call_t *call) {
  uint64_t value = UINT64_C(0xcbf29ce484222325) ^ call->index;
  uint32_t iteration;
  for (iteration = 0; iteration < call->tool_cycles; ++iteration)
    value = (value ^ (iteration + call->priority + 1u)) *
            UINT64_C(0x100000001b3);
  return value;
}

static void configure_mlx(void) {
  unsigned index;
  for (index = 0; index < MLX_PROGRAM_ENTRIES; ++index)
    mlx_config(mlx_program[index].pe, mlx_program[index].index,
               mlx_program[index].word);
  for (index = 0; index < 16; ++index)
    mlx_config(16, index, mlx_instruction_counts[index]);
  mlx_config(31, 0, MLX_INPUT_VECTORS);
  mlx_config(31, 1, MLX_OUTPUT_VECTORS);
  mlx_config(31, 2, MLX_OUTPUT_SPM_BASE);
}

static unsigned check_output(uint64_t *checksum) {
  unsigned vector;
  unsigned beat;
  unsigned mismatches = 0;
  for (vector = 0; vector < MLX_OUTPUT_VECTORS; ++vector) {
    for (beat = 0; beat < 8; ++beat) {
      *checksum = mix_checksum(*checksum, mlx_output[vector][beat]);
      if (mlx_output[vector][beat] != mlx_golden[vector][beat])
        ++mismatches;
    }
  }
  return mismatches;
}

int main(void) {
  uint64_t completed_mask = 0;
  uint64_t aggregate_checksum = AGENTSYS_MLX_WORKLOAD_DIGEST;
  uint64_t total_host_config = 0;
  uint64_t total_host_launch_wait = 0;
  uint64_t total_system = 0;
  uint64_t total_dma = 0;
  uint64_t total_kernel = 0;
  uint64_t total_instructions = 0;
  uint64_t total_load = 0;
  uint64_t total_store = 0;
  uint64_t total_compute = 0;
  uint64_t total_xfer = 0;
  uint64_t total_stall = 0;
  uint64_t total_hops = 0;
  uint64_t total_conflicts = 0;
  uint64_t total_dma_bytes = 0;
  unsigned dependency_violations = 0;
  unsigned mismatches = 0;
  unsigned launches = 0;
  unsigned tools = 0;
  unsigned index;
  const char *backend_name = "none";

  for (index = 0; index < AGENTSYS_MLX_CALLS; ++index) {
    const agentsys_mlx_call_t *call = &agentsys_mlx_calls[index];
    if ((completed_mask & call->deps_mask) != call->deps_mask) {
      ++dependency_violations;
      printf("AGENTSYS_MLX_DEPENDENCY_FAIL index=%u call=%s deps=%016" PRIx64
             " complete=%016" PRIx64 "\n",
             index, call->call_id, call->deps_mask, completed_mask);
      continue;
    }
    printf("AGENTSYS_MLX_CALL_START index=%u call=%s program=%s kind=%s"
           " priority=%u flow=%u chunk=%u batch=%u deps=%016" PRIx64 "\n",
           index, call->call_id, call->program_id,
           call->kind ? "tool" : "llm", call->priority, call->flow_code,
           call->prefill_chunk_tokens, call->decode_batch_cap, call->deps_mask);
    if (call->kind) {
      uint64_t start = mlx_read_cycle();
      uint64_t tool_checksum = execute_tool(call);
      uint64_t end = mlx_read_cycle();
      aggregate_checksum = mix_checksum(aggregate_checksum, tool_checksum);
      ++tools;
      printf("AGENTSYS_MLX_CALL index=%u call=%s program=%s kind=tool"
             " cpu_cycles=%" PRIu64 " checksum=%016" PRIx64 " first=%u last=%u\n",
             index, call->call_id, call->program_id, end - start, tool_checksum,
             call->program_first, call->program_last);
    } else {
      uint64_t status[15];
      uint64_t config_start;
      uint64_t config_end;
      uint64_t launch_start;
      uint64_t launch_end;
      uint64_t call_checksum = call->index + 1u;
      uint64_t wait_status;
      unsigned vector;
      unsigned beat;
      unsigned status_index;

      for (vector = 0; vector < MLX_OUTPUT_VECTORS; ++vector)
        for (beat = 0; beat < 8; ++beat)
          mlx_output[vector][beat] = UINT64_C(0xdeadbeefdeadbeef);

      config_start = mlx_read_cycle();
      configure_mlx();
      config_end = mlx_read_cycle();
      launch_start = mlx_read_cycle();
      mlx_launch(mlx_input, mlx_output);
      wait_status = mlx_wait();
      launch_end = mlx_read_cycle();
      for (status_index = 0; status_index < 15; ++status_index)
        status[status_index] = mlx_status(status_index);
      mismatches += check_output(&call_checksum);
      if (status[14] != AGENTSYS_MLX_ABI_MAGIC)
        ++mismatches;
      backend_name = (status[0] & 8) ? "rtl" : "cycle";
      aggregate_checksum = mix_checksum(aggregate_checksum, call_checksum);
      total_host_config += config_end - config_start;
      total_host_launch_wait += launch_end - launch_start;
      total_system += status[1];
      total_dma += status[3];
      total_kernel += status[4];
      total_instructions += status[5];
      total_load += status[6];
      total_store += status[7];
      total_compute += status[8];
      total_xfer += status[9];
      total_stall += status[10];
      total_hops += status[11];
      total_conflicts += status[12];
      total_dma_bytes += status[13];
      ++launches;
      printf("AGENTSYS_MLX_CALL index=%u call=%s program=%s kind=llm backend=%s"
             " wait=%" PRIu64 " host_config=%" PRIu64
             " host_launch_wait=%" PRIu64 " system=%" PRIu64
             " dma=%" PRIu64 " kernel=%" PRIu64 " instructions=%" PRIu64
             " load=%" PRIu64 " store=%" PRIu64 " compute=%" PRIu64
             " xfer=%" PRIu64 " stall=%" PRIu64 " hops=%" PRIu64
             " conflicts=%" PRIu64 " dma_bytes=%" PRIu64
             " abi=%08" PRIx64 " checksum=%016" PRIx64
             " mismatches=%u first=%u last=%u\n",
             index, call->call_id, call->program_id, backend_name, wait_status,
             config_end - config_start, launch_end - launch_start, status[1],
             status[3], status[4], status[5], status[6], status[7], status[8],
             status[9], status[10], status[11], status[12], status[13],
             status[14], call_checksum, mismatches, call->program_first,
             call->program_last);
    }
    completed_mask |= UINT64_C(1) << call->index;
  }

  printf("AGENTSYS_MLX_%s workload=%s backend=%s programs=%u calls=%u"
         " llm_calls=%u tool_calls=%u launches=%u dependencies=%u"
         " completed=%016" PRIx64 " host_config=%" PRIu64
         " host_launch_wait=%" PRIu64 " system=%" PRIu64 " dma=%" PRIu64
         " kernel=%" PRIu64 " instructions=%" PRIu64 " load=%" PRIu64
         " store=%" PRIu64 " compute=%" PRIu64 " xfer=%" PRIu64
         " stall=%" PRIu64 " hops=%" PRIu64 " conflicts=%" PRIu64
         " dma_bytes=%" PRIu64 " checksum=%016" PRIx64
         " app_digest=%016" PRIx64 " mir_digest=%016" PRIx64
         " workload_digest=%016" PRIx64 " mismatches=%u\n",
         (mismatches == 0 && dependency_violations == 0 &&
          completed_mask == AGENTSYS_MLX_EXPECT_COMPLETED_MASK)
             ? "PASS"
             : "FAIL",
         AGENTSYS_MLX_WORKLOAD_NAME, backend_name, AGENTSYS_MLX_PROGRAMS,
         AGENTSYS_MLX_CALLS, AGENTSYS_MLX_EXPECT_LLM_CALLS,
         AGENTSYS_MLX_EXPECT_TOOL_CALLS, launches, dependency_violations,
         completed_mask, total_host_config, total_host_launch_wait, total_system,
         total_dma, total_kernel, total_instructions, total_load, total_store,
         total_compute, total_xfer, total_stall, total_hops, total_conflicts,
         total_dma_bytes, aggregate_checksum, AGENTSYS_MLX_APP_DIGEST,
         AGENTSYS_MLX_MIR_DIGEST, AGENTSYS_MLX_WORKLOAD_DIGEST, mismatches);
  return (mismatches == 0 && dependency_violations == 0 &&
          completed_mask == AGENTSYS_MLX_EXPECT_COMPLETED_MASK)
             ? 0
             : 1;
}
