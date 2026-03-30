MAKE ?= make
DFS_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
REPO_ROOT := $(abspath $(DFS_DIR)/../..)
BENCH_WRAPPER := $(REPO_ROOT)/scripts/benchmark_with_memory.sh

.PHONY: benchmark_long_recursive benchmark_long_iterative benchmark_long_all benchmark_path_recursive benchmark_path_iterative benchmark_path_all clean

benchmark_long_recursive:
	@$(MAKE) -C recursive REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_long

benchmark_long_iterative:
	@$(MAKE) -C iterative REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_long

benchmark_long_all: benchmark_long_recursive benchmark_long_iterative

benchmark_path_recursive:
	@$(MAKE) -C recursive REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_path

benchmark_path_iterative:
	@$(MAKE) -C iterative REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_path

benchmark_path_all: benchmark_path_recursive benchmark_path_iterative

clean:
	@$(MAKE) -C recursive REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" clean
	@$(MAKE) -C iterative REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" clean
