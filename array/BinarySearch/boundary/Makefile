CXX ?= g++
CXXFLAGS ?= -std=c++20 -Wall -Wextra -Wpedantic -O2
PYTHON ?= python3
CARGO ?= cargo
JAVAC ?= javac
JAVA ?= java

MAKEFILE_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
TOPIC_DIR := $(abspath $(MAKEFILE_DIR)/..)
REPO_ROOT ?= $(abspath $(TOPIC_DIR)/../..)

CPP_DIR := $(MAKEFILE_DIR)/cpp
PY_DIR := $(MAKEFILE_DIR)/python
RUST_DIR := $(MAKEFILE_DIR)/rust
JAVA_DIR := $(MAKEFILE_DIR)/java
BUILD_DIR := $(CPP_DIR)/build
TARGET := binary_search_boundary
CPP_SRC := $(CPP_DIR)/BoundarySearch.cpp $(CPP_DIR)/main.cpp
BENCH_WRAPPER ?= $(REPO_ROOT)/scripts/benchmark_with_memory.sh
LOG_DIR := $(MAKEFILE_DIR)/logs
CPP_BUILD_LOG := $(LOG_DIR)/build_cpp.log
JAVA_BUILD_LOG := $(LOG_DIR)/build_java.log
RUST_BUILD_LOG := $(LOG_DIR)/build_rust.log
INPUT_DIR := $(TOPIC_DIR)/inputs
INPUT ?= $(INPUT_DIR)/boundary_input.txt
LONG_INPUT ?= $(INPUT_DIR)/boundary_input_large.txt
CHALLENGE_INPUT ?= $(INPUT_DIR)/boundary_input_challenge.txt

.PHONY: build build_cpp build_java build_rs run run_cpp run_java run_py run_rs benchmark_long benchmark_long_range_halving benchmark_long_powers_of_two benchmark_long_cpp_range_halving benchmark_long_py_range_halving benchmark_long_java_range_halving benchmark_long_rs_range_halving benchmark_long_cpp_powers_of_two benchmark_long_py_powers_of_two benchmark_long_java_powers_of_two benchmark_long_rs_powers_of_two benchmark_challenge benchmark_challenge_range_halving benchmark_challenge_powers_of_two benchmark_challenge_cpp_range_halving benchmark_challenge_py_range_halving benchmark_challenge_java_range_halving benchmark_challenge_rs_range_halving benchmark_challenge_cpp_powers_of_two benchmark_challenge_py_powers_of_two benchmark_challenge_java_powers_of_two benchmark_challenge_rs_powers_of_two clean

build: build_cpp

build_cpp: $(BUILD_DIR)/$(TARGET)

$(BUILD_DIR)/$(TARGET): $(CPP_SRC)
	@mkdir -p $(BUILD_DIR) $(LOG_DIR)
	@$(CXX) $(CXXFLAGS) $^ -o $@ >$(CPP_BUILD_LOG) 2>&1 || { \
		printf 'C++ build failed. See %s\n' "$(CPP_BUILD_LOG)"; \
		exit 1; \
	}

run: run_cpp

run_cpp: build_cpp
	$(BUILD_DIR)/$(TARGET) $(INPUT)

run_py:
	$(PYTHON) $(PY_DIR)/main.py $(INPUT)

build_java: $(JAVA_DIR)/build/Main.class

$(JAVA_DIR)/build/Main.class: $(JAVA_DIR)/BoundarySearch.java $(JAVA_DIR)/Main.java
	@mkdir -p $(JAVA_DIR)/build $(LOG_DIR)
	@$(JAVAC) -d $(JAVA_DIR)/build $^ >$(JAVA_BUILD_LOG) 2>&1 || { \
		printf 'Java build failed. See %s\n' "$(JAVA_BUILD_LOG)"; \
		exit 1; \
	}

run_java: build_java
	$(JAVA) -cp $(JAVA_DIR)/build Main $(INPUT)

build_rs:
	@mkdir -p $(LOG_DIR)
	@$(CARGO) build --release --manifest-path $(RUST_DIR)/Cargo.toml >$(RUST_BUILD_LOG) 2>&1 || { \
		printf 'Rust build failed. See %s\n' "$(RUST_BUILD_LOG)"; \
		exit 1; \
	}

run_rs: build_rs
	$(RUST_DIR)/target/release/binary_search_boundary $(INPUT)

benchmark_long: benchmark_long_range_halving benchmark_long_powers_of_two

benchmark_long_range_halving: build_cpp build_java build_rs benchmark_long_cpp_range_halving benchmark_long_py_range_halving benchmark_long_java_range_halving benchmark_long_rs_range_halving

