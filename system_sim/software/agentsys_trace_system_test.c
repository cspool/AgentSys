#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

#include "agentsys_runtime.h"
#include "generated/agentsys_app_trace.h"

#define TRACE_EVENTS 128
#define ABI_MAGIC UINT64_C(0x41545801)
#define RESULT_MAGIC UINT64_C(0x4154585f54495341)

enum trace_layer {
  LAYER_APPLICATION = 0,
  LAYER_FRAMEWORK = 1,
  LAYER_RUNTIME = 2,
  LAYER_CPU = 3,
  LAYER_XPU = 4,
  LAYER_DMA = 5,
};

enum trace_kind {
  EVENT_PROGRAM_START = 0,
  EVENT_PROGRAM_COMPLETE = 1,
  EVENT_CALL_RELEASE = 2,
  EVENT_CALL_COMPLETE = 3,
  EVENT_LOWER = 4,
  EVENT_CONFIG_START = 5,
  EVENT_CONFIG_COMPLETE = 6,
  EVENT_LAUNCH = 7,
  EVENT_WAIT_COMPLETE = 8,
  EVENT_XPU_COMPLETE = 9,
  EVENT_DMA_COMPLETE = 10,
  EVENT_TOOL_START = 11,
  EVENT_TOOL_COMPLETE = 12,
};

typedef struct {
  uint64_t cycle;
  uint64_t arg0;
  uint64_t arg1;
  uint16_t sequence;
  uint8_t layer;
  uint8_t kind;
  uint8_t program;
  uint8_t call;
  uint8_t priority;
} trace_event_t;

static trace_event_t trace_events[TRACE_EVENTS];
static unsigned trace_count;
static uint64_t trace_input[AGENTSYS_APP_INPUT_BEATS] __attribute__((aligned(64)));
static uint64_t trace_output[AGENTSYS_APP_OUTPUT_BEATS] __attribute__((aligned(64)));

static void record_event(uint8_t layer, uint8_t kind, uint8_t program,
                         uint8_t call, uint8_t priority, uint64_t arg0,
                         uint64_t arg1) {
  trace_event_t *event;
  if (trace_count >= TRACE_EVENTS)
    return;
  event = &trace_events[trace_count];
  event->cycle = agentsys_read_cycle();
  event->arg0 = arg0;
  event->arg1 = arg1;
  event->sequence = trace_count;
  event->layer = layer;
  event->kind = kind;
  event->program = program;
  event->call = call;
  event->priority = priority;
  ++trace_count;
}

static uint64_t run_tool(uint16_t cycles, uint64_t seed) {
  volatile uint64_t value = seed;
  uint16_t index;
  for (index = 0; index < cycles; ++index) {
    value ^= (value << 7) + index + UINT64_C(0x9e3779b97f4a7c15);
    asm volatile("nop");
  }
  return value;
}

