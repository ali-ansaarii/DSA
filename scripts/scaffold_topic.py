#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from string import Template


MAKEFILE_TEMPLATE = r"""CXX ?= g++
CXXFLAGS ?= -std=c++20 -Wall -Wextra -Wpedantic -O2
PYTHON ?= python3
CARGO ?= cargo
JAVAC ?= javac
JAVA ?= java

MAKEFILE_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
REPO_ROOT ?= $(abspath $(MAKEFILE_DIR)/../..)

CPP_DIR := $(MAKEFILE_DIR)/cpp
PY_DIR := $(MAKEFILE_DIR)/python
RUST_DIR := $(MAKEFILE_DIR)/rust
JAVA_DIR := $(MAKEFILE_DIR)/java
BUILD_DIR := $(CPP_DIR)/build
TARGET := __binary_name__
CPP_SRC := $(CPP_DIR)/__algo_id__.cpp $(CPP_DIR)/main.cpp
CPP_HDR := $(CPP_DIR)/__algo_id__.hpp
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

$(JAVA_DIR)/build/Main.class: $(JAVA_DIR)/__algo_id__.java $(JAVA_DIR)/Main.java
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
	$(RUST_DIR)/target/release/__binary_name__ $(INPUT)

benchmark_long: benchmark_long_cpp benchmark_long_py benchmark_long_java benchmark_long_rs

benchmark_long_cpp: build_cpp
	@printf '\n[__display_name__][C++] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(BUILD_DIR)/$(TARGET) $(LONG_INPUT) --__time_flag__

benchmark_long_py:
	@printf '\n[__display_name__][Python] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(PYTHON) $(PY_DIR)/main.py $(LONG_INPUT) --__time_flag__

benchmark_long_java: build_java
	@printf '\n[__display_name__][Java] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(JAVA) -cp $(JAVA_DIR)/build Main $(LONG_INPUT) --__time_flag__

benchmark_long_rs: build_rs
	@printf '\n[__display_name__][Rust] %s\n' "$(LONG_INPUT)"
	@$(BENCH_WRAPPER) $(RUST_DIR)/target/release/__binary_name__ $(LONG_INPUT) --__time_flag__

benchmark_challenge: benchmark_challenge_cpp benchmark_challenge_py benchmark_challenge_java benchmark_challenge_rs

benchmark_challenge_cpp: build_cpp
	@printf '\n[__display_name__][C++][challenge] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(BUILD_DIR)/$(TARGET) $(CHALLENGE_INPUT) --__time_flag__

benchmark_challenge_py:
	@printf '\n[__display_name__][Python][challenge] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(PYTHON) $(PY_DIR)/main.py $(CHALLENGE_INPUT) --__time_flag__

benchmark_challenge_java: build_java
	@printf '\n[__display_name__][Java][challenge] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(JAVA) -cp $(JAVA_DIR)/build Main $(CHALLENGE_INPUT) --__time_flag__

benchmark_challenge_rs: build_rs
	@printf '\n[__display_name__][Rust][challenge] %s\n' "$(CHALLENGE_INPUT)"
	@$(BENCH_WRAPPER) $(RUST_DIR)/target/release/__binary_name__ $(CHALLENGE_INPUT) --__time_flag__

clean:
	@rm -rf $(BUILD_DIR) $(PY_DIR)/__pycache__ $(RUST_DIR)/target $(JAVA_DIR)/build $(LOG_DIR)
"""

PROBLEM_TEMPLATE = Template(
    """# $display_name

## What is $display_name?
TODO: explain the data structure or algorithm in one direct paragraph.

## Problem in this folder
TODO: define the concrete baseline problem solved in this topic.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
TODO: explain the invariant or key transition clearly.

## Input Format
TODO: document the exact file format shared across all language implementations.

## Time Complexity
TODO

## Space Complexity
TODO

## Why the challenge input is challenging
TODO

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
TODO
```

## Intended Output
Expected output:

```text
TODO
```
"""
)

USAGE_TEMPLATE = Template(
    """# $display_name Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case
- `inputs/input_large.txt`
  - long general benchmark input
- `inputs/input_challenge.txt`
  - algorithm-specific challenging input

## Run Commands
From this topic folder:

```bash
make run_cpp
make run_py
make run_java
make run_rs
```

Convenience alias:

```bash
make run
```

## Build Commands
```bash
make build_cpp
make build_java
make build_rs
make build
```

## Benchmark Commands
General benchmark input:

```bash
make benchmark_long
```

Algorithm-specific challenge input:

```bash
make benchmark_challenge
```

## Benchmark Scope
TODO: state exactly what the benchmark timer includes and excludes.

## Expected Small-Input Output
```text
TODO
```
"""
)

CPP_HEADER_TEMPLATE = Template(
    """#pragma once

using namespace std;

// TODO: define the algorithm-facing types for $display_name.
"""
)

CPP_IMPL_TEMPLATE = Template(
    """#include "$algo_id.hpp"

using namespace std;

// TODO: implement the core $display_name logic here.
"""
)

CPP_MAIN_TEMPLATE = Template(
    """#include "$algo_id.hpp"

#include <chrono>
#include <iostream>
#include <string>

using namespace std;

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool $time_var = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--$time_flag") {
            $time_var = true;
        } else {
            inputPath = argument;
        }
    }

    (void)inputPath;
    (void)$time_var;

    // TODO: parse input, run the algorithm, and print output.
    return 0;
}
"""
)

