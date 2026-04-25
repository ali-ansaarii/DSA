MAKEFILE_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
INPUT ?= $(MAKEFILE_DIR)/inputs/input.txt
LARGE_INPUT ?= $(MAKEFILE_DIR)/inputs/input_large.txt
CHALLENGE_INPUT ?= $(MAKEFILE_DIR)/inputs/input_challenge.txt

CXX ?= c++
CXXFLAGS ?= -std=c++20 -O2 -Wall -Wextra -pedantic
CPP_BUILD_DIR := $(MAKEFILE_DIR)/cpp/build
CPP_BIN := $(CPP_BUILD_DIR)/matrix_multiplication

PYTHON ?= python3

JAVAC ?= javac
JAVA ?= java
JAVA_BUILD_DIR := $(MAKEFILE_DIR)/java/build
JAVA_STAMP := $(JAVA_BUILD_DIR)/.compiled

CARGO ?= cargo
RUST_MANIFEST := $(MAKEFILE_DIR)/rust/Cargo.toml

LOG_DIR := $(MAKEFILE_DIR)/logs

.PHONY: build build_cpp build_java build_rs run run_cpp run_py run_java run_rs benchmark_long benchmark_long_cpp benchmark_long_py benchmark_long_java benchmark_long_rs benchmark_challenge benchmark_challenge_cpp benchmark_challenge_py benchmark_challenge_java benchmark_challenge_rs clean

build: build_cpp

build_cpp: $(CPP_BIN)

$(CPP_BIN): $(MAKEFILE_DIR)/cpp/main.cpp $(MAKEFILE_DIR)/cpp/MatrixMultiplication.cpp $(MAKEFILE_DIR)/cpp/MatrixMultiplication.hpp
	@mkdir -p "$(CPP_BUILD_DIR)"
	@$(CXX) $(CXXFLAGS) "$(MAKEFILE_DIR)/cpp/main.cpp" "$(MAKEFILE_DIR)/cpp/MatrixMultiplication.cpp" -o "$(CPP_BIN)"

build_java: $(JAVA_STAMP)

$(JAVA_STAMP): $(MAKEFILE_DIR)/java/Main.java $(MAKEFILE_DIR)/java/MatrixMultiplication.java
	@mkdir -p "$(JAVA_BUILD_DIR)"
	@$(JAVAC) -d "$(JAVA_BUILD_DIR)" "$(MAKEFILE_DIR)/java/Main.java" "$(MAKEFILE_DIR)/java/MatrixMultiplication.java"
	@touch "$(JAVA_STAMP)"

build_rs:
	@$(CARGO) build --quiet --release --manifest-path "$(RUST_MANIFEST)"

run: run_cpp

run_cpp: $(CPP_BIN)
	@"$(CPP_BIN)" "$(INPUT)"

run_py:
	@$(PYTHON) "$(MAKEFILE_DIR)/python/main.py" "$(INPUT)"

run_java: $(JAVA_STAMP)
	@$(JAVA) -cp "$(JAVA_BUILD_DIR)" Main "$(INPUT)"

run_rs:
	@$(CARGO) run --quiet --release --manifest-path "$(RUST_MANIFEST)" -- "$(INPUT)"

benchmark_long: benchmark_long_cpp benchmark_long_py benchmark_long_java benchmark_long_rs

benchmark_long_cpp: $(CPP_BIN)
	@mkdir -p "$(LOG_DIR)"
	@"$(CPP_BIN)" "$(LARGE_INPUT)" --time-matrix-multiplication > "$(LOG_DIR)/cpp-long.out"

benchmark_long_py:
	@mkdir -p "$(LOG_DIR)"
	@$(PYTHON) "$(MAKEFILE_DIR)/python/main.py" "$(LARGE_INPUT)" --time-matrix-multiplication > "$(LOG_DIR)/python-long.out"

benchmark_long_java: $(JAVA_STAMP)
	@mkdir -p "$(LOG_DIR)"
	@$(JAVA) -cp "$(JAVA_BUILD_DIR)" Main "$(LARGE_INPUT)" --time-matrix-multiplication > "$(LOG_DIR)/java-long.out"

benchmark_long_rs:
	@mkdir -p "$(LOG_DIR)"
	@$(CARGO) run --quiet --release --manifest-path "$(RUST_MANIFEST)" -- "$(LARGE_INPUT)" --time-matrix-multiplication > "$(LOG_DIR)/rust-long.out"

benchmark_challenge: benchmark_challenge_cpp benchmark_challenge_py benchmark_challenge_java benchmark_challenge_rs

benchmark_challenge_cpp: $(CPP_BIN)
	@mkdir -p "$(LOG_DIR)"
	@"$(CPP_BIN)" "$(CHALLENGE_INPUT)" --time-matrix-multiplication > "$(LOG_DIR)/cpp-challenge.out"

benchmark_challenge_py:
	@mkdir -p "$(LOG_DIR)"
	@$(PYTHON) "$(MAKEFILE_DIR)/python/main.py" "$(CHALLENGE_INPUT)" --time-matrix-multiplication > "$(LOG_DIR)/python-challenge.out"

benchmark_challenge_java: $(JAVA_STAMP)
	@mkdir -p "$(LOG_DIR)"
	@$(JAVA) -cp "$(JAVA_BUILD_DIR)" Main "$(CHALLENGE_INPUT)" --time-matrix-multiplication > "$(LOG_DIR)/java-challenge.out"

benchmark_challenge_rs:
	@mkdir -p "$(LOG_DIR)"
	@$(CARGO) run --quiet --release --manifest-path "$(RUST_MANIFEST)" -- "$(CHALLENGE_INPUT)" --time-matrix-multiplication > "$(LOG_DIR)/rust-challenge.out"

clean:
	@rm -rf "$(CPP_BUILD_DIR)" "$(JAVA_BUILD_DIR)" "$(MAKEFILE_DIR)/python/__pycache__" "$(MAKEFILE_DIR)/rust/target" "$(LOG_DIR)"
