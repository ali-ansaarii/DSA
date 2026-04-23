MAKE ?= make
INORDER_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
REPO_ROOT := $(abspath $(INORDER_DIR)/../../..)
BENCH_WRAPPER := $(REPO_ROOT)/scripts/benchmark_with_memory.sh

.PHONY: benchmark_long_recursive benchmark_long_iterative benchmark_long_all benchmark_challenge_recursive benchmark_challenge_iterative benchmark_challenge_all clean

benchmark_long_recursive:
	@$(MAKE) -C recursive REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_long

benchmark_long_iterative:
	@$(MAKE) -C iterative REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_long

benchmark_long_all: benchmark_long_recursive benchmark_long_iterative

benchmark_challenge_recursive:
	@$(MAKE) -C recursive REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_challenge

benchmark_challenge_iterative:
	@$(MAKE) -C iterative REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_challenge

benchmark_challenge_all: benchmark_challenge_recursive benchmark_challenge_iterative

clean:
	@$(MAKE) -C recursive REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" clean
	@$(MAKE) -C iterative REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" clean
