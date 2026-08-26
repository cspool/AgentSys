#pragma once

#include <stdint.h>

#include "rocc.h"

// Neutral ordinary-RISC-V <-> XPU command ABI. There are deliberately no
// accelerator-task, cancel, or prefetch instructions in this interface.
#define AGENTSYS_XPU_FUNCT_CONFIG 0
#define AGENTSYS_XPU_FUNCT_LAUNCH 1
#define AGENTSYS_XPU_FUNCT_WAIT 2
#define AGENTSYS_XPU_FUNCT_STATUS 3
#define AGENTSYS_XPU_FUNCT_CLEAR 4

static inline void agentsys_xpu_fence(void) { asm volatile("fence" ::: "memory"); }

static inline uint64_t agentsys_xpu_read_cycle(void) {
  uint64_t value;
  asm volatile("rdcycle %0" : "=r"(value));
  return value;
}

static inline void agentsys_xpu_config(uint8_t target, uint8_t index,
                                       uint64_t value) {
  uint64_t address = ((uint64_t)target << 8) | index;
  ROCC_INSTRUCTION_SS(0, value, address, AGENTSYS_XPU_FUNCT_CONFIG);
}

static inline void agentsys_xpu_launch(const void *input, void *output) {
  agentsys_xpu_fence();
  ROCC_INSTRUCTION_SS(0, (uintptr_t)input, (uintptr_t)output,
                      AGENTSYS_XPU_FUNCT_LAUNCH);
}

static inline uint64_t agentsys_xpu_wait(void) {
  uint64_t status;
  ROCC_INSTRUCTION_DSS(0, status, 0, 0, AGENTSYS_XPU_FUNCT_WAIT);
  agentsys_xpu_fence();
  return status;
}

static inline uint64_t agentsys_xpu_status(uint8_t index) {
  uint64_t value;
  ROCC_INSTRUCTION_DSS(0, value, index, 0, AGENTSYS_XPU_FUNCT_STATUS);
  return value;
}

static inline void agentsys_xpu_clear(void) {
  ROCC_INSTRUCTION_SS(0, 0, 0, AGENTSYS_XPU_FUNCT_CLEAR);
}
