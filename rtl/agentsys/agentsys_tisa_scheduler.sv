`timescale 1ns/1ps
/* verilator lint_off UNUSED */

module agentsys_tisa_scheduler #(
    parameter DYNAMIC = 1,
    parameter ENTRIES = 8,
    parameter [63:0] RESULT_MAGIC = 64'h4154585f54495341,
    parameter INCLUDE_ENGINE_CHECKSUM = 0,
    parameter TRACE = 0,
    parameter [7:0] DISPATCH_LATENCY = 0
) (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        cfg_valid_i,
    input  wire [4:0]  cfg_target_i,
    input  wire [4:0]  cfg_index_i,
    input  wire [63:0] cfg_word_i,
    input  wire        launch_i,
    input  wire [63:0] input_checksum_i,
    input  wire        cancel_valid_i,
    input  wire [7:0]  cancel_task_mask_i,
    input  wire        prefetch_valid_i,
    input  wire [2:0]  prefetch_index_i,
    output wire        busy_o,
    output reg         done_o,
    output reg  [63:0] result_checksum_o,
    output reg  [63:0] stat_cycles_o,
    output reg  [63:0] stat_submitted_o,
    output reg  [63:0] stat_issued_o,
    output reg  [63:0] stat_completed_o,
    output reg  [63:0] stat_canceled_o,
    output wire [63:0] stat_me_busy_o,
    output wire [63:0] stat_ve_busy_o,
    output wire [63:0] stat_de_busy_o,
    output reg  [63:0] stat_dependency_stall_o,
    output reg  [63:0] stat_resource_stall_o,
    output reg  [63:0] stat_pair_overlap_o,
    output reg  [63:0] stat_triple_overlap_o,
    output reg  [63:0] stat_decisions_o,
    output reg  [63:0] stat_prefetch_requests_o,
    output reg  [63:0] stat_prefetch_hits_o,
    output reg  [63:0] stat_priority_violations_o,
    output reg  [63:0] stat_me_issued_o,
    output reg  [63:0] stat_ve_issued_o,
    output reg  [63:0] stat_de_issued_o,
    output wire [7:0]  completed_mask_o,
    output wire [7:0]  canceled_mask_o
);
  localparam TARGET_CONTROL = 5'd0;
  localparam TARGET_TILEMEM = 5'd1;
  localparam TARGET_GLOBAL = 5'd31;
  localparam ENGINE_ME = 2'd0;
  localparam ENGINE_VE = 2'd1;
  localparam ENGINE_DE = 2'd2;

  reg [63:0] control_q [0:ENTRIES-1];
  reg [63:0] tilemem_q [0:ENTRIES-1];
  reg [7:0] configured_valid_q;
  reg [3:0] descriptor_count_q;
  reg [7:0] active_mask_q;
  reg [7:0] issued_mask_q;
  reg [7:0] completed_mask_q;
  reg [7:0] canceled_mask_q;
  reg [7:0] prefetched_mask_q;
  reg [7:0] cancel_tasks_q;
  reg running_q;
  reg [63:0] input_checksum_q;
  reg [63:0] descriptor_digest_q;

  reg [2:0] me_index_q;
  reg [2:0] ve_index_q;
  reg [2:0] de_index_q;
  reg       me_dispatch_valid_q;
  reg       ve_dispatch_valid_q;
  reg       de_dispatch_valid_q;
  reg [7:0] me_dispatch_count_q;
  reg [7:0] ve_dispatch_count_q;
  reg [7:0] de_dispatch_count_q;
  reg [2:0] me_dispatch_index_q;
  reg [2:0] ve_dispatch_index_q;
  reg [2:0] de_dispatch_index_q;

  reg cand_me_valid;
  reg cand_ve_valid;
  reg cand_de_valid;
  reg [2:0] cand_me_index;
  reg [2:0] cand_ve_index;
  reg [2:0] cand_de_index;
  reg [1:0] cand_me_priority;
  reg [1:0] cand_ve_priority;
  reg [1:0] cand_de_priority;
  reg cand_me_safe;
  reg cand_ve_safe;
  reg cand_de_safe;
  reg static_group_ready;
  reg dependency_blocked_any;
  reg resource_blocked_any;
  integer i;
  integer j;

  wire me_busy;
  wire me_done;
  wire [63:0] me_checksum;
  wire [63:0] me_busy_cycles;
  wire ve_busy;
  wire ve_done;
  wire [63:0] ve_checksum;
  wire [63:0] ve_busy_cycles;
  wire de_busy;
  wire de_done;
  wire [63:0] de_checksum;
  wire [63:0] de_busy_cycles;

  localparam USE_DYNAMIC_DISPATCH = DYNAMIC && (DISPATCH_LATENCY != 0);
  wire admit_me = running_q && cand_me_valid && cand_me_safe
      && !me_busy && !me_dispatch_valid_q;
  wire admit_ve_pre = running_q && cand_ve_valid && cand_ve_safe
      && !ve_busy && !ve_dispatch_valid_q;
  wire admit_ve = admit_ve_pre
      && !(DYNAMIC && admit_me
           && semantic_hazard(control_q[cand_ve_index], tilemem_q[cand_ve_index],
                              control_q[cand_me_index], tilemem_q[cand_me_index]));
  wire admit_de_pre = running_q && cand_de_valid && cand_de_safe
      && !de_busy && !de_dispatch_valid_q;
  wire admit_de = admit_de_pre
      && !(DYNAMIC && admit_me
           && semantic_hazard(control_q[cand_de_index], tilemem_q[cand_de_index],
                              control_q[cand_me_index], tilemem_q[cand_me_index]))
      && !(DYNAMIC && admit_ve
           && semantic_hazard(control_q[cand_de_index], tilemem_q[cand_de_index],
                              control_q[cand_ve_index], tilemem_q[cand_ve_index]));
  wire reserve_me = USE_DYNAMIC_DISPATCH && admit_me;
  wire reserve_ve = USE_DYNAMIC_DISPATCH && admit_ve;
  wire reserve_de = USE_DYNAMIC_DISPATCH && admit_de;
  wire issue_me = USE_DYNAMIC_DISPATCH
      ? (running_q && me_dispatch_valid_q && (me_dispatch_count_q == 1) && !me_busy)
      : admit_me;
  wire issue_ve = USE_DYNAMIC_DISPATCH
      ? (running_q && ve_dispatch_valid_q && (ve_dispatch_count_q == 1) && !ve_busy)
      : admit_ve;
  wire issue_de = USE_DYNAMIC_DISPATCH
      ? (running_q && de_dispatch_valid_q && (de_dispatch_count_q == 1) && !de_busy)
      : admit_de;
  wire [2:0] issue_me_index = USE_DYNAMIC_DISPATCH ? me_dispatch_index_q : cand_me_index;
  wire [2:0] issue_ve_index = USE_DYNAMIC_DISPATCH ? ve_dispatch_index_q : cand_ve_index;
  wire [2:0] issue_de_index = USE_DYNAMIC_DISPATCH ? de_dispatch_index_q : cand_de_index;
  wire [7:0] issue_mask = (issue_me ? (8'b1 << issue_me_index) : 8'd0)
      | (issue_ve ? (8'b1 << issue_ve_index) : 8'd0)
      | (issue_de ? (8'b1 << issue_de_index) : 8'd0);
  wire [7:0] engine_done_mask = (me_done ? (8'b1 << me_index_q) : 8'd0)
      | (ve_done ? (8'b1 << ve_index_q) : 8'd0)
      | (de_done ? (8'b1 << de_index_q) : 8'd0);

  wire [63:0] me_seed = input_checksum_q ^ control_q[issue_me_index]
      ^ tilemem_q[issue_me_index] ^ {61'd0, issue_me_index};
  wire [63:0] ve_seed = input_checksum_q ^ control_q[issue_ve_index]
      ^ tilemem_q[issue_ve_index] ^ {61'd0, issue_ve_index};
  wire [63:0] de_seed = input_checksum_q ^ control_q[issue_de_index]
      ^ tilemem_q[issue_de_index] ^ {61'd0, issue_de_index};

  assign busy_o = running_q;
  assign completed_mask_o = completed_mask_q;
  assign canceled_mask_o = canceled_mask_q;
  assign stat_me_busy_o = me_busy_cycles;
  assign stat_ve_busy_o = ve_busy_cycles;
  assign stat_de_busy_o = de_busy_cycles;

  function automatic reads_access;
    input [1:0] access;
    begin
      reads_access = (access == 2'd0) || (access == 2'd2);
    end
  endfunction

  function automatic writes_access;
    input [1:0] access;
    begin
      writes_access = (access == 2'd1) || (access == 2'd2);
    end
  endfunction

  function automatic semantic_hazard;
    input [63:0] younger_control;
    input [63:0] younger_mem;
    input [63:0] older_control;
    input [63:0] older_mem;
    reg [32:0] younger_end;
    reg [32:0] older_end;
    reg overlap;
    reg same_domain;
    reg raw_hazard;
    reg war_hazard;
    reg waw_hazard;
    begin
      younger_end = {1'b0, younger_mem[31:0]} + {17'd0, younger_mem[47:32]} + 1'b1;
      older_end = {1'b0, older_mem[31:0]} + {17'd0, older_mem[47:32]} + 1'b1;
      overlap = ({1'b0, younger_mem[31:0]} < older_end)
          && ({1'b0, older_mem[31:0]} < younger_end);
      same_domain = (younger_mem[49:48] == older_mem[49:48])
          && (younger_mem[53:50] == older_mem[53:50]);
      raw_hazard = writes_access(older_control[25:24])
          && reads_access(younger_control[25:24]);
      war_hazard = reads_access(older_control[25:24])
          && writes_access(younger_control[25:24]);
      waw_hazard = writes_access(older_control[25:24])
          && writes_access(younger_control[25:24]);
      semantic_hazard = same_domain && overlap
          && (raw_hazard || war_hazard || waw_hazard);
    end
  endfunction

  function automatic [3:0] popcount8;
    input [7:0] value;
    integer k;
    begin
      popcount8 = 4'd0;
      for (k = 0; k < 8; k = k + 1)
        popcount8 = popcount8 + {3'd0, value[k]};
    end
  endfunction

  function automatic [7:0] count_mask;
    input [3:0] count;
    begin
      if (count >= 8)
        count_mask = 8'hff;
      else if (count == 0)
        count_mask = 8'h00;
      else
        count_mask = (8'h01 << count) - 1'b1;
    end
  endfunction

  function automatic candidate_safe_from_flight;
    input [2:0] candidate_index;
    begin
      candidate_safe_from_flight = 1'b1;
      if (me_busy && semantic_hazard(control_q[candidate_index], tilemem_q[candidate_index],
                                     control_q[me_index_q], tilemem_q[me_index_q]))
        candidate_safe_from_flight = 1'b0;
      if (ve_busy && semantic_hazard(control_q[candidate_index], tilemem_q[candidate_index],
                                     control_q[ve_index_q], tilemem_q[ve_index_q]))
        candidate_safe_from_flight = 1'b0;
      if (de_busy && semantic_hazard(control_q[candidate_index], tilemem_q[candidate_index],
                                     control_q[de_index_q], tilemem_q[de_index_q]))
        candidate_safe_from_flight = 1'b0;
      if (me_dispatch_valid_q
          && semantic_hazard(control_q[candidate_index], tilemem_q[candidate_index],
                             control_q[me_dispatch_index_q], tilemem_q[me_dispatch_index_q]))
        candidate_safe_from_flight = 1'b0;
      if (ve_dispatch_valid_q
          && semantic_hazard(control_q[candidate_index], tilemem_q[candidate_index],
                             control_q[ve_dispatch_index_q], tilemem_q[ve_dispatch_index_q]))
        candidate_safe_from_flight = 1'b0;
      if (de_dispatch_valid_q
          && semantic_hazard(control_q[candidate_index], tilemem_q[candidate_index],
                             control_q[de_dispatch_index_q], tilemem_q[de_dispatch_index_q]))
        candidate_safe_from_flight = 1'b0;
    end
  endfunction

  wire [7:0] terminal_mask = completed_mask_q | canceled_mask_q;
  wire [7:0] pending_mask = active_mask_q & ~issued_mask_q & ~terminal_mask;

  always @* begin
    cand_me_valid = 1'b0;
    cand_ve_valid = 1'b0;
    cand_de_valid = 1'b0;
    cand_me_index = 3'd0;
    cand_ve_index = 3'd0;
    cand_de_index = 3'd0;
    cand_me_priority = 2'b11;
    cand_ve_priority = 2'b11;
    cand_de_priority = 2'b11;
    dependency_blocked_any = 1'b0;
    resource_blocked_any = 1'b0;

    for (i = 0; i < ENTRIES; i = i + 1) begin
      if (pending_mask[i] && !cancel_tasks_q[control_q[i][10:8]]) begin
        if ((control_q[i][23:16] & ~terminal_mask) != 0) begin
          dependency_blocked_any = 1'b1;
        end else begin
          static_group_ready = 1'b1;
          if (!DYNAMIC) begin
            for (j = 0; j < ENTRIES; j = j + 1) begin
              if (active_mask_q[j] && !terminal_mask[j]
                  && (control_q[j][59:52] < control_q[i][59:52]))
                static_group_ready = 1'b0;
            end
          end
          if (static_group_ready) begin
            case (control_q[i][29:28])
              ENGINE_ME: begin
                if (!cand_me_valid
                    || (DYNAMIC && (control_q[i][27:26] < cand_me_priority))) begin
                  cand_me_valid = 1'b1;
                  cand_me_index = i[2:0];
                  cand_me_priority = control_q[i][27:26];
                end
              end
              ENGINE_VE: begin
                if (!cand_ve_valid
                    || (DYNAMIC && (control_q[i][27:26] < cand_ve_priority))) begin
                  cand_ve_valid = 1'b1;
                  cand_ve_index = i[2:0];
                  cand_ve_priority = control_q[i][27:26];
                end
              end
              ENGINE_DE: begin
                if (!cand_de_valid
                    || (DYNAMIC && (control_q[i][27:26] < cand_de_priority))) begin
                  cand_de_valid = 1'b1;
                  cand_de_index = i[2:0];
                  cand_de_priority = control_q[i][27:26];
                end
              end
              default: begin end
            endcase
          end
        end
      end
    end

    cand_me_safe = !DYNAMIC || candidate_safe_from_flight(cand_me_index);
    cand_ve_safe = !DYNAMIC || candidate_safe_from_flight(cand_ve_index);
    cand_de_safe = !DYNAMIC || candidate_safe_from_flight(cand_de_index);
    if ((cand_me_valid && (me_busy || me_dispatch_valid_q || !cand_me_safe))
        || (cand_ve_valid && (ve_busy || ve_dispatch_valid_q || !cand_ve_safe))
        || (cand_de_valid && (de_busy || de_dispatch_valid_q || !cand_de_safe)))
      resource_blocked_any = 1'b1;
  end

  agentsys_matrix_engine matrix_engine (
      .clk(clk), .rst_n(rst_n), .start_i(issue_me),
      .duration_i(control_q[issue_me_index][51:36]), .seed_i(me_seed),
      .busy_o(me_busy), .done_o(me_done), .checksum_o(me_checksum),
      .busy_cycles_o(me_busy_cycles)
  );

  agentsys_simple_engine #(.KIND_MAGIC(64'h56455f5449534131)) vector_engine (
      .clk(clk), .rst_n(rst_n), .start_i(issue_ve),
      .duration_i(control_q[issue_ve_index][51:36]), .seed_i(ve_seed),
      .busy_o(ve_busy), .done_o(ve_done), .checksum_o(ve_checksum),
      .busy_cycles_o(ve_busy_cycles)
  );

  agentsys_simple_engine #(.KIND_MAGIC(64'h44455f5449534131)) data_engine (
      .clk(clk), .rst_n(rst_n), .start_i(issue_de),
      .duration_i(control_q[issue_de_index][51:36]), .seed_i(de_seed),
      .busy_o(de_busy), .done_o(de_done), .checksum_o(de_checksum),
      .busy_cycles_o(de_busy_cycles)
  );

  reg [7:0] new_cancel_mask;
  reg [63:0] completion_digest;
  reg [7:0] terminal_next;
  always @* begin
    new_cancel_mask = 8'd0;
    for (i = 0; i < ENTRIES; i = i + 1) begin
      if (pending_mask[i] && cancel_tasks_q[control_q[i][10:8]])
        new_cancel_mask[i] = 1'b1;
    end
    completion_digest = 64'd0;
    if (me_done)
      completion_digest = completion_digest ^ control_q[me_index_q]
          ^ (INCLUDE_ENGINE_CHECKSUM ? me_checksum : 64'd0);
    if (ve_done)
      completion_digest = completion_digest ^ control_q[ve_index_q]
          ^ (INCLUDE_ENGINE_CHECKSUM ? ve_checksum : 64'd0);
    if (de_done)
      completion_digest = completion_digest ^ control_q[de_index_q]
          ^ (INCLUDE_ENGINE_CHECKSUM ? de_checksum : 64'd0);
    terminal_next = terminal_mask | engine_done_mask | new_cancel_mask;
  end

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      configured_valid_q <= 8'd0;
      descriptor_count_q <= 4'd0;
      active_mask_q <= 8'd0;
      issued_mask_q <= 8'd0;
      completed_mask_q <= 8'd0;
      canceled_mask_q <= 8'd0;
      prefetched_mask_q <= 8'd0;
      cancel_tasks_q <= 8'd0;
      running_q <= 1'b0;
      done_o <= 1'b0;
      input_checksum_q <= 64'd0;
      descriptor_digest_q <= 64'd0;
      result_checksum_o <= 64'd0;
      me_index_q <= 3'd0;
      ve_index_q <= 3'd0;
      de_index_q <= 3'd0;
      me_dispatch_valid_q <= 1'b0;
      ve_dispatch_valid_q <= 1'b0;
      de_dispatch_valid_q <= 1'b0;
      me_dispatch_count_q <= 8'd0;
      ve_dispatch_count_q <= 8'd0;
      de_dispatch_count_q <= 8'd0;
      me_dispatch_index_q <= 3'd0;
      ve_dispatch_index_q <= 3'd0;
      de_dispatch_index_q <= 3'd0;
      stat_cycles_o <= 64'd0;
      stat_submitted_o <= 64'd0;
      stat_issued_o <= 64'd0;
      stat_completed_o <= 64'd0;
      stat_canceled_o <= 64'd0;
      stat_dependency_stall_o <= 64'd0;
      stat_resource_stall_o <= 64'd0;
      stat_pair_overlap_o <= 64'd0;
      stat_triple_overlap_o <= 64'd0;
      stat_decisions_o <= 64'd0;
      stat_prefetch_requests_o <= 64'd0;
      stat_prefetch_hits_o <= 64'd0;
      stat_priority_violations_o <= 64'd0;
      stat_me_issued_o <= 64'd0;
      stat_ve_issued_o <= 64'd0;
      stat_de_issued_o <= 64'd0;
      for (i = 0; i < ENTRIES; i = i + 1) begin
        control_q[i] <= 64'd0;
        tilemem_q[i] <= 64'd0;
      end
    end else begin
      done_o <= 1'b0;
      if (cfg_valid_i && !running_q) begin
        if ((cfg_target_i == TARGET_CONTROL) && (cfg_index_i < ENTRIES)) begin
          control_q[cfg_index_i[2:0]] <= cfg_word_i;
          configured_valid_q[cfg_index_i[2:0]] <= cfg_word_i[60];
        end else if ((cfg_target_i == TARGET_TILEMEM) && (cfg_index_i < ENTRIES)) begin
          tilemem_q[cfg_index_i[2:0]] <= cfg_word_i;
        end else if ((cfg_target_i == TARGET_GLOBAL) && (cfg_index_i == 0)) begin
          descriptor_count_q <= cfg_word_i[3:0];
        end
      end

      if (prefetch_valid_i) begin
        prefetched_mask_q[prefetch_index_i] <= 1'b1;
        stat_prefetch_requests_o <= stat_prefetch_requests_o + 1'b1;
      end
      if (cancel_valid_i)
        cancel_tasks_q <= cancel_tasks_q | cancel_task_mask_i;

      if (launch_i && !running_q) begin
        active_mask_q <= configured_valid_q & count_mask(descriptor_count_q);
        issued_mask_q <= 8'd0;
        completed_mask_q <= 8'd0;
        canceled_mask_q <= 8'd0;
        cancel_tasks_q <= 8'd0;
        me_dispatch_valid_q <= 1'b0;
        ve_dispatch_valid_q <= 1'b0;
        de_dispatch_valid_q <= 1'b0;
        me_dispatch_count_q <= 8'd0;
        ve_dispatch_count_q <= 8'd0;
        de_dispatch_count_q <= 8'd0;
        running_q <= 1'b1;
        input_checksum_q <= input_checksum_i;
        descriptor_digest_q <= 64'd0;
        result_checksum_o <= 64'd0;
        stat_cycles_o <= 64'd0;
        stat_submitted_o <= {{60{1'b0}},
            popcount8(configured_valid_q & count_mask(descriptor_count_q))};
        stat_issued_o <= 64'd0;
        stat_completed_o <= 64'd0;
        stat_canceled_o <= 64'd0;
        stat_dependency_stall_o <= 64'd0;
        stat_resource_stall_o <= 64'd0;
        stat_pair_overlap_o <= 64'd0;
        stat_triple_overlap_o <= 64'd0;
        stat_decisions_o <= 64'd0;
        stat_prefetch_hits_o <= 64'd0;
        stat_priority_violations_o <= 64'd0;
        stat_me_issued_o <= 64'd0;
        stat_ve_issued_o <= 64'd0;
        stat_de_issued_o <= 64'd0;
      end else if (running_q) begin
        stat_cycles_o <= stat_cycles_o + 1'b1;
        if (dependency_blocked_any)
          stat_dependency_stall_o <= stat_dependency_stall_o + 1'b1;
        if (resource_blocked_any)
          stat_resource_stall_o <= stat_resource_stall_o + 1'b1;
        if ((me_busy && ve_busy) || (me_busy && de_busy) || (ve_busy && de_busy))
          stat_pair_overlap_o <= stat_pair_overlap_o + 1'b1;
        if (me_busy && ve_busy && de_busy)
          stat_triple_overlap_o <= stat_triple_overlap_o + 1'b1;
        if (issue_mask != 0)
          stat_decisions_o <= stat_decisions_o + 1'b1;

        issued_mask_q <= issued_mask_q | issue_mask;
        completed_mask_q <= completed_mask_q | engine_done_mask;
        canceled_mask_q <= canceled_mask_q | new_cancel_mask;
        stat_issued_o <= stat_issued_o + {{60{1'b0}}, popcount8(issue_mask)};
        stat_completed_o <= stat_completed_o
            + {{60{1'b0}}, popcount8(engine_done_mask)};
        stat_canceled_o <= stat_canceled_o
            + {{60{1'b0}}, popcount8(new_cancel_mask)};
        descriptor_digest_q <= descriptor_digest_q ^ completion_digest;

        if (reserve_me) begin
          me_dispatch_valid_q <= 1'b1;
          me_dispatch_count_q <= DISPATCH_LATENCY;
          me_dispatch_index_q <= cand_me_index;
        end else if (me_dispatch_valid_q) begin
          if (issue_me) begin
            me_dispatch_valid_q <= 1'b0;
            me_dispatch_count_q <= 8'd0;
          end else begin
            me_dispatch_count_q <= me_dispatch_count_q - 1'b1;
          end
        end
        if (reserve_ve) begin
          ve_dispatch_valid_q <= 1'b1;
          ve_dispatch_count_q <= DISPATCH_LATENCY;
          ve_dispatch_index_q <= cand_ve_index;
        end else if (ve_dispatch_valid_q) begin
          if (issue_ve) begin
            ve_dispatch_valid_q <= 1'b0;
            ve_dispatch_count_q <= 8'd0;
          end else begin
            ve_dispatch_count_q <= ve_dispatch_count_q - 1'b1;
          end
        end
        if (reserve_de) begin
          de_dispatch_valid_q <= 1'b1;
          de_dispatch_count_q <= DISPATCH_LATENCY;
          de_dispatch_index_q <= cand_de_index;
        end else if (de_dispatch_valid_q) begin
          if (issue_de) begin
            de_dispatch_valid_q <= 1'b0;
            de_dispatch_count_q <= 8'd0;
          end else begin
            de_dispatch_count_q <= de_dispatch_count_q - 1'b1;
          end
        end

        if (issue_me) begin
          stat_me_issued_o <= stat_me_issued_o + 1'b1;
          me_index_q <= issue_me_index;
`ifndef SYNTHESIS
          if (TRACE)
            $display("AGENTSYS_TISA_ISSUE cycle=%0d index=%0d engine=me source=%0d flow=%0d stage=%0d placement=%0d preemptible=%0d priority=%0d duration=%0d",
                     stat_cycles_o, issue_me_index,
                     tilemem_q[issue_me_index][63:54], control_q[issue_me_index][61],
                     control_q[issue_me_index][63], control_q[issue_me_index][35:34],
                     control_q[issue_me_index][62], control_q[issue_me_index][27:26],
                     control_q[issue_me_index][51:36]);
