#pragma once

#include <stdint.h>

#define AGENTSYS_MLX_WORKLOAD_NAME "planner_debate"
#define AGENTSYS_MLX_WORKLOAD_DIGEST UINT64_C(0x0fbd066467fc5205)
#define AGENTSYS_MLX_APP_DIGEST UINT64_C(0xd9d843ddd613dcd0)
#define AGENTSYS_MLX_MIR_DIGEST UINT64_C(0x2ce653ac177a8ee5)
#define AGENTSYS_MLX_PROGRAMS 2u
#define AGENTSYS_MLX_CALLS 6u
#define AGENTSYS_MLX_EXPECT_LLM_CALLS 5u
#define AGENTSYS_MLX_EXPECT_TOOL_CALLS 1u
#define AGENTSYS_MLX_EXPECT_COMPLETED_MASK UINT64_C(0x000000000000003f)

typedef struct {
  const char *call_id;
  const char *program_id;
  uint8_t index;
  uint8_t kind; /* 0=LLM/MLX, 1=CPU tool */
  uint8_t priority;
  uint8_t program_first;
  uint8_t program_last;
  uint8_t flow_code;
  uint8_t prefill_chunk_tokens;
  uint8_t decode_batch_cap;
  uint16_t input_tokens;
  uint16_t output_tokens;
  uint16_t tool_cycles;
  uint64_t deps_mask;
} agentsys_mlx_call_t;

static const agentsys_mlx_call_t agentsys_mlx_calls[AGENTSYS_MLX_CALLS] = {
  {
    "planner-seed", "planner",
    0, 0, 0,
    1, 0, 0,
    32, 2,
    320, 72, 0,
    UINT64_C(0x0000000000000000)
  },
  {
    "critic-a", "debate",
    1, 0, 2,
    1, 0, 1,
    32, 8,
    512, 80, 0,
    UINT64_C(0x0000000000000000)
  },
  {
    "critic-b", "debate",
    2, 0, 2,
    0, 0, 1,
    32, 8,
    448, 88, 0,
    UINT64_C(0x0000000000000000)
  },
  {
    "planner-tool", "planner",
    3, 1, 0,
    0, 0, 0,
    32, 2,
    48, 16, 192,
    UINT64_C(0x0000000000000001)
  },
  {
    "planner-final", "planner",
    4, 0, 0,
    0, 1, 0,
    32, 2,
    384, 96, 0,
    UINT64_C(0x0000000000000008)
  },
  {
    "critic-merge", "debate",
    5, 0, 2,
    0, 1, 1,
    32, 8,
    640, 104, 0,
    UINT64_C(0x0000000000000007)
  },
};
