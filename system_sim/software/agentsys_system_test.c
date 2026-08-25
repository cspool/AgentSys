#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

#include "agentsys_runtime.h"

#define DESCRIPTORS 8
#define INPUT_BEATS 8
#define OUTPUT_BEATS 4
#define ABI_MAGIC UINT64_C(0x41545801)
#define RESULT_MAGIC UINT64_C(0x4154585f54495341)

static uint64_t agentsys_input[INPUT_BEATS] __attribute__((aligned(64))) = {
    UINT64_C(0x0123456789abcdef), UINT64_C(0xfedcba9876543210),
    UINT64_C(0x1111222233334444), UINT64_C(0x5555666677778888),
    UINT64_C(0x0f1e2d3c4b5a6978), UINT64_C(0x8877665544332211),
    UINT64_C(0x13579bdf2468ace0), UINT64_C(0xcafebabedeadbeef),
};
static uint64_t agentsys_output[OUTPUT_BEATS] __attribute__((aligned(64)));

static uint64_t control_word(uint8_t tile_id, uint8_t task_id, uint8_t deps,
                             uint8_t access, uint8_t priority, uint8_t engine,
                             uint8_t op_type, uint16_t duration,
                             uint8_t static_group) {
  return ((uint64_t)1 << 60) | ((uint64_t)static_group << 52) |
         ((uint64_t)duration << 36) | ((uint64_t)op_type << 30) |
         ((uint64_t)engine << 28) | ((uint64_t)priority << 26) |
         ((uint64_t)access << 24) | ((uint64_t)deps << 16) |
         ((uint64_t)task_id << 8) | tile_id;
}

static uint64_t tilemem_word(uint32_t base, uint16_t size, uint8_t scope,
                             uint8_t bank) {
  return ((uint64_t)bank << 50) | ((uint64_t)scope << 48) |
         ((uint64_t)(size - 1) << 32) | base;
}

