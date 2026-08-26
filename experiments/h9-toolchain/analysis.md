# H9 analysis: complete pinned toolchain and serial reproduction

Run 015 executes the complete registered pipeline from source commit `98b9ebee760f2c09c49607c78eb53a2dc335f608`.

- Full `scripts/setup_toolchain.sh` entry completed successfully (4.69 s with valid incremental build reuse); its built-level preflight is 9/9 gates.
- Serial stages: 8/8 pass in the exact registered order.
- Adjacent timing intervals do not overlap; `serial_order=true`.
- Stage wall times are 18.182 s (direct paper), 0.056 s (Agentix aggregate), 0.064 s (ATX aggregate), 0.222 s (mllm), 7.098 s (full stack), 1.652 s (Ramulator2), 1.347 s (ablations), and 62.683 s (Chipyard).
- Full toolchain audit: 11/11 gates, including exact Python packages, nine system tools, six pinned source revisions, two applied compatibility patches, four fresh build outputs, four source-identical Chipyard overlays, all stage artifacts, and the serial manifest.
- Run 016 certificate: 13/13 requirements, 55/55 paper endpoints, maximum relative error 8.33%, fresh 25-test pytest, and Verilator RTL lint.

The result supports H9: setup, build, component execution, real simulator execution, artifact verification and final certification now form one machine-executable path. The evidence classifications are unchanged; a complete toolchain does not upgrade parameterized paper replay into original-hardware measurement.
