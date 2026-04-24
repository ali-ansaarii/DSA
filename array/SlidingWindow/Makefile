MAKE ?= make
SLIDING_WINDOW_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
REPO_ROOT := $(abspath $(SLIDING_WINDOW_DIR)/../..)
BENCH_WRAPPER := $(REPO_ROOT)/scripts/benchmark_with_memory.sh

.PHONY: benchmark_long_fixed benchmark_long_variable benchmark_long_all benchmark_challenge_fixed benchmark_challenge_variable benchmark_challenge_all clean

benchmark_long_fixed:
	@$(MAKE) -C fixed_size REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_long

benchmark_long_variable:
	@$(MAKE) -C variable_size REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_long

benchmark_long_all: benchmark_long_fixed benchmark_long_variable

benchmark_challenge_fixed:
	@$(MAKE) -C fixed_size REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_challenge

benchmark_challenge_variable:
	@$(MAKE) -C variable_size REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_challenge

benchmark_challenge_all: benchmark_challenge_fixed benchmark_challenge_variable

clean:
	@$(MAKE) -C fixed_size REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" clean
	@$(MAKE) -C variable_size REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" clean