int main(void) {
  uint64_t control[DESCRIPTORS];
  uint64_t tilemem[DESCRIPTORS];
  uint64_t status[28];
  uint64_t input_xor = 0;
  uint64_t control_xor = 0;
  uint64_t expected_checksum;
  uint64_t wait_status;
  uint64_t config_start;
  uint64_t config_end;
  uint64_t run_start;
  uint64_t run_end;
  uint64_t prefetch_accepted;
  unsigned errors = 0;
  unsigned index;

  // Two independent attention-like tile chains. Task 1 is reactive and its
  // first DE tile is deliberately later in program order; dynamic arbitration
  // must select it first, then overlap task 0 across engines.
  control[0] = control_word(0, 0, 0x00, 1, 2, 2, 1, 20, 0);  // DE load p
  control[1] = control_word(1, 0, 0x01, 2, 2, 0, 2, 80, 1);  // ME p
  control[2] = control_word(2, 0, 0x02, 2, 2, 1, 3, 40, 2);  // VE p
  control[3] = control_word(3, 1, 0x00, 1, 0, 2, 1, 20, 0);  // DE load r
  control[4] = control_word(4, 1, 0x08, 2, 0, 0, 2, 80, 1);  // ME r
  control[5] = control_word(5, 1, 0x10, 2, 0, 1, 3, 40, 2);  // VE r
  control[6] = control_word(6, 0, 0x04, 0, 2, 2, 4, 20, 3);  // DE store p
  control[7] = control_word(7, 1, 0x20, 0, 0, 2, 4, 20, 3);  // DE store r

  tilemem[0] = tilemem_word(0x0000, 64, 1, 0);
  tilemem[1] = tilemem_word(0x0000, 64, 1, 0);
  tilemem[2] = tilemem_word(0x0000, 64, 1, 0);
  tilemem[3] = tilemem_word(0x1000, 64, 1, 1);
  tilemem[4] = tilemem_word(0x1000, 64, 1, 1);
  tilemem[5] = tilemem_word(0x1000, 64, 1, 1);
  tilemem[6] = tilemem_word(0x0000, 64, 1, 0);
  tilemem[7] = tilemem_word(0x1000, 64, 1, 1);

  for (index = 0; index < INPUT_BEATS; ++index)
    input_xor ^= agentsys_input[index];
  for (index = 0; index < DESCRIPTORS; ++index)
    control_xor ^= control[index];
  expected_checksum = input_xor ^ control_xor ^ RESULT_MAGIC;
  for (index = 0; index < OUTPUT_BEATS; ++index)
    agentsys_output[index] = UINT64_C(0xdeadbeefdeadbeef);

  agentsys_clear();
  config_start = agentsys_read_cycle();
  for (index = 0; index < DESCRIPTORS; ++index) {
    agentsys_config(0, index, control[index]);
    agentsys_config(1, index, tilemem[index]);
  }
  agentsys_config(31, 0, DESCRIPTORS);
  agentsys_config(31, 1, INPUT_BEATS);
  agentsys_config(31, 2, OUTPUT_BEATS);
  prefetch_accepted = agentsys_prefetch(3);
  config_end = agentsys_read_cycle();

  run_start = agentsys_read_cycle();
  agentsys_launch(agentsys_input, agentsys_output);
  wait_status = agentsys_wait();
  run_end = agentsys_read_cycle();

  for (index = 0; index < 28; ++index)
    status[index] = agentsys_status(index);

  for (index = 0; index < OUTPUT_BEATS; ++index) {
    uint64_t expected = expected_checksum ^ index;
    if (agentsys_output[index] != expected) {
      ++errors;
      printf("AGENTSYS_ELF_MISMATCH beat=%u got=%016" PRIx64
             " expected=%016" PRIx64 "\n",
             index, agentsys_output[index], expected);
    }
  }
  if (status[22] != ABI_MAGIC || status[20] != expected_checksum)
    ++errors;
  if (status[5] != DESCRIPTORS || status[6] != DESCRIPTORS ||
      status[7] != DESCRIPTORS || status[8] != 0)
    ++errors;
  if (status[25] + status[26] + status[27] != status[6] ||
      status[25] != 2 || status[26] != 2 || status[27] != 4)
    ++errors;
  if (status[9] != 160 || status[10] != 80 || status[11] != 80)
    ++errors;
  if (status[17] != 1 || status[18] != 1 || prefetch_accepted != 1)
    ++errors;
  if (status[19] != (INPUT_BEATS + OUTPUT_BEATS) * 8 || status[21] != 0)
    ++errors;
  if ((status[0] & 0x08) == 0 || (status[0] & 0x02) == 0)
    ++errors;
  if ((status[0] & 0x10) && status[14] == 0)
    ++errors;

  printf("AGENTSYS_ELF_%s backend=%s wait=%" PRIu64
         " host_config=%" PRIu64 " host_launch_wait=%" PRIu64
         " system=%" PRIu64 " dma=%" PRIu64 " kernel=%" PRIu64
         " submitted=%" PRIu64 " issued=%" PRIu64
         " completed=%" PRIu64 " canceled=%" PRIu64
         " me_busy=%" PRIu64 " ve_busy=%" PRIu64 " de_busy=%" PRIu64
         " dep_stall=%" PRIu64 " resource_stall=%" PRIu64
         " pair_overlap=%" PRIu64 " triple_overlap=%" PRIu64
         " decisions=%" PRIu64 " prefetch=%" PRIu64 "/%" PRIu64
         " dma_bytes=%" PRIu64 " checksum=%016" PRIx64
         " priority_violations=%" PRIu64 " engine_issues=%" PRIu64
         "/%" PRIu64 "/%" PRIu64 "\n",
         errors == 0 ? "PASS" : "FAIL", (status[0] & 0x10) ? "dynamic" : "static",
         wait_status, config_end - config_start, run_end - run_start,
         status[1], status[3], status[4], status[5], status[6], status[7],
         status[8], status[9], status[10], status[11], status[12], status[13],
         status[14], status[15], status[16], status[18], status[17], status[19],
         status[20], status[21], status[25], status[26], status[27]);
  return errors == 0 ? 0 : 1;
}

