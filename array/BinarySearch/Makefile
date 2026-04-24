MAKE ?= make
BINARY_SEARCH_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
REPO_ROOT := $(abspath $(BINARY_SEARCH_DIR)/../..)
BENCH_WRAPPER := $(REPO_ROOT)/scripts/benchmark_with_memory.sh

.PHONY: run_exact_cpp run_exact_py run_exact_java run_exact_rs run_boundary_cpp run_boundary_py run_boundary_java run_boundary_rs benchmark_exact_long benchmark_exact_challenge benchmark_boundary_long benchmark_boundary_challenge clean

run_exact_cpp:
	@$(MAKE) -C exact_match REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" run_cpp

run_exact_py:
	@$(MAKE) -C exact_match REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" run_py

run_exact_java:
	@$(MAKE) -C exact_match REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" run_java

run_exact_rs:
	@$(MAKE) -C exact_match REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" run_rs

run_boundary_cpp:
	@$(MAKE) -C boundary REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" run_cpp

run_boundary_py:
	@$(MAKE) -C boundary REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" run_py

run_boundary_java:
	@$(MAKE) -C boundary REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" run_java

run_boundary_rs:
	@$(MAKE) -C boundary REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" run_rs

benchmark_exact_long:
	@$(MAKE) -C exact_match REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_long

benchmark_exact_challenge:
	@$(MAKE) -C exact_match REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_challenge

benchmark_boundary_long:
	@$(MAKE) -C boundary REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_long

benchmark_boundary_challenge:
	@$(MAKE) -C boundary REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" benchmark_challenge

clean:
	@$(MAKE) -C exact_match REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" clean
	@$(MAKE) -C boundary REPO_ROOT="$(REPO_ROOT)" BENCH_WRAPPER="$(BENCH_WRAPPER)" clean
