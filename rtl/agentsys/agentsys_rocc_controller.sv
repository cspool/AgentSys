`timescale 1ns/1ps
/* verilator lint_off DECLFILENAME */
/* verilator lint_off UNUSED */

module AgentSysRoCCBlackBox #(
    parameter DYNAMIC = 1,
    parameter XLEN = 64,
    parameter ADDR_BITS = 40,
    parameter TAG_BITS = 6,
    parameter CMD_BITS = 5,
    parameter SIZE_BITS = 3,
    parameter DATA_BITS = 64,
    parameter DATA_BYTES = 8
) (
    input  wire                   clock,
    input  wire                   reset,
    output wire                   cmd_ready,
    input  wire                   cmd_valid,
    input  wire [6:0]             cmd_funct,
    input  wire                   cmd_xd,
    input  wire [4:0]             cmd_rd,
    input  wire [XLEN-1:0]        cmd_rs1,
    input  wire [XLEN-1:0]        cmd_rs2,
    input  wire [1:0]             cmd_dprv,
    input  wire                   resp_ready,
    output wire                   resp_valid,
    output wire [4:0]             resp_rd,
    output wire [XLEN-1:0]        resp_data,
    input  wire                   mem_req_ready,
    output wire                   mem_req_valid,
    output wire [ADDR_BITS-1:0]   mem_req_addr,
    output wire [TAG_BITS-1:0]    mem_req_tag,
    output wire [CMD_BITS-1:0]    mem_req_cmd,
    output wire [SIZE_BITS-1:0]   mem_req_size,
    output wire                   mem_req_signed,
    output wire                   mem_req_phys,
    output wire [1:0]             mem_req_dprv,
    output wire [DATA_BITS-1:0]   mem_req_data,
    output wire [DATA_BYTES-1:0]  mem_req_mask,
    input  wire                   mem_resp_valid,
    input  wire [TAG_BITS-1:0]    mem_resp_tag,
    input  wire [DATA_BITS-1:0]   mem_resp_data,
    output wire                   busy
);
  agentsys_rocc_controller #(
      .DYNAMIC(DYNAMIC), .XLEN(XLEN), .ADDR_BITS(ADDR_BITS),
      .TAG_BITS(TAG_BITS), .CMD_BITS(CMD_BITS), .SIZE_BITS(SIZE_BITS),
      .DATA_BITS(DATA_BITS), .DATA_BYTES(DATA_BYTES)
  ) controller (
      .clk(clock), .rst_n(!reset),
      .cmd_ready_o(cmd_ready), .cmd_valid_i(cmd_valid),
      .cmd_funct_i(cmd_funct), .cmd_xd_i(cmd_xd), .cmd_rd_i(cmd_rd),
      .cmd_rs1_i(cmd_rs1), .cmd_rs2_i(cmd_rs2), .cmd_dprv_i(cmd_dprv),
      .resp_ready_i(resp_ready), .resp_valid_o(resp_valid),
      .resp_rd_o(resp_rd), .resp_data_o(resp_data),
      .mem_req_ready_i(mem_req_ready), .mem_req_valid_o(mem_req_valid),
      .mem_req_addr_o(mem_req_addr), .mem_req_tag_o(mem_req_tag),
      .mem_req_cmd_o(mem_req_cmd), .mem_req_size_o(mem_req_size),
      .mem_req_signed_o(mem_req_signed), .mem_req_phys_o(mem_req_phys),
      .mem_req_dprv_o(mem_req_dprv), .mem_req_data_o(mem_req_data),
      .mem_req_mask_o(mem_req_mask), .mem_resp_valid_i(mem_resp_valid),
      .mem_resp_tag_i(mem_resp_tag), .mem_resp_data_i(mem_resp_data),
      .busy_o(busy)
  );
endmodule

module agentsys_rocc_controller #(
    parameter DYNAMIC = 1,
    parameter XLEN = 64,
    parameter ADDR_BITS = 40,
    parameter TAG_BITS = 6,
    parameter CMD_BITS = 5,
    parameter SIZE_BITS = 3,
    parameter DATA_BITS = 64,
    parameter DATA_BYTES = 8,
    parameter SPM_BEATS = 64
) (
    input  wire                  clk,
    input  wire                  rst_n,
    output reg                   cmd_ready_o,
    input  wire                  cmd_valid_i,
    input  wire [6:0]            cmd_funct_i,
    input  wire                  cmd_xd_i,
    input  wire [4:0]            cmd_rd_i,
    input  wire [XLEN-1:0]       cmd_rs1_i,
    input  wire [XLEN-1:0]       cmd_rs2_i,
    input  wire [1:0]            cmd_dprv_i,
    input  wire                  resp_ready_i,
    output reg                   resp_valid_o,
    output reg [4:0]             resp_rd_o,
    output reg [XLEN-1:0]        resp_data_o,
    input  wire                  mem_req_ready_i,
    output reg                   mem_req_valid_o,
    output reg [ADDR_BITS-1:0]   mem_req_addr_o,
    output wire [TAG_BITS-1:0]   mem_req_tag_o,
    output reg [CMD_BITS-1:0]    mem_req_cmd_o,
    output wire [SIZE_BITS-1:0]  mem_req_size_o,
    output wire                  mem_req_signed_o,
    output wire                  mem_req_phys_o,
    output wire [1:0]            mem_req_dprv_o,
    output reg [DATA_BITS-1:0]   mem_req_data_o,
    output wire [DATA_BYTES-1:0] mem_req_mask_o,
    input  wire                  mem_resp_valid_i,
    input  wire [TAG_BITS-1:0]   mem_resp_tag_i,
    input  wire [DATA_BITS-1:0]  mem_resp_data_i,
    output wire                  busy_o
);
  localparam FUNCT_CONFIG = 7'd0;
  localparam FUNCT_LAUNCH = 7'd1;
  localparam FUNCT_WAIT = 7'd2;
  localparam FUNCT_STATUS = 7'd3;
  localparam FUNCT_CANCEL = 7'd4;
  localparam FUNCT_PREFETCH = 7'd5;
  localparam FUNCT_CLEAR = 7'd6;

  localparam ST_IDLE = 4'd0;
  localparam ST_DMA_READ_REQ = 4'd1;
  localparam ST_DMA_READ_RESP = 4'd2;
  localparam ST_BACKEND_START = 4'd3;
  localparam ST_BACKEND_RUN = 4'd4;
  localparam ST_DMA_WRITE_REQ = 4'd5;
  localparam ST_DMA_WRITE_RESP = 4'd6;
  localparam ST_COMPLETE = 4'd7;

  reg [3:0] state_q;
  reg [XLEN-1:0] input_address_q;
  reg [XLEN-1:0] output_address_q;
  reg [1:0] request_dprv_q;
  reg [7:0] input_beats_q;
  reg [7:0] output_beats_q;
  reg [7:0] dma_beat_q;
  reg [63:0] input_checksum_q;
  reg [63:0] system_cycles_q;
  reg [63:0] config_commands_q;
  reg [63:0] dma_cycles_q;
  reg [63:0] dma_bytes_q;
  reg [63:0] spm_q [0:SPM_BEATS-1];

  wire command_fire = cmd_valid_i && cmd_ready_o;
  wire idle_or_complete = (state_q == ST_IDLE) || (state_q == ST_COMPLETE);
  wire [4:0] command_target = cmd_rs2_i[12:8];
  wire [4:0] command_index = cmd_rs2_i[4:0];
  wire backend_cfg_valid = command_fire && (cmd_funct_i == FUNCT_CONFIG);
  wire backend_launch = state_q == ST_BACKEND_START;
  wire backend_cancel = command_fire && (cmd_funct_i == FUNCT_CANCEL);
  wire backend_prefetch = command_fire && (cmd_funct_i == FUNCT_PREFETCH);
  wire unused_command_xd = cmd_xd_i;
  wire [TAG_BITS-1:0] unused_response_tag = mem_resp_tag_i;
  wire [ADDR_BITS-1:0] dma_byte_offset = {{(ADDR_BITS-11){1'b0}}, dma_beat_q, 3'b000};

  wire backend_busy;
  wire backend_done;
  wire [63:0] backend_checksum;
  wire [63:0] backend_stat_cycles;
  wire [63:0] backend_stat_submitted;
  wire [63:0] backend_stat_issued;
  wire [63:0] backend_stat_completed;
  wire [63:0] backend_stat_canceled;
  wire [63:0] backend_stat_me_busy;
  wire [63:0] backend_stat_ve_busy;
  wire [63:0] backend_stat_de_busy;
  wire [63:0] backend_stat_dependency_stall;
  wire [63:0] backend_stat_resource_stall;
  wire [63:0] backend_stat_pair_overlap;
  wire [63:0] backend_stat_triple_overlap;
  wire [63:0] backend_stat_decisions;
  wire [63:0] backend_stat_prefetch_requests;
  wire [63:0] backend_stat_prefetch_hits;
  wire [63:0] backend_stat_priority_violations;
  wire [63:0] backend_stat_me_issued;
  wire [63:0] backend_stat_ve_issued;
  wire [63:0] backend_stat_de_issued;
  wire [7:0] backend_completed_mask;
  wire [7:0] backend_canceled_mask;

  assign mem_req_tag_o = {TAG_BITS{1'b0}};
  assign mem_req_size_o = {{(SIZE_BITS-2){1'b0}}, 2'd3};
  assign mem_req_signed_o = 1'b0;
  assign mem_req_phys_o = 1'b0;
  assign mem_req_dprv_o = request_dprv_q;
  assign mem_req_mask_o = {DATA_BYTES{1'b1}};
  assign busy_o = !idle_or_complete;

  agentsys_tisa_scheduler #(.DYNAMIC(DYNAMIC), .ENTRIES(8)) backend (
      .clk(clk), .rst_n(rst_n),
      .cfg_valid_i(backend_cfg_valid), .cfg_target_i(command_target),
      .cfg_index_i(command_index), .cfg_word_i(cmd_rs1_i),
      .launch_i(backend_launch), .input_checksum_i(input_checksum_q),
      .trace_call_i(8'd0),
      .cancel_valid_i(backend_cancel), .cancel_task_mask_i(cmd_rs1_i[7:0]),
      .prefetch_valid_i(backend_prefetch), .prefetch_index_i(cmd_rs1_i[2:0]),
      .busy_o(backend_busy), .done_o(backend_done),
      .result_checksum_o(backend_checksum),
      .stat_cycles_o(backend_stat_cycles),
      .stat_submitted_o(backend_stat_submitted),
      .stat_issued_o(backend_stat_issued),
      .stat_completed_o(backend_stat_completed),
      .stat_canceled_o(backend_stat_canceled),
      .stat_me_busy_o(backend_stat_me_busy),
      .stat_ve_busy_o(backend_stat_ve_busy),
      .stat_de_busy_o(backend_stat_de_busy),
      .stat_dependency_stall_o(backend_stat_dependency_stall),
      .stat_resource_stall_o(backend_stat_resource_stall),
      .stat_pair_overlap_o(backend_stat_pair_overlap),
      .stat_triple_overlap_o(backend_stat_triple_overlap),
      .stat_decisions_o(backend_stat_decisions),
      .stat_prefetch_requests_o(backend_stat_prefetch_requests),
      .stat_prefetch_hits_o(backend_stat_prefetch_hits),
      .stat_priority_violations_o(backend_stat_priority_violations),
      .stat_me_issued_o(backend_stat_me_issued),
      .stat_ve_issued_o(backend_stat_ve_issued),
      .stat_de_issued_o(backend_stat_de_issued),
      .completed_mask_o(backend_completed_mask),
      .canceled_mask_o(backend_canceled_mask)
  );

  function [XLEN-1:0] status_value;
    input [4:0] index;
    begin
      case (index)
        5'd0: status_value = {{(XLEN-5){1'b0}}, DYNAMIC[0],
                              state_q == ST_COMPLETE, busy_o, idle_or_complete, backend_busy};
        5'd1: status_value = system_cycles_q;
        5'd2: status_value = config_commands_q;
        5'd3: status_value = dma_cycles_q;
        5'd4: status_value = backend_stat_cycles;
        5'd5: status_value = backend_stat_submitted;
        5'd6: status_value = backend_stat_issued;
        5'd7: status_value = backend_stat_completed;
        5'd8: status_value = backend_stat_canceled;
        5'd9: status_value = backend_stat_me_busy;
        5'd10: status_value = backend_stat_ve_busy;
        5'd11: status_value = backend_stat_de_busy;
        5'd12: status_value = backend_stat_dependency_stall;
        5'd13: status_value = backend_stat_resource_stall;
        5'd14: status_value = backend_stat_pair_overlap;
        5'd15: status_value = backend_stat_triple_overlap;
        5'd16: status_value = backend_stat_decisions;
        5'd17: status_value = backend_stat_prefetch_requests;
        5'd18: status_value = backend_stat_prefetch_hits;
        5'd19: status_value = dma_bytes_q;
        5'd20: status_value = backend_checksum;
        5'd21: status_value = backend_stat_priority_violations;
        5'd22: status_value = {{(XLEN-32){1'b0}}, 32'h41545801};
        5'd23: status_value = input_checksum_q;
        5'd24: status_value = {{(XLEN-16){1'b0}}, backend_canceled_mask,
                               backend_completed_mask};
        5'd25: status_value = backend_stat_me_issued;
        5'd26: status_value = backend_stat_ve_issued;
        5'd27: status_value = backend_stat_de_issued;
        default: status_value = {XLEN{1'b0}};
      endcase
    end
  endfunction

  always @* begin
    cmd_ready_o = 1'b0;
    resp_valid_o = 1'b0;
    resp_rd_o = cmd_rd_i;
    resp_data_o = {XLEN{1'b0}};
    if (cmd_valid_i) begin
      case (cmd_funct_i)
        FUNCT_CONFIG, FUNCT_LAUNCH, FUNCT_CLEAR: cmd_ready_o = idle_or_complete;
        FUNCT_WAIT: begin
          resp_valid_o = state_q == ST_COMPLETE;
          resp_data_o = status_value(5'd0);
          cmd_ready_o = (state_q == ST_COMPLETE) && resp_ready_i;
        end
        FUNCT_STATUS: begin
          resp_valid_o = 1'b1;
          resp_data_o = status_value(cmd_rs1_i[4:0]);
          cmd_ready_o = resp_ready_i;
        end
        FUNCT_CANCEL, FUNCT_PREFETCH: begin
          resp_valid_o = 1'b1;
          resp_data_o = {{(XLEN-1){1'b0}}, 1'b1};
          cmd_ready_o = resp_ready_i;
        end
        default: cmd_ready_o = idle_or_complete;
      endcase
    end

    mem_req_valid_o = 1'b0;
    mem_req_addr_o = {ADDR_BITS{1'b0}};
    mem_req_cmd_o = {CMD_BITS{1'b0}};
    mem_req_data_o = {DATA_BITS{1'b0}};
    if (state_q == ST_DMA_READ_REQ) begin
      mem_req_valid_o = 1'b1;
      mem_req_addr_o = input_address_q[ADDR_BITS-1:0] + dma_byte_offset;
      mem_req_cmd_o = {CMD_BITS{1'b0}};
    end else if (state_q == ST_DMA_WRITE_REQ) begin
      mem_req_valid_o = 1'b1;
      mem_req_addr_o = output_address_q[ADDR_BITS-1:0] + dma_byte_offset;
      mem_req_cmd_o = {{(CMD_BITS-1){1'b0}}, 1'b1};
      mem_req_data_o = backend_checksum ^ {{56{1'b0}}, dma_beat_q};
    end
  end

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state_q <= ST_IDLE;
      input_address_q <= {XLEN{1'b0}};
      output_address_q <= {XLEN{1'b0}};
      request_dprv_q <= 2'd0;
      input_beats_q <= 8'd0;
      output_beats_q <= 8'd0;
      dma_beat_q <= 8'd0;
      input_checksum_q <= 64'd0;
      system_cycles_q <= 64'd0;
      config_commands_q <= 64'd0;
      dma_cycles_q <= 64'd0;
      dma_bytes_q <= 64'd0;
    end else begin
      if (busy_o)
        system_cycles_q <= system_cycles_q + 1'b1;
      if ((state_q == ST_DMA_READ_REQ) || (state_q == ST_DMA_READ_RESP)
          || (state_q == ST_DMA_WRITE_REQ) || (state_q == ST_DMA_WRITE_RESP))
        dma_cycles_q <= dma_cycles_q + 1'b1;

      if (command_fire && (cmd_funct_i == FUNCT_CONFIG)) begin
        config_commands_q <= config_commands_q + 1'b1;
        if (command_target == 5'd31) begin
          case (command_index)
            5'd1: input_beats_q <= cmd_rs1_i[7:0];
            5'd2: output_beats_q <= cmd_rs1_i[7:0];
            default: begin end
          endcase
        end
      end

      if (command_fire && (cmd_funct_i == FUNCT_CLEAR)) begin
        state_q <= ST_IDLE;
        system_cycles_q <= 64'd0;
        dma_cycles_q <= 64'd0;
        dma_bytes_q <= 64'd0;
        input_checksum_q <= 64'd0;
      end else if (command_fire && (cmd_funct_i == FUNCT_LAUNCH)) begin
        input_address_q <= cmd_rs1_i;
        output_address_q <= cmd_rs2_i;
        request_dprv_q <= cmd_dprv_i;
        dma_beat_q <= 8'd0;
        input_checksum_q <= 64'd0;
        system_cycles_q <= 64'd0;
        dma_cycles_q <= 64'd0;
        dma_bytes_q <= 64'd0;
        state_q <= (input_beats_q == 0) ? ST_BACKEND_START : ST_DMA_READ_REQ;
      end else begin
        case (state_q)
          ST_DMA_READ_REQ: begin
            if (mem_req_valid_o && mem_req_ready_i)
              state_q <= ST_DMA_READ_RESP;
          end
          ST_DMA_READ_RESP: begin
            if (mem_resp_valid_i) begin
              spm_q[dma_beat_q[5:0]] <= mem_resp_data_i;
              input_checksum_q <= input_checksum_q ^ mem_resp_data_i;
              dma_bytes_q <= dma_bytes_q + DATA_BYTES;
              if (dma_beat_q + 1'b1 == input_beats_q) begin
                dma_beat_q <= 8'd0;
                state_q <= ST_BACKEND_START;
              end else begin
                dma_beat_q <= dma_beat_q + 1'b1;
                state_q <= ST_DMA_READ_REQ;
              end
            end
          end
          ST_BACKEND_START: state_q <= ST_BACKEND_RUN;
          ST_BACKEND_RUN: begin
            if (backend_done) begin
              dma_beat_q <= 8'd0;
              state_q <= (output_beats_q == 0) ? ST_COMPLETE : ST_DMA_WRITE_REQ;
            end
          end
          ST_DMA_WRITE_REQ: begin
            if (mem_req_valid_o && mem_req_ready_i)
              state_q <= ST_DMA_WRITE_RESP;
          end
          ST_DMA_WRITE_RESP: begin
            if (mem_resp_valid_i) begin
              dma_bytes_q <= dma_bytes_q + DATA_BYTES;
              if (dma_beat_q + 1'b1 == output_beats_q) begin
                dma_beat_q <= 8'd0;
                state_q <= ST_COMPLETE;
`ifndef SYNTHESIS
                $display("AGENTSYS_SYSTEM_DONE dynamic=%0d system=%0d dma=%0d backend=%0d submitted=%0d completed=%0d canceled=%0d overlap=%0d checksum=%016x bytes=%0d",
                         DYNAMIC, system_cycles_q, dma_cycles_q,
                         backend_stat_cycles, backend_stat_submitted,
                         backend_stat_completed, backend_stat_canceled,
                         backend_stat_pair_overlap, backend_checksum,
                         dma_bytes_q + DATA_BYTES);
`endif
              end else begin
                dma_beat_q <= dma_beat_q + 1'b1;
                state_q <= ST_DMA_WRITE_REQ;
              end
            end
          end
          default: begin end
        endcase
      end
    end
  end
endmodule
