#pragma once

#include <stdint.h>

#include "rocc.h"

#define AGENTSYS_FUNCT_CONFIG 0
#define AGENTSYS_FUNCT_LAUNCH 1
#define AGENTSYS_FUNCT_WAIT 2
#define AGENTSYS_FUNCT_STATUS 3
#define AGENTSYS_FUNCT_CANCEL 4
#define AGENTSYS_FUNCT_PREFETCH 5
#define AGENTSYS_FUNCT_CLEAR 6

static inline void agentsys_fence(void) { asm volatile("fence" ::: "memory"); }

static inline uint64_t agentsys_read_cycle(void) {
  uint64_t value;
  asm volatile("rdcycle %0" : "=r"(value));
  return value;
}

static inline void agentsys_config(uint8_t target, uint8_t index, uint64_t value) {
  uint64_t address = ((uint64_t)target << 8) | index;
  ROCC_INSTRUCTION_SS(0, value, address, AGENTSYS_FUNCT_CONFIG);
}

static inline void agentsys_launch(const void *input, void *output) {
  agentsys_fence();
  ROCC_INSTRUCTION_SS(0, (uintptr_t)input, (uintptr_t)output, AGENTSYS_FUNCT_LAUNCH);
}

static inline uint64_t agentsys_wait(void) {
  uint64_t status;
  ROCC_INSTRUCTION_DSS(0, status, 0, 0, AGENTSYS_FUNCT_WAIT);
  agentsys_fence();
  return status;
}

static inline uint64_t agentsys_status(uint8_t index) {
  uint64_t value;
  ROCC_INSTRUCTION_DSS(0, value, index, 0, AGENTSYS_FUNCT_STATUS);
  return value;
}

static inline uint64_t agentsys_cancel(uint8_t task_mask) {
  uint64_t accepted;
  ROCC_INSTRUCTION_DSS(0, accepted, task_mask, 0, AGENTSYS_FUNCT_CANCEL);
  return accepted;
}

static inline uint64_t agentsys_prefetch(uint8_t descriptor_index) {
  uint64_t accepted;
  ROCC_INSTRUCTION_DSS(0, accepted, descriptor_index, 0, AGENTSYS_FUNCT_PREFETCH);
  return accepted;
}

static inline void agentsys_clear(void) {
  ROCC_INSTRUCTION_SS(0, 0, 0, AGENTSYS_FUNCT_CLEAR);
}

