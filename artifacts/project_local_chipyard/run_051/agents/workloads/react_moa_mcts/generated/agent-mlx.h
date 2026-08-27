#pragma once

#include <stdint.h>

#define AGENTSYS_MLX_WORKLOAD_NAME "react_moa_mcts"
#define AGENTSYS_MLX_WORKLOAD_DIGEST UINT64_C(0x9239befff9e01643)
#define AGENTSYS_MLX_APP_DIGEST UINT64_C(0x4347e5adb9552f70)
#define AGENTSYS_MLX_MIR_DIGEST UINT64_C(0x2ce653ac177a8ee5)
#define AGENTSYS_MLX_PROGRAMS 3u
#define AGENTSYS_MLX_CALLS 11u
#define AGENTSYS_MLX_EXPECT_LLM_CALLS 10u
#define AGENTSYS_MLX_EXPECT_TOOL_CALLS 1u
#define AGENTSYS_MLX_EXPECT_COMPLETED_MASK UINT64_C(0x00000000000007ff)

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
    "react-plan", "react",
    0, 0, 0,
    1, 0, 0,
    16, 3,
    213, 78, 0,
    UINT64_C(0x0000000000000000)
  },
  {
    "moa-map0", "moa",
    1, 0, 2,
    1, 0, 1,
    16, 16,
    451, 90, 0,
    UINT64_C(0x0000000000000000)
  },
  {
    "moa-map1", "moa",
    2, 0, 2,
    0, 0, 1,
    16, 16,
    467, 96, 0,
    UINT64_C(0x0000000000000000)
  },
  {
    "moa-map2", "moa",
    3, 0, 2,
    0, 0, 1,
    16, 16,
    483, 87, 0,
    UINT64_C(0x0000000000000000)
  },
  {
    "mcts-root", "mcts",
    4, 0, 2,
    1, 0, 1,
    16, 16,
    515, 85, 0,
    UINT64_C(0x0000000000000000)
  },
  {
    "react-tool", "react",
    5, 1, 0,
    0, 0, 0,
    16, 3,
    253, 72, 256,
    UINT64_C(0x0000000000000001)
  },
  {
    "react-answer", "react",
    6, 0, 0,
    0, 1, 0,
    16, 3,
    261, 76, 0,
    UINT64_C(0x0000000000000020)
  },
  {
    "mcts-actor0", "mcts",
    7, 0, 2,
    0, 0, 1,
    16, 16,
    551, 89, 0,
    UINT64_C(0x0000000000000010)
  },
  {
    "mcts-actor1", "mcts",
    8, 0, 2,
    0, 0, 1,
    16, 16,
    563, 81, 0,
    UINT64_C(0x0000000000000010)
  },
  {
    "moa-reduce", "moa",
    9, 0, 2,
    0, 1, 1,
    16, 16,
    579, 93, 0,
    UINT64_C(0x000000000000000e)
  },
  {
    "mcts-critic", "mcts",
    10, 0, 2,
    0, 1, 1,
    16, 16,
    587, 85, 0,
    UINT64_C(0x0000000000000180)
  },
};
