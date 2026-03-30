CXX ?= g++
CXXFLAGS ?= -std=c++20 -Wall -Wextra -Wpedantic -O2
PYTHON ?= python3
CARGO ?= cargo
JAVAC ?= javac
JAVA ?= java

MAKEFILE_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
REPO_ROOT ?= $(abspath $(MAKEFILE_DIR)/../../..)

CPP_DIR := $(MAKEFILE_DIR)/cpp
PY_DIR := $(MAKEFILE_DIR)/python
RUST_DIR := $(MAKEFILE_DIR)/rust
JAVA_DIR := $(MAKEFILE_DIR)/java
BUILD_DIR := $(CPP_DIR)/build
TARGET := dfs
CPP_SRC := $(CPP_DIR)/DFS.cpp $(CPP_DIR)/main.cpp
BENCH_WRAPPER ?= $(REPO_ROOT)/scripts/benchmark_with_memory.sh
LOG_DIR := $(MAKEFILE_DIR)/logs
CPP_BUILD_LOG := $(LOG_DIR)/build_cpp.log
JAVA_BUILD_LOG := $(LOG_DIR)/build_java.log
RUST_BUILD_LOG := $(LOG_DIR)/build_rust.log
INPUT_DIR := $(MAKEFILE_DIR)/../inputs
INPUT ?= $(INPUT_DIR)/input.txt
LONG_INPUT ?= $(INPUT_DIR)/input_large.txt
PATH_INPUT ?= $(INPUT_DIR)/input_path.txt

.PHONY: build build_cpp build_java build_rs run run_cpp run_java run_py run_rs benchmark_long benchmark_long_cpp benchmark_long_py benchmark_long_java benchmark_long_rs benchmark_path benchmark_path_cpp benchmark_path_py benchmark_path_java benchmark_path_rs clean

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

$(JAVA_DIR)/build/Main.class: $(JAVA_DIR)/DFS.java $(JAVA_DIR)/Main.java
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
	$(RUST_DIR)/target/release/dfs $(INPUT)

benchmark_long: build_cpp build_java build_rs benchmark_long_cpp benchmark_long_py benchmark_long_java benchmark_long_rs

benchmark_long_cpp:
	@printf '\n[recursive][C++] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(BUILD_DIR)/$(TARGET) $(LONG_INPUT) --time-dfs

benchmark_long_py:
	@printf '\n[recursive][Python] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(PYTHON) $(PY_DIR)/main.py $(LONG_INPUT) --time-dfs

benchmark_long_java:
	@printf '\n[recursive][Java] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(JAVA) -cp $(JAVA_DIR)/build Main $(LONG_INPUT) --time-dfs

benchmark_long_rs:
	@printf '\n[recursive][Rust] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(RUST_DIR)/target/release/dfs $(LONG_INPUT) --time-dfs

benchmark_path: build_cpp build_java build_rs benchmark_path_cpp benchmark_path_py benchmark_path_java benchmark_path_rs

benchmark_path_cpp:
	@printf '\n[recursive][C++][path] %s\n' "$(PATH_INPUT)"
	@$(BENCH_WRAPPER) --allow-failure $(BUILD_DIR)/$(TARGET) $(PATH_INPUT) --time-dfs

benchmark_path_py:
	@printf '\n[recursive][Python][path] %s\n' "$(PATH_INPUT)"
	@$(BENCH_WRAPPER) --allow-failure $(PYTHON) $(PY_DIR)/main.py $(PATH_INPUT) --time-dfs

benchmark_path_java:
	@printf '\n[recursive][Java][path] %s\n' "$(PATH_INPUT)"
	@$(BENCH_WRAPPER) --allow-failure $(JAVA) -cp $(JAVA_DIR)/build Main $(PATH_INPUT) --time-dfs

benchmark_path_rs:
	@printf '\n[recursive][Rust][path] %s\n' "$(PATH_INPUT)"
	@$(BENCH_WRAPPER) --allow-failure $(RUST_DIR)/target/release/dfs $(PATH_INPUT) --time-dfs

clean:
	@rm -rf $(BUILD_DIR) $(PY_DIR)/__pycache__ $(RUST_DIR)/target $(RUST_DIR)/build $(JAVA_DIR)/build $(LOG_DIR)
