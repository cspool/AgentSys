// SPDX-License-Identifier: MIT
// Compatibility top reconstructed from the HPTPE OPT1-WS baseline top.
// The official artifact filelists and DC reports reference
// array_opt1_based/top.v, but that file is absent at pinned commit ebe4db7d.
// This wrapper preserves the released OPT1 PE interface and WS wavefront.

module top #(
    parameter A_H = 16,
    parameter B_W = 16,
    parameter WIDTH = 8,
    parameter ACC_WIDTH = 2 * WIDTH + $clog2(A_H)
) (
    input  wire                               clk,
    input  wire                               rst_n,
    input  wire                               weight_wen,
    input  wire [A_H*WIDTH-1:0]               weight_din,
    input  wire [A_H*WIDTH-1:0]               A,
    output wire [2*B_W*ACC_WIDTH-1:0]         result
);

reg [A_H*WIDTH-1:0] a_reg;
reg [A_H*WIDTH-1:0] weight_din_reg;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        a_reg <= {A_H*WIDTH{1'b0}};
        weight_din_reg <= {A_H*WIDTH{1'b0}};
    end else begin
        a_reg <= A;
        weight_din_reg <= weight_din;
    end
end

wire signed [2*ACC_WIDTH-1:0] row [0:B_W-1][0:A_H-1];
wire signed [WIDTH-1:0] col [0:B_W-1][0:A_H-1];

genvar i, j;
generate
    for (i = 0; i < B_W; i = i + 1) begin : gen_column
        for (j = 0; j < A_H; j = j + 1) begin : gen_reduction
            wire signed [WIDTH-1:0] wave_value;
            wire signed [WIDTH-1:0] wave_weight;
            wire signed [2*ACC_WIDTH-1:0] partial;

            if (i == 0) begin : gen_left_edge
                assign wave_value = a_reg[(j+1)*WIDTH-1:j*WIDTH];
                assign wave_weight = weight_din_reg[(j+1)*WIDTH-1:j*WIDTH];
            end else begin : gen_wave
                assign wave_value = col[i-1][j];
                assign wave_weight = col[i-1][j];
            end

            if (j == 0) begin : gen_zero_partial
                assign partial = {2*ACC_WIDTH{1'b0}};
            end else begin : gen_row_partial
                assign partial = row[i][j-1];
            end

            PE #(
                .WIDTH(WIDTH),
                .ACC_WIDTH(ACC_WIDTH)
            ) u_pe (
                .rst_n(rst_n),
                .clk(clk),
                .weight_wen(weight_wen),
                .weight_din(wave_weight),
                .a(wave_value),
                .partial_result(partial),
                .col(col[i][j]),
                .row(row[i][j])
            );

            if (j == A_H-1) begin : gen_output
                assign result[(i+1)*2*ACC_WIDTH-1:i*2*ACC_WIDTH] = row[i][j];
            end
        end
    end
endgenerate

endmodule
