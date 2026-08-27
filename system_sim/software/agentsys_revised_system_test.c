#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>

#include "agentsys_xpu_runtime.h"
#ifndef AGENTSYS_REVISED_TRACE_HEADER
#define AGENTSYS_REVISED_TRACE_HEADER "generated/agentsys_revised_app_trace.h"
#endif
#include AGENTSYS_REVISED_TRACE_HEADER

#ifndef AGENTSYS_WORKLOAD_NAME
#define AGENTSYS_WORKLOAD_NAME "certified_fixed"
#endif
#ifndef AGENTSYS_WORKLOAD_DIGEST
#define AGENTSYS_WORKLOAD_DIGEST UINT64_C(0)
#endif
#ifndef AGENTSYS_REVISED_TRACE_CAPACITY
#define AGENTSYS_REVISED_TRACE_CAPACITY 192
#endif
#ifndef AGENTSYS_EXPECT_LLM_CALLS
#define AGENTSYS_EXPECT_LLM_CALLS 10
#define AGENTSYS_EXPECT_TOOL_CALLS 1
#define AGENTSYS_EXPECT_DESCRIPTORS 80
#define AGENTSYS_EXPECT_REACTIVE_FLOWS 2
#define AGENTSYS_EXPECT_PROACTIVE_FLOWS 8
#define AGENTSYS_EXPECT_HPTPE_PLACEMENTS 30
#define AGENTSYS_EXPECT_VECTOR_PLACEMENTS 30
#define AGENTSYS_EXPECT_DATA_PLACEMENTS 20
#define AGENTSYS_EXPECT_ME_BUSY 2400
#define AGENTSYS_EXPECT_VE_BUSY 2400
#define AGENTSYS_EXPECT_DE_BUSY 1600
#define AGENTSYS_HPTPE_LANES 256
#endif

#define TRACE_EVENTS AGENTSYS_REVISED_TRACE_CAPACITY
#define XPU_ABI_MAGIC UINT64_C(0x58505502)

enum trace_layer {
  LAYER_APPLICATION = 0,
  LAYER_AGENTIX = 1,
  LAYER_MLLM = 2,
  LAYER_AGENTXPU = 3,
  LAYER_SOFTWARE = 4,
  LAYER_CPU = 5,
  LAYER_XPU = 6,
  LAYER_DMA = 7,
};