int main(void) {
  uint16_t completed_calls = 0;
  uint8_t completed_programs = 0;
  uint64_t aggregate_checksum = AGENTSYS_APP_TRACE_DIGEST;
  uint64_t total_system_cycles = 0;
  uint64_t total_backend_cycles = 0;
  uint64_t total_dma_cycles = 0;
  uint64_t total_dma_bytes = 0;
  uint64_t total_config_cycles = 0;
  uint64_t total_me_busy = 0;
  uint64_t total_ve_busy = 0;
  uint64_t total_de_busy = 0;
  uint64_t total_overlap = 0;
  uint64_t total_priority_violations = 0;
  uint64_t previous_me_busy = 0;
  uint64_t previous_ve_busy = 0;
  uint64_t previous_de_busy = 0;
  uint64_t app_start = agentsys_read_cycle();
  uint64_t app_end;
  unsigned errors = 0;
  unsigned llm_calls = 0;
  unsigned tool_calls = 0;
  unsigned descriptors = 0;
  unsigned call_index;

  for (call_index = 0; call_index < AGENTSYS_APP_CALLS; ++call_index) {
    const agentsys_app_call_t *call = &agentsys_app_calls[call_index];
    uint64_t call_start = agentsys_read_cycle();
    if ((call->deps_mask & ~completed_calls) != 0) {
      ++errors;
      continue;
    }
    if (call->program_first)
      record_event(LAYER_APPLICATION, EVENT_PROGRAM_START, call->program_code,
                   0xff, call->priority, 0, 0);
    record_event(LAYER_FRAMEWORK, EVENT_CALL_RELEASE, call->program_code,
                 call_index, call->priority, call->input_tokens,
                 call->output_tokens);

    if (call->kind == 1) {
      uint64_t tool_result;
      ++tool_calls;
      record_event(LAYER_CPU, EVENT_TOOL_START, call->program_code, call_index,
                   call->priority, call->tool_cycles, 0);
      tool_result = run_tool(call->tool_cycles,
                             AGENTSYS_APP_TRACE_DIGEST ^ call_index);
      aggregate_checksum ^= tool_result;
      record_event(LAYER_CPU, EVENT_TOOL_COMPLETE, call->program_code,
                   call_index, call->priority,
                   agentsys_read_cycle() - call_start, tool_result);
    } else {
      uint64_t input_xor = 0;
      uint64_t control_xor = 0;
      uint64_t expected_checksum;
      uint64_t status[28];
      uint64_t me_busy_delta;
      uint64_t ve_busy_delta;
      uint64_t de_busy_delta;
      uint64_t config_start;
      uint64_t config_end;
      unsigned index;

      ++llm_calls;
      descriptors += call->descriptor_count;
      for (index = 0; index < AGENTSYS_APP_INPUT_BEATS; ++index) {
        trace_input[index] = UINT64_C(0x9e3779b97f4a7c15) ^
                             ((uint64_t)call_index << 40) ^
                             ((uint64_t)call->input_tokens << 16) ^ index;
        input_xor ^= trace_input[index];
      }
      for (index = 0; index < AGENTSYS_APP_OUTPUT_BEATS; ++index)
        trace_output[index] = UINT64_C(0xdeadbeefdeadbeef);
      for (index = 0; index < call->descriptor_count; ++index)
        control_xor ^= call->control[index];
      expected_checksum = input_xor ^ control_xor ^ RESULT_MAGIC;

      record_event(LAYER_FRAMEWORK, EVENT_LOWER, call->program_code,
                   call_index, call->priority, call->descriptor_count, 0);
      agentsys_clear();
      config_start = agentsys_read_cycle();
      record_event(LAYER_RUNTIME, EVENT_CONFIG_START, call->program_code,
                   call_index, call->priority, call->descriptor_count, 0);
      for (index = 0; index < call->descriptor_count; ++index) {
        agentsys_config(0, index, call->control[index]);
        agentsys_config(1, index, call->tilemem[index]);
      }
      agentsys_config(31, 0, call->descriptor_count);
      agentsys_config(31, 1, AGENTSYS_APP_INPUT_BEATS);
      agentsys_config(31, 2, AGENTSYS_APP_OUTPUT_BEATS);
      agentsys_prefetch(0);
      config_end = agentsys_read_cycle();
      total_config_cycles += config_end - config_start;
      record_event(LAYER_RUNTIME, EVENT_CONFIG_COMPLETE, call->program_code,
                   call_index, call->priority, config_end - config_start, 0);

      record_event(LAYER_CPU, EVENT_LAUNCH, call->program_code, call_index,
                   call->priority, (uintptr_t)trace_input,
                   (uintptr_t)trace_output);
      agentsys_launch(trace_input, trace_output);
      agentsys_wait();
      record_event(LAYER_CPU, EVENT_WAIT_COMPLETE, call->program_code,
                   call_index, call->priority,
                   agentsys_read_cycle() - call_start, 0);
      for (index = 0; index < 28; ++index)
        status[index] = agentsys_status(index);
      me_busy_delta = status[9] - previous_me_busy;
      ve_busy_delta = status[10] - previous_ve_busy;
      de_busy_delta = status[11] - previous_de_busy;
      previous_me_busy = status[9];
      previous_ve_busy = status[10];
      previous_de_busy = status[11];

      if (status[22] != ABI_MAGIC || status[20] != expected_checksum)
        ++errors;
      if (status[5] != call->descriptor_count ||
          status[6] != call->descriptor_count ||
          status[7] != call->descriptor_count || status[8] != 0)
        ++errors;
      if (status[25] != 3 || status[26] != 3 || status[27] != 2)
        ++errors;
      if (me_busy_delta != 240 || ve_busy_delta != 240 || de_busy_delta != 160)
        ++errors;
      if (status[19] !=
          (AGENTSYS_APP_INPUT_BEATS + AGENTSYS_APP_OUTPUT_BEATS) * 8)
        ++errors;
      if (status[21] != 0)
        ++errors;
      for (index = 0; index < AGENTSYS_APP_OUTPUT_BEATS; ++index) {
        if (trace_output[index] != (expected_checksum ^ index))
          ++errors;
      }
      total_system_cycles += status[1];
      total_dma_cycles += status[3];
      total_backend_cycles += status[4];
      total_me_busy += me_busy_delta;
      total_ve_busy += ve_busy_delta;
      total_de_busy += de_busy_delta;
      total_overlap += status[14];
      total_dma_bytes += status[19];
      total_priority_violations += status[21];
      aggregate_checksum ^= status[20];
      record_event(LAYER_XPU, EVENT_XPU_COMPLETE, call->program_code,
                   call_index, call->priority, status[4],
                   (me_busy_delta << 32) | (ve_busy_delta << 16) |
                       de_busy_delta);
      record_event(LAYER_DMA, EVENT_DMA_COMPLETE, call->program_code,
                   call_index, call->priority, status[3], status[19]);
    }

    completed_calls |= (uint16_t)1 << call_index;
    record_event(LAYER_FRAMEWORK, EVENT_CALL_COMPLETE, call->program_code,
                 call_index, call->priority, agentsys_read_cycle() - call_start,
                 aggregate_checksum);
    if (call->program_last) {
      completed_programs |= (uint8_t)1 << call->program_code;
      record_event(LAYER_APPLICATION, EVENT_PROGRAM_COMPLETE,
                   call->program_code, 0xff, call->priority, completed_calls,
                   aggregate_checksum);
    }
  }
  app_end = agentsys_read_cycle();

  if (completed_calls != ((UINT16_C(1) << AGENTSYS_APP_CALLS) - 1))
    ++errors;
  if (completed_programs != ((1u << AGENTSYS_APP_PROGRAMS) - 1))
    ++errors;
  if (llm_calls != 10 || tool_calls != 1 || descriptors != 80)
    ++errors;
  if (total_priority_violations != 0)
    ++errors;

  printf("AGENTSYS_APP_TRACE version=1 events=%u digest=%016" PRIx64 "\n",
         trace_count, AGENTSYS_APP_TRACE_DIGEST);
  for (call_index = 0; call_index < AGENTSYS_APP_CALLS; ++call_index) {
    const agentsys_app_call_t *call = &agentsys_app_calls[call_index];
    uint64_t cycles[13] = {0};
    uint64_t xpu_cycles = 0;
    uint64_t dma_call_cycles = 0;
    uint64_t dma_call_bytes = 0;
    unsigned event_index;
    for (event_index = 0; event_index < trace_count; ++event_index) {
      const trace_event_t *event = &trace_events[event_index];
      if (event->call != call_index)
        continue;
      cycles[event->kind] = event->cycle;
      if (event->kind == EVENT_XPU_COMPLETE)
        xpu_cycles = event->arg0;
      if (event->kind == EVENT_DMA_COMPLETE) {
        dma_call_cycles = event->arg0;
        dma_call_bytes = event->arg1;
      }
    }
    printf("AGENTSYS_APP_CALL index=%u program=%s call=%s kind=%s"
           " priority=%u deps=%04x first=%u last=%u"
           " release=%" PRIu64 " lower=%" PRIu64
           " config_start=%" PRIu64 " config_end=%" PRIu64
           " launch=%" PRIu64 " wait=%" PRIu64
           " xpu=%" PRIu64 " dma=%" PRIu64 " complete=%" PRIu64
           " tool_start=%" PRIu64 " tool_end=%" PRIu64
           " xpu_cycles=%" PRIu64 " dma_cycles=%" PRIu64
           " dma_bytes=%" PRIu64 "\n",
           call_index, call->program_id, call->call_id,
           call->kind ? "tool" : "llm", call->priority, call->deps_mask,
           call->program_first, call->program_last,
           cycles[EVENT_CALL_RELEASE], cycles[EVENT_LOWER],
           cycles[EVENT_CONFIG_START], cycles[EVENT_CONFIG_COMPLETE],
           cycles[EVENT_LAUNCH], cycles[EVENT_WAIT_COMPLETE],
           cycles[EVENT_XPU_COMPLETE], cycles[EVENT_DMA_COMPLETE],
           cycles[EVENT_CALL_COMPLETE], cycles[EVENT_TOOL_START],
           cycles[EVENT_TOOL_COMPLETE], xpu_cycles, dma_call_cycles,
           dma_call_bytes);
  }
  printf("AGENTSYS_APP_%s backend=%s programs=3 calls=%u llm_calls=%u"
         " tool_calls=%u launches=%u descriptors=%u trace_events=%u"
         " cpu_cycles=%" PRIu64 " config_cycles=%" PRIu64
         " system_cycles=%" PRIu64 " backend_cycles=%" PRIu64
         " dma_cycles=%" PRIu64 " dma_bytes=%" PRIu64
         " me_busy=%" PRIu64 " ve_busy=%" PRIu64 " de_busy=%" PRIu64
         " overlap=%" PRIu64 " priority_violations=%" PRIu64
         " checksum=%016" PRIx64 " app_digest=%016" PRIx64 "\n",
         errors == 0 ? "PASS" : "FAIL",
         (agentsys_status(0) & 0x10) ? "dynamic" : "static",
         AGENTSYS_APP_CALLS, llm_calls, tool_calls, llm_calls, descriptors,
         trace_count, app_end - app_start, total_config_cycles,
         total_system_cycles, total_backend_cycles, total_dma_cycles,
         total_dma_bytes, total_me_busy, total_ve_busy, total_de_busy,
         total_overlap, total_priority_violations, aggregate_checksum,
         AGENTSYS_APP_TRACE_DIGEST);
  return errors == 0 ? 0 : 1;
}
