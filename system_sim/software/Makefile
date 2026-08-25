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

.PHONY: all clean dump
all: $(ELF)

$(BUILD_DIR):
	mkdir -p $@

$(ELF): agentsys_system_test.c agentsys_runtime.h | $(BUILD_DIR)
	$(GCC) $(CFLAGS) $< $(LDFLAGS) -o $@

dump: $(ELF)
	$(OBJDUMP) -D $(ELF) > $(ELF).dump

clean:
	$(RM) $(ELF) $(ELF).dump