benchmark_long_powers_of_two: build_cpp build_java build_rs benchmark_long_cpp_powers_of_two benchmark_long_py_powers_of_two benchmark_long_java_powers_of_two benchmark_long_rs_powers_of_two

benchmark_long_cpp_range_halving:
	@printf '\n[Binary Search][Boundary][range-halving][C++] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(BUILD_DIR)/$(TARGET) $(LONG_INPUT) --time-range-halving

benchmark_long_py_range_halving:
	@printf '\n[Binary Search][Boundary][range-halving][Python] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(PYTHON) $(PY_DIR)/main.py $(LONG_INPUT) --time-range-halving

benchmark_long_java_range_halving:
	@printf '\n[Binary Search][Boundary][range-halving][Java] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(JAVA) -cp $(JAVA_DIR)/build Main $(LONG_INPUT) --time-range-halving

benchmark_long_rs_range_halving:
	@printf '\n[Binary Search][Boundary][range-halving][Rust] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(RUST_DIR)/target/release/binary_search_boundary $(LONG_INPUT) --time-range-halving

benchmark_long_cpp_powers_of_two:
	@printf '\n[Binary Search][Boundary][powers-of-two][C++] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(BUILD_DIR)/$(TARGET) $(LONG_INPUT) --time-powers-of-two

benchmark_long_py_powers_of_two:
	@printf '\n[Binary Search][Boundary][powers-of-two][Python] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(PYTHON) $(PY_DIR)/main.py $(LONG_INPUT) --time-powers-of-two

benchmark_long_java_powers_of_two:
	@printf '\n[Binary Search][Boundary][powers-of-two][Java] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(JAVA) -cp $(JAVA_DIR)/build Main $(LONG_INPUT) --time-powers-of-two

benchmark_long_rs_powers_of_two:
	@printf '\n[Binary Search][Boundary][powers-of-two][Rust] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(RUST_DIR)/target/release/binary_search_boundary $(LONG_INPUT) --time-powers-of-two

benchmark_challenge: benchmark_challenge_range_halving benchmark_challenge_powers_of_two

benchmark_challenge_range_halving: build_cpp build_java build_rs benchmark_challenge_cpp_range_halving benchmark_challenge_py_range_halving benchmark_challenge_java_range_halving benchmark_challenge_rs_range_halving

benchmark_challenge_powers_of_two: build_cpp build_java build_rs benchmark_challenge_cpp_powers_of_two benchmark_challenge_py_powers_of_two benchmark_challenge_java_powers_of_two benchmark_challenge_rs_powers_of_two

benchmark_challenge_cpp_range_halving:
	@printf '\n[Binary Search][Boundary][range-halving][challenge][C++] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(BUILD_DIR)/$(TARGET) $(CHALLENGE_INPUT) --time-range-halving

benchmark_challenge_py_range_halving:
	@printf '\n[Binary Search][Boundary][range-halving][challenge][Python] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(PYTHON) $(PY_DIR)/main.py $(CHALLENGE_INPUT) --time-range-halving

benchmark_challenge_java_range_halving:
	@printf '\n[Binary Search][Boundary][range-halving][challenge][Java] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(JAVA) -cp $(JAVA_DIR)/build Main $(CHALLENGE_INPUT) --time-range-halving

benchmark_challenge_rs_range_halving:
	@printf '\n[Binary Search][Boundary][range-halving][challenge][Rust] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(RUST_DIR)/target/release/binary_search_boundary $(CHALLENGE_INPUT) --time-range-halving

benchmark_challenge_cpp_powers_of_two:
	@printf '\n[Binary Search][Boundary][powers-of-two][challenge][C++] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(BUILD_DIR)/$(TARGET) $(CHALLENGE_INPUT) --time-powers-of-two

benchmark_challenge_py_powers_of_two:
	@printf '\n[Binary Search][Boundary][powers-of-two][challenge][Python] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(PYTHON) $(PY_DIR)/main.py $(CHALLENGE_INPUT) --time-powers-of-two

benchmark_challenge_java_powers_of_two:
	@printf '\n[Binary Search][Boundary][powers-of-two][challenge][Java] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(JAVA) -cp $(JAVA_DIR)/build Main $(CHALLENGE_INPUT) --time-powers-of-two

benchmark_challenge_rs_powers_of_two:
	@printf '\n[Binary Search][Boundary][powers-of-two][challenge][Rust] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(RUST_DIR)/target/release/binary_search_boundary $(CHALLENGE_INPUT) --time-powers-of-two

clean:
	@rm -rf $(BUILD_DIR) $(PY_DIR)/__pycache__ $(RUST_DIR)/target $(JAVA_DIR)/build $(LOG_DIR)