`endif
          if (prefetched_mask_q[issue_me_index]) begin
            stat_prefetch_hits_o <= stat_prefetch_hits_o + 1'b1;
            prefetched_mask_q[issue_me_index] <= 1'b0;
          end
        end
        if (issue_ve) begin
          stat_ve_issued_o <= stat_ve_issued_o + 1'b1;
          ve_index_q <= issue_ve_index;
`ifndef SYNTHESIS
          if (TRACE)
            $display("AGENTSYS_TISA_ISSUE cycle=%0d index=%0d engine=ve source=%0d flow=%0d stage=%0d placement=%0d preemptible=%0d priority=%0d duration=%0d",
                     stat_cycles_o, issue_ve_index,
                     tilemem_q[issue_ve_index][63:54], control_q[issue_ve_index][61],
                     control_q[issue_ve_index][63], control_q[issue_ve_index][35:34],
                     control_q[issue_ve_index][62], control_q[issue_ve_index][27:26],
                     control_q[issue_ve_index][51:36]);
`endif
          if (prefetched_mask_q[issue_ve_index]) begin
            stat_prefetch_hits_o <= stat_prefetch_hits_o + 1'b1;
            prefetched_mask_q[issue_ve_index] <= 1'b0;
          end
        end
        if (issue_de) begin
          stat_de_issued_o <= stat_de_issued_o + 1'b1;
          de_index_q <= issue_de_index;
`ifndef SYNTHESIS
          if (TRACE)
            $display("AGENTSYS_TISA_ISSUE cycle=%0d index=%0d engine=de source=%0d flow=%0d stage=%0d placement=%0d preemptible=%0d priority=%0d duration=%0d",
                     stat_cycles_o, issue_de_index,
                     tilemem_q[issue_de_index][63:54], control_q[issue_de_index][61],
                     control_q[issue_de_index][63], control_q[issue_de_index][35:34],
                     control_q[issue_de_index][62], control_q[issue_de_index][27:26],
                     control_q[issue_de_index][51:36]);