PY_MODULE_TEMPLATE = Template(
    """# TODO: implement the core $display_name logic here.
"""
)

PY_MAIN_TEMPLATE = Template(
    """from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    input_path = Path("inputs/input.txt")
    $time_var = False

    for argument in sys.argv[1:]:
        if argument == "--$time_flag":
            $time_var = True
        else:
            input_path = Path(argument)

    _ = input_path
    _ = $time_var

    # TODO: parse input, run the algorithm, and print output.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
"""
)

JAVA_ALGO_TEMPLATE = Template(
    """public final class $algo_id {
    private $algo_id() {}

    // TODO: implement the core $display_name logic here.
}
"""
)

JAVA_MAIN_TEMPLATE = Template(
    """import java.nio.file.Path;

public final class Main {
    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean $time_var = false;

        for (String argument : args) {
            if (argument.equals("--$time_flag")) {
                $time_var = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        if ($time_var && inputPath.toString().isEmpty()) {
            throw new IllegalStateException();
        }

        // TODO: parse input, run the algorithm, and print output.
    }
}
"""
)

RUST_CARGO_TEMPLATE = Template(
    """[package]
name = "$binary_name"
version = "0.1.0"
edition = "2021"

[profile.release]
codegen-units = 1
lto = true
"""
)

RUST_MODULE_TEMPLATE = Template(
    """// TODO: implement the core $display_name logic here.
"""
)

RUST_MAIN_TEMPLATE = Template(
    """mod $rust_module;

use std::env;

fn main() {
    let mut input_path = String::from("inputs/input.txt");
    let mut $time_var = false;

    for argument in env::args().skip(1) {
        if argument == "--$time_flag" {
            $time_var = true;
        } else {
            input_path = argument;
        }
    }

    let _ = input_path;
    let _ = $time_var;

    // TODO: parse input, run the algorithm, and print output.
}
"""
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a standard single-topic algorithm scaffold."
    )
    parser.add_argument("--topic-path", required=True, help="Repository-relative topic path.")
    parser.add_argument("--display-name", required=True, help="Human-readable topic name.")
    parser.add_argument("--algo-id", required=True, help="Algorithm file/class stem, e.g. FenwickTree.")
    parser.add_argument("--binary-name", required=True, help="Executable/cargo package name, e.g. fenwick_tree.")
    parser.add_argument("--time-flag", required=True, help="Benchmark flag name without leading dashes.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow writing into an existing topic directory if it is empty.",
    )
    return parser.parse_args()


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_plain_template(template: str, substitutions: dict[str, str]) -> str:
    rendered = template
    for key, value in substitutions.items():
        rendered = rendered.replace(f"__{key}__", value)
    return rendered


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    topic_dir = (repo_root / args.topic_path).resolve()

    try:
        topic_dir.relative_to(repo_root)
    except ValueError:
        raise SystemExit("topic path must stay inside the repository root")

    if topic_dir.exists():
        if not args.force:
            raise SystemExit(f"refusing to overwrite existing path: {topic_dir}")
        if any(topic_dir.iterdir()):
            raise SystemExit(f"refusing to scaffold into non-empty path: {topic_dir}")

    rust_module = args.binary_name
    time_var = args.time_flag.replace("-", "_")

    substitutions = {
        "display_name": args.display_name,
        "algo_id": args.algo_id,
        "binary_name": args.binary_name,
        "time_flag": args.time_flag,
        "time_var": time_var,
        "rust_module": rust_module,
    }

    files = {
        "Makefile": render_plain_template(MAKEFILE_TEMPLATE, substitutions),
        "PROBLEM.md": PROBLEM_TEMPLATE.substitute(substitutions),
        "USAGE.md": USAGE_TEMPLATE.substitute(substitutions),
        f"cpp/{args.algo_id}.hpp": CPP_HEADER_TEMPLATE.substitute(substitutions),
        f"cpp/{args.algo_id}.cpp": CPP_IMPL_TEMPLATE.substitute(substitutions),
        "cpp/main.cpp": CPP_MAIN_TEMPLATE.substitute(substitutions),
        f"python/{args.algo_id}.py": PY_MODULE_TEMPLATE.substitute(substitutions),
        "python/main.py": PY_MAIN_TEMPLATE.substitute(substitutions),
        f"java/{args.algo_id}.java": JAVA_ALGO_TEMPLATE.substitute(substitutions),
        "java/Main.java": JAVA_MAIN_TEMPLATE.substitute(substitutions),
        "rust/Cargo.toml": RUST_CARGO_TEMPLATE.substitute(substitutions),
        f"rust/src/{rust_module}.rs": RUST_MODULE_TEMPLATE.substitute(substitutions),
        "rust/src/main.rs": RUST_MAIN_TEMPLATE.substitute(substitutions),
    }

    for relative_path, content in files.items():
        write_file(topic_dir / relative_path, content)

    for relative_dir in [
        "inputs",
        "cpp/build",
        "java/build",
        "rust/src",
    ]:
        (topic_dir / relative_dir).mkdir(parents=True, exist_ok=True)

    print(f"Scaffold created at {topic_dir.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
