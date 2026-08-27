/* verilator lint_off DECLFILENAME */

// Revised ME: the exact released HPTPE OPT1 compressed output-stationary
// 16x16 array is instantiated below. A deterministic operand stream keeps the
// bare-metal system test self-contained while exercising all 256 PEs.
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
  localparam ARRAY_H = 16;
  localparam ARRAY_W = 16;
  localparam WIDTH = 8;
  localparam ACC_WIDTH = 32;
  localparam RESULT_BITS = 2 * ARRAY_H * ARRAY_W * ACC_WIDTH;

  reg [15:0] remaining_q;
  reg [15:0] step_q;
  reg [63:0] seed_q;
  wire clear_array = start_i && !busy_o;
  wire array_rst_n = rst_n && !clear_array;
  // The released array has no clock-enable. Gate it at the wrapper so ordinary
  // Rocket control/DMA cycles do not mutate or evaluate 256 idle PEs.
  wire array_clk = clk && (busy_o || start_i);
  wire [ARRAY_H*WIDTH-1:0] array_a;
  wire [ARRAY_W*WIDTH-1:0] array_b;
  wire [RESULT_BITS-1:0] array_result;

  genvar lane;
  generate
    for (lane = 0; lane < ARRAY_H; lane = lane + 1) begin : gen_a
      wire [7:0] seed_byte = seed_q[(lane % 8)*8 +: 8];
      assign array_a[lane*8 +: 8] = seed_byte + step_q[7:0] + lane;
    end
    for (lane = 0; lane < ARRAY_W; lane = lane + 1) begin : gen_b
      wire [7:0] seed_byte = seed_q[((lane + 3) % 8)*8 +: 8];
      assign array_b[lane*8 +: 8] = seed_byte ^ step_q[7:0] ^ lane;
    end
  endgenerate

  top #(
      .A_H(ARRAY_H),
      .B_W(ARRAY_W),
      .WIDTH(WIDTH),
      .ACC_WIDTH(ACC_WIDTH)
  ) hptpe_opt1_os_array (
      // clc clears accumulation state; the local reset also clears all
      // released-array pipeline registers so descriptor results cannot depend
      // on the previous ME tile or on static/dynamic issue timing.
      .rst_n(array_rst_n),
      .clk(array_clk),
      .A(array_a),
      .B(array_b),
      .clc(clear_array),
      .result(array_result)
  );

  integer fold_index;
  reg [63:0] array_fold;
  reg [31:0] fold_sum;
  reg [31:0] fold_carry;
  always @* begin
    array_fold = seed_q ^ 64'h48505450455f4f53;
    fold_sum = 32'd0;
    fold_carry = 32'd0;
    for (fold_index = 0; fold_index < ARRAY_H*ARRAY_W; fold_index = fold_index + 1) begin
      fold_sum = array_result[fold_index*64 + 32 +: 32];
      fold_carry = array_result[fold_index*64 +: 32];
      array_fold = {array_fold[56:0], array_fold[63:57]}
          ^ {32'd0, fold_sum + fold_carry}
          ^ {{48{1'b0}}, fold_index[15:0]};
    end
  end

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      busy_o <= 1'b0;
      done_o <= 1'b0;
      checksum_o <= 64'd0;
      busy_cycles_o <= 64'd0;
      remaining_q <= 16'd0;
      step_q <= 16'd0;
      seed_q <= 64'd0;
    end else begin
      done_o <= 1'b0;
      if (start_i && !busy_o) begin
        busy_o <= 1'b1;
        remaining_q <= duration_i == 0 ? 16'd1 : duration_i;
        step_q <= 16'd0;
        seed_q <= seed_i;
      end else if (busy_o) begin
        busy_cycles_o <= busy_cycles_o + 1'b1;
        step_q <= step_q + 1'b1;
        remaining_q <= remaining_q - 1'b1;
        if (remaining_q == 16'd1) begin
          busy_o <= 1'b0;
          done_o <= 1'b1;
          checksum_o <= array_fold ^ {48'd0, step_q};
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
