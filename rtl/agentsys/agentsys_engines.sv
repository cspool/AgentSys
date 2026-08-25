`timescale 1ns/1ps
/* verilator lint_off DECLFILENAME */

// Four-lane output-stationary integer MAC engine. The lane accumulators retain
// partial sums for the full tile, following the HPTPE OS-array organization,
// while the compact deterministic operand generator keeps the Chipyard system
// test self-contained.
module agentsys_matrix_engine (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        start_i,
    input  wire [15:0] duration_i,
    input  wire [63:0] seed_i,
    output reg         busy_o,
    output reg         done_o,
    output reg  [63:0] checksum_o,
    output reg  [63:0] busy_cycles_o
);
  reg [15:0] remaining_q;
  reg [15:0] step_q;
  reg [63:0] seed_q;
  reg [63:0] acc0_q;
  reg [63:0] acc1_q;
  reg [63:0] acc2_q;
  reg [63:0] acc3_q;

  wire [15:0] a0 = {8'd0, seed_q[7:0]} + step_q;
  wire [15:0] a1 = {8'd0, seed_q[15:8]} + step_q + 16'd1;
  wire [15:0] a2 = {8'd0, seed_q[23:16]} + step_q + 16'd2;
  wire [15:0] a3 = {8'd0, seed_q[31:24]} + step_q + 16'd3;
  wire [15:0] b0 = {8'd0, seed_q[39:32]} ^ step_q;
  wire [15:0] b1 = {8'd0, seed_q[47:40]} ^ (step_q + 16'd1);
  wire [15:0] b2 = {8'd0, seed_q[55:48]} ^ (step_q + 16'd2);
  wire [15:0] b3 = {8'd0, seed_q[63:56]} ^ (step_q + 16'd3);
  wire [31:0] product0 = a0 * b0;
  wire [31:0] product1 = a1 * b1;
  wire [31:0] product2 = a2 * b2;
  wire [31:0] product3 = a3 * b3;
  wire [63:0] final_sum = acc0_q + {32'd0, product0}
      + acc1_q + {32'd0, product1} + acc2_q + {32'd0, product2}
      + acc3_q + {32'd0, product3};

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      busy_o <= 1'b0;
      done_o <= 1'b0;
      checksum_o <= 64'd0;
      busy_cycles_o <= 64'd0;
      remaining_q <= 16'd0;
      step_q <= 16'd0;
      seed_q <= 64'd0;
      acc0_q <= 64'd0;
      acc1_q <= 64'd0;
      acc2_q <= 64'd0;
      acc3_q <= 64'd0;
    end else begin
      done_o <= 1'b0;
      if (start_i && !busy_o) begin
        busy_o <= 1'b1;
        remaining_q <= duration_i == 0 ? 16'd1 : duration_i;
        step_q <= 16'd0;
        seed_q <= seed_i;
        acc0_q <= 64'd0;
        acc1_q <= 64'd0;
        acc2_q <= 64'd0;
        acc3_q <= 64'd0;
      end else if (busy_o) begin
        busy_cycles_o <= busy_cycles_o + 1'b1;
        acc0_q <= acc0_q + {32'd0, product0};
        acc1_q <= acc1_q + {32'd0, product1};
        acc2_q <= acc2_q + {32'd0, product2};
        acc3_q <= acc3_q + {32'd0, product3};
        step_q <= step_q + 1'b1;
        remaining_q <= remaining_q - 1'b1;
        if (remaining_q == 16'd1) begin
          busy_o <= 1'b0;
          done_o <= 1'b1;
          checksum_o <= final_sum ^ seed_q ^ 64'h4d455f4f535f3031;
        end
      end
    end
  end
endmodule

module agentsys_simple_engine #(
    parameter [63:0] KIND_MAGIC = 64'h0
) (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        start_i,
    input  wire [15:0] duration_i,
    input  wire [63:0] seed_i,
    output reg         busy_o,
    output reg         done_o,
    output reg  [63:0] checksum_o,
    output reg  [63:0] busy_cycles_o
);
  reg [15:0] remaining_q;
  reg [15:0] step_q;
  reg [63:0] state_q;
  wire [63:0] mixed_state = {state_q[56:0], state_q[63:57]}
      ^ (KIND_MAGIC + {48'd0, step_q});

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      busy_o <= 1'b0;
      done_o <= 1'b0;
      checksum_o <= 64'd0;
      busy_cycles_o <= 64'd0;
      remaining_q <= 16'd0;
      step_q <= 16'd0;
      state_q <= 64'd0;
    end else begin
      done_o <= 1'b0;
      if (start_i && !busy_o) begin
        busy_o <= 1'b1;
        remaining_q <= duration_i == 0 ? 16'd1 : duration_i;
        step_q <= 16'd0;
        state_q <= seed_i ^ KIND_MAGIC;
      end else if (busy_o) begin
        busy_cycles_o <= busy_cycles_o + 1'b1;
        state_q <= mixed_state;
        step_q <= step_q + 1'b1;
        remaining_q <= remaining_q - 1'b1;
        if (remaining_q == 16'd1) begin
          busy_o <= 1'b0;
          done_o <= 1'b1;
          checksum_o <= mixed_state;
        end
      end
    end
  end
endmodule
