CXX ?= g++
CXXFLAGS ?= -std=c++20 -Wall -Wextra -Wpedantic -O2
PYTHON ?= python3
CARGO ?= cargo
JAVAC ?= javac
JAVA ?= java

MAKEFILE_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
REPO_ROOT ?= $(shell git -C "$(MAKEFILE_DIR)" rev-parse --show-toplevel 2>/dev/null || printf '%s\n' "$(MAKEFILE_DIR)")

CPP_DIR := $(MAKEFILE_DIR)/cpp
PY_DIR := $(MAKEFILE_DIR)/python
RUST_DIR := $(MAKEFILE_DIR)/rust
JAVA_DIR := $(MAKEFILE_DIR)/java
BUILD_DIR := $(CPP_DIR)/build
TARGET := binary-search-on-answer
CPP_SRC := $(CPP_DIR)/BinarySearchOnAnswer.cpp $(CPP_DIR)/main.cpp
CPP_HDR := $(CPP_DIR)/BinarySearchOnAnswer.hpp
BENCH_WRAPPER ?= $(REPO_ROOT)/scripts/benchmark_with_memory.sh
LOG_DIR := $(MAKEFILE_DIR)/logs
CPP_BUILD_LOG := $(LOG_DIR)/build_cpp.log
JAVA_BUILD_LOG := $(LOG_DIR)/build_java.log
RUST_BUILD_LOG := $(LOG_DIR)/build_rust.log
INPUT_DIR := $(MAKEFILE_DIR)/inputs
INPUT ?= $(INPUT_DIR)/input.txt
LONG_INPUT ?= $(INPUT_DIR)/input_large.txt
CHALLENGE_INPUT ?= $(INPUT_DIR)/input_challenge.txt

.PHONY: build build_cpp build_java build_rs run run_cpp run_java run_py run_rs benchmark_long benchmark_long_cpp benchmark_long_py benchmark_long_java benchmark_long_rs benchmark_challenge benchmark_challenge_cpp benchmark_challenge_py benchmark_challenge_java benchmark_challenge_rs clean

build: build_cpp

build_cpp: $(BUILD_DIR)/$(TARGET)

$(BUILD_DIR)/$(TARGET): $(CPP_SRC) $(CPP_HDR)
	@mkdir -p $(BUILD_DIR) $(LOG_DIR)
	@$(CXX) $(CXXFLAGS) $(CPP_SRC) -o $@ >$(CPP_BUILD_LOG) 2>&1 || { \
		printf 'C++ build failed. See %s\n' "$(CPP_BUILD_LOG)"; \
		exit 1; \
	}

run: run_cpp

run_cpp: build_cpp
	$(BUILD_DIR)/$(TARGET) $(INPUT)

run_py:
	$(PYTHON) $(PY_DIR)/main.py $(INPUT)

build_java: $(JAVA_DIR)/build/Main.class

$(JAVA_DIR)/build/Main.class: $(JAVA_DIR)/BinarySearchOnAnswer.java $(JAVA_DIR)/Main.java
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
	$(RUST_DIR)/target/release/binary-search-on-answer $(INPUT)

benchmark_long: benchmark_long_cpp benchmark_long_py benchmark_long_java benchmark_long_rs

benchmark_long_cpp: build_cpp
	@printf '\n[Binary Search on Answer][C++] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(BUILD_DIR)/$(TARGET) $(LONG_INPUT) --time-binary-search-on-answer

benchmark_long_py:
	@printf '\n[Binary Search on Answer][Python] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(PYTHON) $(PY_DIR)/main.py $(LONG_INPUT) --time-binary-search-on-answer

benchmark_long_java: build_java
	@printf '\n[Binary Search on Answer][Java] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(JAVA) -cp $(JAVA_DIR)/build Main $(LONG_INPUT) --time-binary-search-on-answer

benchmark_long_rs: build_rs
	@printf '\n[Binary Search on Answer][Rust] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(RUST_DIR)/target/release/binary-search-on-answer $(LONG_INPUT) --time-binary-search-on-answer

benchmark_challenge: benchmark_challenge_cpp benchmark_challenge_py benchmark_challenge_java benchmark_challenge_rs

benchmark_challenge_cpp: build_cpp
	@printf '\n[Binary Search on Answer][C++][challenge] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(BUILD_DIR)/$(TARGET) $(CHALLENGE_INPUT) --time-binary-search-on-answer

benchmark_challenge_py:
	@printf '\n[Binary Search on Answer][Python][challenge] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(PYTHON) $(PY_DIR)/main.py $(CHALLENGE_INPUT) --time-binary-search-on-answer

benchmark_challenge_java: build_java
	@printf '\n[Binary Search on Answer][Java][challenge] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(JAVA) -cp $(JAVA_DIR)/build Main $(CHALLENGE_INPUT) --time-binary-search-on-answer

benchmark_challenge_rs: build_rs
	@printf '\n[Binary Search on Answer][Rust][challenge] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(RUST_DIR)/target/release/binary-search-on-answer $(CHALLENGE_INPUT) --time-binary-search-on-answer

clean:
	@rm -rf $(BUILD_DIR) $(PY_DIR)/__pycache__ $(RUST_DIR)/target $(JAVA_DIR)/build $(LOG_DIR)