enum trace_kind {
  EVENT_PROGRAM_START = 0,
  EVENT_PROGRAM_COMPLETE = 1,
  EVENT_CALL_RELEASE = 2,
  EVENT_CALL_COMPLETE = 3,
  EVENT_MLLM_LOWER = 4,
  EVENT_AGENTXPU_PLAN = 5,
  EVENT_CONFIG_START = 6,
  EVENT_CONFIG_COMPLETE = 7,
  EVENT_LAUNCH = 8,
  EVENT_WAIT_COMPLETE = 9,
  EVENT_XPU_COMPLETE = 10,
  EVENT_DMA_COMPLETE = 11,
  EVENT_TOOL_START = 12,
  EVENT_TOOL_COMPLETE = 13,
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
static unsigned trace_overflow;
static uint64_t trace_input[AGENTSYS_REVISED_INPUT_BEATS]
    __attribute__((aligned(64)));
static uint64_t trace_output[AGENTSYS_REVISED_OUTPUT_BEATS]
    __attribute__((aligned(64)));

static void record_event(uint8_t layer, uint8_t kind, uint8_t program,
                         uint8_t call, uint8_t priority, uint64_t arg0,
                         uint64_t arg1) {
  trace_event_t *event;
  if (trace_count >= TRACE_EVENTS) {
    trace_overflow = 1;
    return;
  }
  event = &trace_events[trace_count];
  event->cycle = agentsys_xpu_read_cycle();
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
  uint64_t completed_calls = 0;
  uint64_t completed_programs = 0;
  uint64_t aggregate_checksum = AGENTSYS_REVISED_TRACE_DIGEST;
  uint64_t total_system_cycles = 0;
  uint64_t total_backend_cycles = 0;
  uint64_t total_dma_cycles = 0;
  uint64_t total_dma_bytes = 0;
  uint64_t total_config_cycles = 0;
  uint64_t total_me_busy = 0;
  uint64_t total_ve_busy = 0;
  uint64_t total_de_busy = 0;
  uint64_t total_overlap = 0;
  uint64_t total_hptpe_mac_ops = 0;
  uint64_t total_priority_violations = 0;
  uint64_t previous_me_busy = 0;
  uint64_t previous_ve_busy = 0;
  uint64_t previous_de_busy = 0;
  uint64_t previous_hptpe_mac_ops = 0;
  uint64_t app_start = agentsys_xpu_read_cycle();
  uint64_t app_end;
  unsigned errors = 0;
  unsigned llm_calls = 0;
  unsigned tool_calls = 0;
  unsigned descriptors = 0;
  unsigned reactive_flows = 0;
  unsigned proactive_flows = 0;
  unsigned hptpe_placements = 0;
  unsigned vector_placements = 0;
  unsigned data_placements = 0;
  unsigned call_index;

  for (call_index = 0; call_index < AGENTSYS_REVISED_CALLS; ++call_index) {
    const agentsys_revised_call_t *call = &agentsys_revised_calls[call_index];
    uint64_t call_start = agentsys_xpu_read_cycle();
    if ((call->deps_mask & ~completed_calls) != 0) {
      ++errors;
      continue;
    }
    if (call->program_first)
      record_event(LAYER_APPLICATION, EVENT_PROGRAM_START, call->program_code,
                   0xff, call->priority, 0, 0);
    record_event(LAYER_AGENTIX, EVENT_CALL_RELEASE, call->program_code,
                 call_index, call->priority, call->input_tokens,
                 call->output_tokens);

    if (call->kind == 1) {
      uint64_t tool_result;
      ++tool_calls;
      record_event(LAYER_CPU, EVENT_TOOL_START, call->program_code, call_index,
                   call->priority, call->tool_cycles, 0);
      tool_result = run_tool(call->tool_cycles,
                             AGENTSYS_REVISED_TRACE_DIGEST ^ call_index);
      aggregate_checksum ^= tool_result;
      record_event(LAYER_CPU, EVENT_TOOL_COMPLETE, call->program_code,
                   call_index, call->priority,
                   agentsys_xpu_read_cycle() - call_start, tool_result);
    } else {
      uint64_t status[29];
      uint64_t me_busy_delta;
      uint64_t ve_busy_delta;
      uint64_t de_busy_delta;
      uint64_t hptpe_mac_delta;
      uint64_t config_start;
      uint64_t config_end;
      uint64_t placement_pack = 0;
      uint64_t expected_me_busy = 0;
      uint64_t expected_ve_busy = 0;
      uint64_t expected_de_busy = 0;
      unsigned expected_me_issued = 0;
      unsigned expected_ve_issued = 0;
      unsigned expected_de_issued = 0;
      unsigned index;

      ++llm_calls;
      if (call->flow_code == 0)
        ++reactive_flows;
      else
        ++proactive_flows;
      descriptors += call->descriptor_count;
      for (index = 0; index < AGENTSYS_REVISED_INPUT_BEATS; ++index)
        trace_input[index] = UINT64_C(0x9e3779b97f4a7c15) ^
                             ((uint64_t)call_index << 40) ^
                             ((uint64_t)call->input_tokens << 16) ^ index;
      for (index = 0; index < AGENTSYS_REVISED_OUTPUT_BEATS; ++index)
        trace_output[index] = UINT64_C(0xdeadbeefdeadbeef);

      for (index = 0; index < call->descriptor_count; ++index) {
        uint64_t control = call->control[index];
        uint64_t tilemem = call->tilemem[index];
        if (((control >> 61) & 1) != call->flow_code ||
            ((control >> 62) & 1) != 1 ||
            ((control >> 63) & 1) != call->stage[index] ||
            ((control >> 34) & 3) != call->placement[index] ||
            ((tilemem >> 54) & 0x3ff) != call->source_op[index])
          ++errors;
        placement_pack |= ((uint64_t)call->placement[index] & 3)
                          << (index * 2);
        if (call->placement[index] == 0) {
          ++hptpe_placements;
          ++expected_me_issued;
          expected_me_busy += (control >> 36) & 0xffff;
        } else if (call->placement[index] == 1) {
          ++vector_placements;
          ++expected_ve_issued;
          expected_ve_busy += (control >> 36) & 0xffff;
        } else if (call->placement[index] == 2) {
          ++data_placements;
          ++expected_de_issued;
          expected_de_busy += (control >> 36) & 0xffff;
        } else {
          ++errors;
        }
      }

      record_event(LAYER_MLLM, EVENT_MLLM_LOWER, call->program_code,
                   call_index, call->priority, call->descriptor_count,
                   AGENTSYS_REVISED_MIR_DIGEST);
      record_event(LAYER_AGENTXPU, EVENT_AGENTXPU_PLAN, call->program_code,
                   call_index, call->priority,
                   ((uint64_t)call->flow_code << 56) |
                       ((uint64_t)call->prefill_chunk_tokens << 40) |
                       ((uint64_t)call->decode_batch_cap << 32) |
                       call->elastic_hptpe_percent,
                   placement_pack);

      agentsys_xpu_clear();
      config_start = agentsys_xpu_read_cycle();
      record_event(LAYER_SOFTWARE, EVENT_CONFIG_START, call->program_code,
                   call_index, call->priority, call->descriptor_count, 0);
      for (index = 0; index < call->descriptor_count; ++index) {
        agentsys_xpu_config(0, index, call->control[index]);
        agentsys_xpu_config(1, index, call->tilemem[index]);
      }
      agentsys_xpu_config(31, 0, call->descriptor_count);
      agentsys_xpu_config(31, 1, AGENTSYS_REVISED_INPUT_BEATS);
      agentsys_xpu_config(31, 2, AGENTSYS_REVISED_OUTPUT_BEATS);
      agentsys_xpu_config(31, 3, call_index);
      config_end = agentsys_xpu_read_cycle();
      total_config_cycles += config_end - config_start;
      record_event(LAYER_SOFTWARE, EVENT_CONFIG_COMPLETE, call->program_code,
                   call_index, call->priority, config_end - config_start, 0);

      record_event(LAYER_CPU, EVENT_LAUNCH, call->program_code, call_index,
                   call->priority, (uintptr_t)trace_input,
                   (uintptr_t)trace_output);
      agentsys_xpu_launch(trace_input, trace_output);
      agentsys_xpu_wait();
      record_event(LAYER_CPU, EVENT_WAIT_COMPLETE, call->program_code,
                   call_index, call->priority,
                   agentsys_xpu_read_cycle() - call_start, 0);
      for (index = 0; index < 29; ++index)
        status[index] = agentsys_xpu_status(index);

      me_busy_delta = status[9] - previous_me_busy;
      ve_busy_delta = status[10] - previous_ve_busy;
      de_busy_delta = status[11] - previous_de_busy;
      hptpe_mac_delta = status[17] - previous_hptpe_mac_ops;
      previous_me_busy = status[9];
      previous_ve_busy = status[10];
      previous_de_busy = status[11];
      previous_hptpe_mac_ops = status[17];

      if (status[22] != XPU_ABI_MAGIC || status[20] == 0)
        ++errors;
      if (status[2] != 20 || status[18] != call->descriptor_count)
        ++errors;
      if (status[5] != call->descriptor_count ||
          status[6] != call->descriptor_count ||
          status[7] != call->descriptor_count || status[8] != 0)
        ++errors;
      if (status[25] != expected_me_issued || status[26] != expected_ve_issued ||
          status[27] != expected_de_issued)
        ++errors;
      if (status[28] != ((status[0] & 0x10) ? 7 : 0))
        ++errors;
      if (me_busy_delta != expected_me_busy || ve_busy_delta != expected_ve_busy ||
          de_busy_delta != expected_de_busy)
        ++errors;
      if (hptpe_mac_delta != expected_me_busy * AGENTSYS_HPTPE_LANES)
        ++errors;
      if (status[19] !=
          (AGENTSYS_REVISED_INPUT_BEATS + AGENTSYS_REVISED_OUTPUT_BEATS) * 8)
        ++errors;
      if (status[21] != 0)
        ++errors;
      for (index = 0; index < AGENTSYS_REVISED_OUTPUT_BEATS; ++index) {
        if (trace_output[index] != (status[20] ^ index))
          ++errors;
      }

      total_system_cycles += status[1];
      total_dma_cycles += status[3];
      total_backend_cycles += status[4];
      total_me_busy += me_busy_delta;
      total_ve_busy += ve_busy_delta;
      total_de_busy += de_busy_delta;
      total_overlap += status[14];
      total_hptpe_mac_ops += hptpe_mac_delta;
      total_dma_bytes += status[19];
      total_priority_violations += status[21];
      aggregate_checksum ^= status[20];
      record_event(LAYER_XPU, EVENT_XPU_COMPLETE, call->program_code,
                   call_index, call->priority, status[4], hptpe_mac_delta);
      record_event(LAYER_DMA, EVENT_DMA_COMPLETE, call->program_code,
                   call_index, call->priority, status[3], status[19]);
    }

    completed_calls |= UINT64_C(1) << call_index;
    record_event(LAYER_AGENTIX, EVENT_CALL_COMPLETE, call->program_code,
                 call_index, call->priority,
                 agentsys_xpu_read_cycle() - call_start, aggregate_checksum);
    if (call->program_last) {
      completed_programs |= UINT64_C(1) << call->program_code;
      record_event(LAYER_APPLICATION, EVENT_PROGRAM_COMPLETE,
                   call->program_code, 0xff, call->priority, completed_calls,
                   aggregate_checksum);
    }
  }
  app_end = agentsys_xpu_read_cycle();

  if (completed_calls != ((UINT64_C(1) << AGENTSYS_REVISED_CALLS) - 1))
    ++errors;
  if (completed_programs != ((UINT64_C(1) << AGENTSYS_REVISED_PROGRAMS) - 1))
    ++errors;
  if (llm_calls != AGENTSYS_EXPECT_LLM_CALLS ||
      tool_calls != AGENTSYS_EXPECT_TOOL_CALLS ||
      descriptors != AGENTSYS_EXPECT_DESCRIPTORS)
    ++errors;
  if (reactive_flows != AGENTSYS_EXPECT_REACTIVE_FLOWS ||
      proactive_flows != AGENTSYS_EXPECT_PROACTIVE_FLOWS)
    ++errors;
  if (hptpe_placements != AGENTSYS_EXPECT_HPTPE_PLACEMENTS ||
      vector_placements != AGENTSYS_EXPECT_VECTOR_PLACEMENTS ||
      data_placements != AGENTSYS_EXPECT_DATA_PLACEMENTS)
    ++errors;
  if (total_me_busy != AGENTSYS_EXPECT_ME_BUSY ||
      total_ve_busy != AGENTSYS_EXPECT_VE_BUSY ||
      total_de_busy != AGENTSYS_EXPECT_DE_BUSY)
    ++errors;
  if (total_priority_violations != 0)
    ++errors;
  if (trace_overflow)
    ++errors;

  printf("AGENTSYS_REVISED_TRACE version=1 events=%u digest=%016" PRIx64
         " mir=%016" PRIx64 " workload=%s workload_digest=%016" PRIx64 "\n",
         trace_count, AGENTSYS_REVISED_TRACE_DIGEST,
         AGENTSYS_REVISED_MIR_DIGEST, AGENTSYS_WORKLOAD_NAME,
         AGENTSYS_WORKLOAD_DIGEST);
  for (call_index = 0; call_index < AGENTSYS_REVISED_CALLS; ++call_index) {
    const agentsys_revised_call_t *call = &agentsys_revised_calls[call_index];
    uint64_t cycles[14] = {0};
    uint64_t xpu_cycles = 0;
    uint64_t hptpe_ops = 0;
    uint64_t dma_call_cycles = 0;
    uint64_t dma_call_bytes = 0;
    unsigned event_index;
    for (event_index = 0; event_index < trace_count; ++event_index) {
      const trace_event_t *event = &trace_events[event_index];
      if (event->call != call_index)
        continue;
      cycles[event->kind] = event->cycle;
      if (event->kind == EVENT_XPU_COMPLETE) {
        xpu_cycles = event->arg0;
        hptpe_ops = event->arg1;
      }
      if (event->kind == EVENT_DMA_COMPLETE) {
        dma_call_cycles = event->arg0;
        dma_call_bytes = event->arg1;
      }
    }
    printf("AGENTSYS_REVISED_CALL index=%u program=%s call=%s kind=%s"
           " priority=%u flow=%s deps=%016" PRIx64 " first=%u last=%u"
           " release=%" PRIu64 " mllm=%" PRIu64
           " agentxpu=%" PRIu64 " config_start=%" PRIu64
           " config_end=%" PRIu64 " launch=%" PRIu64
           " wait=%" PRIu64 " xpu=%" PRIu64 " dma=%" PRIu64
           " complete=%" PRIu64 " tool_start=%" PRIu64
           " tool_end=%" PRIu64 " xpu_cycles=%" PRIu64
           " hptpe_ops=%" PRIu64 " dma_cycles=%" PRIu64
           " dma_bytes=%" PRIu64 "\n",
           call_index, call->program_id, call->call_id,
           call->kind ? "tool" : "llm", call->priority,
           call->flow_code ? "proactive" : "reactive",
           (uint64_t)call->deps_mask,
           call->program_first, call->program_last,
           cycles[EVENT_CALL_RELEASE], cycles[EVENT_MLLM_LOWER],
           cycles[EVENT_AGENTXPU_PLAN], cycles[EVENT_CONFIG_START],
           cycles[EVENT_CONFIG_COMPLETE], cycles[EVENT_LAUNCH],
           cycles[EVENT_WAIT_COMPLETE], cycles[EVENT_XPU_COMPLETE],
           cycles[EVENT_DMA_COMPLETE], cycles[EVENT_CALL_COMPLETE],
           cycles[EVENT_TOOL_START], cycles[EVENT_TOOL_COMPLETE], xpu_cycles,
           hptpe_ops, dma_call_cycles, dma_call_bytes);
  }

  printf("AGENTSYS_REVISED_%s backend=%s abi=xpu_v2 workload=%s"
         " workload_digest=%016" PRIx64 " programs=%u calls=%u"
         " llm_calls=%u tool_calls=%u launches=%u descriptors=%u"
         " trace_events=%u cpu_cycles=%" PRIu64
         " config_cycles=%" PRIu64 " system_cycles=%" PRIu64
         " backend_cycles=%" PRIu64 " dma_cycles=%" PRIu64
         " dma_bytes=%" PRIu64 " me_busy=%" PRIu64
         " ve_busy=%" PRIu64 " de_busy=%" PRIu64
         " overlap=%" PRIu64 " hptpe_mac_ops=%" PRIu64
         " priority_violations=%" PRIu64
         " dispatch_latency=%" PRIu64
         " flows=%u/%u placements=%u/%u/%u"
         " checksum=%016" PRIx64 " app_digest=%016" PRIx64
         " mir_digest=%016" PRIx64 "\n",
         errors == 0 ? "PASS" : "FAIL",
         (agentsys_xpu_status(0) & 0x10) ? "dynamic" : "static",
         AGENTSYS_WORKLOAD_NAME, AGENTSYS_WORKLOAD_DIGEST,
         AGENTSYS_REVISED_PROGRAMS, AGENTSYS_REVISED_CALLS,
         llm_calls, tool_calls, llm_calls, descriptors,
         trace_count, app_end - app_start, total_config_cycles,
         total_system_cycles, total_backend_cycles, total_dma_cycles,
         total_dma_bytes, total_me_busy, total_ve_busy, total_de_busy,
         total_overlap, total_hptpe_mac_ops, total_priority_violations,
         agentsys_xpu_status(28),
         reactive_flows, proactive_flows, hptpe_placements,
         vector_placements, data_placements, aggregate_checksum,
         AGENTSYS_REVISED_TRACE_DIGEST, AGENTSYS_REVISED_MIR_DIGEST);
  return errors == 0 ? 0 : 1;
}