`endif
          if (prefetched_mask_q[issue_de_index]) begin
            stat_prefetch_hits_o <= stat_prefetch_hits_o + 1'b1;
            prefetched_mask_q[issue_de_index] <= 1'b0;
          end
        end

`ifndef SYNTHESIS
        if (TRACE && me_done)
          $display("AGENTSYS_TISA_COMPLETE cycle=%0d index=%0d engine=me source=%0d checksum=%016x",
                   stat_cycles_o, me_index_q, tilemem_q[me_index_q][63:54], me_checksum);
        if (TRACE && ve_done)
          $display("AGENTSYS_TISA_COMPLETE cycle=%0d index=%0d engine=ve source=%0d checksum=%016x",
                   stat_cycles_o, ve_index_q, tilemem_q[ve_index_q][63:54], ve_checksum);
        if (TRACE && de_done)
          $display("AGENTSYS_TISA_COMPLETE cycle=%0d index=%0d engine=de source=%0d checksum=%016x",
                   stat_cycles_o, de_index_q, tilemem_q[de_index_q][63:54], de_checksum);
`endif

        if ((terminal_next & active_mask_q) == active_mask_q
            && !me_busy && !ve_busy && !de_busy
            && !me_dispatch_valid_q && !ve_dispatch_valid_q && !de_dispatch_valid_q
            && (issue_mask == 0)) begin
          running_q <= 1'b0;
          done_o <= 1'b1;
          result_checksum_o <= input_checksum_q ^ descriptor_digest_q
              ^ completion_digest ^ RESULT_MAGIC;
        end
      end
    end
  end
endmodule
