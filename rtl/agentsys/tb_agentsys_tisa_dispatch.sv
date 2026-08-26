`timescale 1ns/1ps

module agentsys_simple_engine #(
    parameter [63:0] KIND_MAGIC = 64'd0
) (
    input wire clk,
    input wire rst_n,
    input wire start_i,
    input wire [15:0] duration_i,
    input wire [63:0] seed_i,
    output reg busy_o,
    output reg done_o,
    output reg [63:0] checksum_o,
    output reg [63:0] busy_cycles_o
);
  reg [15:0] remaining_q;
  reg [63:0] seed_q;
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      busy_o <= 1'b0;
      done_o <= 1'b0;
      checksum_o <= 64'd0;
      busy_cycles_o <= 64'd0;
      remaining_q <= 16'd0;
      seed_q <= 64'd0;
    end else begin
      done_o <= 1'b0;
      if (start_i && !busy_o) begin
        busy_o <= 1'b1;
        remaining_q <= duration_i;
        seed_q <= seed_i;
      end else if (busy_o) begin
        busy_cycles_o <= busy_cycles_o + 1'b1;
        remaining_q <= remaining_q - 1'b1;
        if (remaining_q == 1) begin
          busy_o <= 1'b0;
          done_o <= 1'b1;
          checksum_o <= seed_q ^ KIND_MAGIC;
        end
      end
    end
  end
endmodule

module agentsys_matrix_engine (
    input wire clk,
    input wire rst_n,
    input wire start_i,
    input wire [15:0] duration_i,
    input wire [63:0] seed_i,
    output wire busy_o,
    output wire done_o,
    output wire [63:0] checksum_o,
    output wire [63:0] busy_cycles_o
);
  agentsys_simple_engine #(.KIND_MAGIC(64'h4d455f5445535431)) engine (
      .clk(clk), .rst_n(rst_n), .start_i(start_i), .duration_i(duration_i),
      .seed_i(seed_i), .busy_o(busy_o), .done_o(done_o),
      .checksum_o(checksum_o), .busy_cycles_o(busy_cycles_o)
  );
endmodule

module tb_agentsys_tisa_dispatch;
  reg clk = 1'b0;
  reg rst_n = 1'b0;
  reg cfg_valid = 1'b0;
  reg [4:0] cfg_target = 5'd0;
  reg [4:0] cfg_index = 5'd0;
  reg [63:0] cfg_word = 64'd0;
  reg launch = 1'b0;
  wire static_done;
  wire dynamic_done;
  wire [63:0] static_result;
  wire [63:0] dynamic_result;
  wire [63:0] static_cycles;
  wire [63:0] dynamic_cycles;
  wire [63:0] static_issued;
  wire [63:0] dynamic_issued;
  wire [63:0] static_completed;
  wire [63:0] dynamic_completed;
  integer static_first = -1;
  integer dynamic_first = -1;
  integer static_issue_count = 0;
  integer dynamic_issue_count = 0;
  reg static_seen = 1'b0;
  reg dynamic_seen = 1'b0;

  always #5 clk = ~clk;

  function automatic [63:0] control_word;
    input [1:0] engine;
    input [7:0] tile_id;
    begin
      control_word = (64'd1 << 60) | (64'd4 << 36)
          | ({62'd0, engine} << 28) | (64'd1 << 24) | tile_id;
    end
  endfunction

  task automatic configure;
    input [4:0] target;
    input [4:0] index;
    input [63:0] word;
    begin
      @(negedge clk);
      cfg_valid = 1'b1;
      cfg_target = target;
      cfg_index = index;
      cfg_word = word;
      @(negedge clk);
      cfg_valid = 1'b0;
    end
  endtask

`define CONNECT_COMMON \
      .clk(clk), .rst_n(rst_n), .cfg_valid_i(cfg_valid), \
      .cfg_target_i(cfg_target), .cfg_index_i(cfg_index), .cfg_word_i(cfg_word), \
      .launch_i(launch), .input_checksum_i(64'h1234), \
      .cancel_valid_i(1'b0), .cancel_task_mask_i(8'd0), \
      .prefetch_valid_i(1'b0), .prefetch_index_i(3'd0), \
      .busy_o(), .stat_canceled_o(), .stat_me_busy_o(), .stat_ve_busy_o(), \
      .stat_de_busy_o(), .stat_dependency_stall_o(), .stat_resource_stall_o(), \
      .stat_pair_overlap_o(), .stat_triple_overlap_o(), .stat_decisions_o(), \
      .stat_prefetch_requests_o(), .stat_prefetch_hits_o(), \
      .stat_priority_violations_o(), .stat_me_issued_o(), .stat_ve_issued_o(), \
      .stat_de_issued_o(), .completed_mask_o(), .canceled_mask_o()

  agentsys_tisa_scheduler #(
      .DYNAMIC(0), .ENTRIES(8), .INCLUDE_ENGINE_CHECKSUM(1),
      .DISPATCH_LATENCY(7)
  ) dut_static (
      `CONNECT_COMMON,
      .done_o(static_done), .result_checksum_o(static_result),
      .stat_cycles_o(static_cycles), .stat_submitted_o(),
      .stat_issued_o(static_issued), .stat_completed_o(static_completed)
  );

  agentsys_tisa_scheduler #(
      .DYNAMIC(1), .ENTRIES(8), .INCLUDE_ENGINE_CHECKSUM(1),
      .DISPATCH_LATENCY(7)
  ) dut_dynamic (
      `CONNECT_COMMON,
      .done_o(dynamic_done), .result_checksum_o(dynamic_result),
      .stat_cycles_o(dynamic_cycles), .stat_submitted_o(),
      .stat_issued_o(dynamic_issued), .stat_completed_o(dynamic_completed)
  );

  always @(posedge clk) begin
    if (dut_static.issue_me || dut_static.issue_ve || dut_static.issue_de) begin
      if (static_first < 0)
        static_first = static_cycles;
      static_issue_count = static_issue_count + dut_static.issue_me
          + dut_static.issue_ve + dut_static.issue_de;
    end
    if (dut_dynamic.issue_me || dut_dynamic.issue_ve || dut_dynamic.issue_de) begin
      if (dynamic_first < 0)
        dynamic_first = dynamic_cycles;
      dynamic_issue_count = dynamic_issue_count + dut_dynamic.issue_me
          + dut_dynamic.issue_ve + dut_dynamic.issue_de;
    end
    if (static_done)
      static_seen = 1'b1;
    if (dynamic_done)
      dynamic_seen = 1'b1;
  end

  initial begin
    repeat (3) @(negedge clk);
    rst_n = 1'b1;
    configure(0, 0, control_word(2'd0, 0));
    configure(1, 0, 64'h0000_0000_0000_1000);
    configure(0, 1, control_word(2'd1, 1));
    configure(1, 1, 64'h0004_0000_0000_2000);
    configure(0, 2, control_word(2'd2, 2));
    configure(1, 2, 64'h0008_0000_0000_3000);
    configure(31, 0, 64'd3);
    @(negedge clk);
    launch = 1'b1;
    @(negedge clk);
    launch = 1'b0;
    wait (static_seen && dynamic_seen);
    if (static_first != 0)
      $fatal(1, "static first issue %0d != 0", static_first);
    if (dynamic_first != 7)
      $fatal(1, "dynamic first issue %0d != 7", dynamic_first);
    if (static_issue_count != 3 || dynamic_issue_count != 3)
      $fatal(1, "issue counts static=%0d dynamic=%0d", static_issue_count,
             dynamic_issue_count);
    if (static_issued != 3 || dynamic_issued != 3
        || static_completed != 3 || dynamic_completed != 3)
      $fatal(1, "scheduler accounting mismatch");
    if (static_result != dynamic_result)
      $fatal(1, "work checksum mismatch");
    $display("AGENTSYS_TISA_DISPATCH_PASS static_first=%0d dynamic_first=%0d",
             static_first, dynamic_first);
    $finish;
  end

  initial begin
    #5000;
    $fatal(1, "timeout");
  end
endmodule
