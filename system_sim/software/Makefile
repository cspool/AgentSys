CHIPYARD_ROOT ?= /root/chipyard
RISCV ?= $(CHIPYARD_ROOT)/esp-tools-install
GCC := $(RISCV)/bin/riscv64-unknown-elf-gcc
OBJDUMP := $(RISCV)/bin/riscv64-unknown-elf-objdump
PROJECT_ROOT := $(abspath ../..)
BUILD_DIR := $(PROJECT_ROOT)/system_sim/build/software
CFLAGS := -std=gnu99 -O2 -g -fno-common -fno-builtin-printf -Wall -Wextra \
          -I$(CHIPYARD_ROOT)/tests -I$(PROJECT_ROOT)/system_sim/software
LDFLAGS := -static -specs=htif_nano.specs
ELF := $(BUILD_DIR)/agentsys-system.riscv
TRACE_ELF := $(BUILD_DIR)/agentsys-trace-system.riscv

.PHONY: all clean dump
all: $(ELF) $(TRACE_ELF)

$(BUILD_DIR):
	mkdir -p $@

$(ELF): agentsys_system_test.c agentsys_runtime.h Makefile | $(BUILD_DIR)
	$(GCC) $(CFLAGS) $< $(LDFLAGS) -o $@

$(TRACE_ELF): agentsys_trace_system_test.c agentsys_runtime.h generated/agentsys_app_trace.h Makefile | $(BUILD_DIR)
	$(GCC) $(CFLAGS) $< $(LDFLAGS) -o $@

dump: $(ELF) $(TRACE_ELF)
	$(OBJDUMP) -D $(ELF) > $(ELF).dump
	$(OBJDUMP) -D $(TRACE_ELF) > $(TRACE_ELF).dump

clean:
	$(RM) $(ELF) $(ELF).dump $(TRACE_ELF) $(TRACE_ELF).dump
