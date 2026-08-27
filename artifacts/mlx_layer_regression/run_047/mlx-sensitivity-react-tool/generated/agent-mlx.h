#pragma once

#include <stdint.h>

#define AGENTSYS_MLX_WORKLOAD_NAME "react_tool"
#define AGENTSYS_MLX_WORKLOAD_DIGEST UINT64_C(0xffcc75abd7f6dc53)
#define AGENTSYS_MLX_APP_DIGEST UINT64_C(0xb071d922518ebdc9)
#define AGENTSYS_MLX_MIR_DIGEST UINT64_C(0x2ce653ac177a8ee5)
#define AGENTSYS_MLX_PROGRAMS 1u
#define AGENTSYS_MLX_CALLS 3u
#define AGENTSYS_MLX_EXPECT_LLM_CALLS 2u
#define AGENTSYS_MLX_EXPECT_TOOL_CALLS 1u
#define AGENTSYS_MLX_EXPECT_COMPLETED_MASK UINT64_C(0x0000000000000007)

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
    "plan", "assistant",
    0, 0, 0,
    1, 0, 0,
    8, 2,
    192, 48, 0,
    UINT64_C(0x0000000000000000)
  },
  {
    "lookup", "assistant",
    1, 1, 0,
    0, 0, 0,
    8, 2,
    32, 8, 128,
    UINT64_C(0x0000000000000001)
  },
  {
    "answer", "assistant",
    2, 0, 0,
    0, 1, 0,
    8, 2,
    224, 64, 0,
    UINT64_C(0x0000000000000002)
  },
};
