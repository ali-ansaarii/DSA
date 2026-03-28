CXX ?= g++
CXXFLAGS ?= -std=c++20 -Wall -Wextra -Wpedantic -O2
PYTHON ?= python3
CARGO ?= cargo
JAVAC ?= javac
JAVA ?= java

CPP_DIR := cpp
PY_DIR := python
RUST_DIR := rust
JAVA_DIR := java
BUILD_DIR := $(CPP_DIR)/build
TARGET := dfs
CPP_SRC := $(CPP_DIR)/DFS.cpp $(CPP_DIR)/main.cpp
INPUT ?= input.txt

.PHONY: build build_cpp build_java build_rs run run_cpp run_java run_py run_rs clean

build: build_cpp

build_cpp: $(BUILD_DIR)/$(TARGET)

$(BUILD_DIR)/$(TARGET): $(CPP_SRC)
	mkdir -p $(CPP_DIR)/build
	$(CXX) $(CXXFLAGS) $^ -o $@

run: run_cpp

run_cpp: build_cpp
	$(BUILD_DIR)/$(TARGET) $(INPUT)

run_py:
	$(PYTHON) $(PY_DIR)/main.py $(INPUT)

build_java: $(JAVA_DIR)/build/Main.class

$(JAVA_DIR)/build/Main.class: $(JAVA_DIR)/DFS.java $(JAVA_DIR)/Main.java
	mkdir -p $(JAVA_DIR)/build
	$(JAVAC) -d $(JAVA_DIR)/build $^

run_java: build_java
	$(JAVA) -cp $(JAVA_DIR)/build Main $(INPUT)

build_rs: $(RUST_DIR)/target/release/dfs

$(RUST_DIR)/target/release/dfs:
	$(CARGO) build --release --manifest-path $(RUST_DIR)/Cargo.toml

run_rs: build_rs
	$(RUST_DIR)/target/release/dfs $(INPUT)

clean:
	rm -rf $(BUILD_DIR) __pycache__ $(PY_DIR)/__pycache__ $(RUST_DIR)/target $(RUST_DIR)/build $(JAVA_DIR)/build