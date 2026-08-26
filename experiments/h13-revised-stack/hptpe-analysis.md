# Run 024 HPTPE standalone analysis

## Outcome

The HPTPE standalone gate passes:

- nine released RTL organizations elaborate/lint at their full default sizes;
- nine reduced-size instances execute the released dataflow protocols and pass
  302 signed INT8 GEMM/vector golden checks;
- all 26 preregistered performance/PPA endpoints are within 15%, with 0.98%
  maximum error.

## Executed RTL

| Organization | Simulator | Golden checks | Result |
|---|---|---:|---|
| OPT1 OS MAC baseline | Icarus 11 | 2 | pass |
| OPT1 compressed OS | Icarus 11 | 2 | pass |
| OPT1 WS MAC baseline | Icarus 11 | 2 | pass |
| OPT1 compressed WS | Icarus 11 | 2 | pass |
| OPT1 Cube MAC baseline | Icarus 11 | 2 | pass |
| OPT1 compressed Cube | Icarus 11 | 2 | pass |
| OPT2 same-bit-weight compressor | Verilator 5.050 | 2 | pass |
| OPT3 sparse PE | Verilator 5.050 | 256 | pass, 2.07 cycles/operand |
| OPT4C sparse column array | Verilator 5.050 | 32 | pass, 2.27 cycles/operand |

Verilator 4.034 separately lints all nine full-scale top modules. Warnings are
preserved in the result/logs: released code contains intentional width extension,
combinational carry-chain and latch-style testbench constructs, plus one implicit
`a_b_c_d` wire in the sparse encoder. No lint case has an error.

The official artifact references
`OPT1/systolic_array_ws/array_opt1_based/top.v` in its filelists and DC reports,
but that file is absent at pinned commit `ebe4db7d`. The project reconstructs only
this top-level wavefront wrapper from the released WS baseline top and OPT1 PE
interface; the actual compressed PE/Booth/CSA RTL remains the released source.
The reconstructed wrapper passes both full-scale lint and signed GEMM execution.

## Performance and PPA

The 12 successful DC operating points yield 24 frequency/area endpoints. Values
are parsed from the checked-in SAED32 reports; frequency is `1000/clock_period`.
The two sparse calculation-cycle endpoints are measured by executing RTL.

| Design | Frequency change | Cell-area change |
|---|---:|---:|
| OPT1 OS | 2.097x | 0.962x |
| OPT1 WS | 1.667x | 1.126x |
| OPT1 Cube | 1.575x | 1.054x |

OPT2 K16×N4/8/16/32 reproduces 740/740/690/666 MHz and
67,171/126,542/230,216/462,716 µm² (rounded paper values). OPT4C N16/N32
reproduces 1,724/1,694 MHz and 15,854/30,877 µm². OPT3's measured 2.07 versus
2.05 target has the largest error, 0.98%; OPT4C 2.27 versus 2.28 has 0.44%.

## Evidence boundary

The functional/cycle evidence is new execution of released RTL using open
simulators. The absolute PPA evidence is an independent parser/check of the
authors' Synopsys DC reports and SAED32 corner, not a fresh synthesis. The
checked-in `.db` does not make Synopsys DC available, so `fresh_synthesis=false`
is a hard report field.

Reduced 4×4 functional instances keep simulation fast; the exact default
16×16/32×32 tops are elaborated in the full-scale lint pass, while their PPA is
read from the corresponding full-scale reports. No simulator wall time is used
as hardware performance.

## Artifacts

- `artifacts/results/paper-hptpe-run_024.json`
- `artifacts/logs/hptpe-run_024/*.compile.log`
- `artifacts/logs/hptpe-run_024/*.run.log`
- `integrations/hptpe/rtl/opt1_ws_top.v`

Replay:

```bash
bash scripts/build_verilator5.sh
.venv/bin/python scripts/run_hptpe_reproduction.py
```
