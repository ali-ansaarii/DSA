# Matrix Multiplication Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - general benchmark input with larger square dense matrices
- `inputs/input_challenge.txt`
  - rectangular challenging input with a long shared dimension

## Folder Layout
- `classical/` contains the direct triple-loop implementation.
- `blocked/` contains the cache-blocked implementation.
- `inputs/` is shared by both variants so result formatting and parsing stay identical.

## Run Commands
From this topic folder, the default `run_*` targets execute the classical variant:

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

To run a specific variant, invoke its Makefile directly:

```bash
make -C classical run_cpp
make -C blocked run_cpp
make -C classical run_py
make -C blocked run_py
make -C classical run_java
make -C blocked run_java
make -C classical run_rs
make -C blocked run_rs
```

You can pass a different input file with `INPUT`:

```bash
make -C blocked run_cpp INPUT=$PWD/inputs/input_challenge.txt
```

## Build Commands
The parent build targets build both variants for that language:

```bash
make build_cpp
make build_java
make build_rs
make build
```

Variant-local build targets are also available:

```bash
make -C classical build_cpp
make -C blocked build_cpp
```

## Benchmark Commands
General benchmark input, across both variants and all languages:

```bash
make benchmark_long
```

Algorithm-specific challenge input, across both variants and all languages:

```bash
make benchmark_challenge
```

Per-language benchmark targets are also available, for example:

```bash
make benchmark_long_cpp
make benchmark_challenge_rs
```

## Benchmark Scope
Benchmark targets use `scripts/benchmark_with_memory.sh` to measure whole-program wall-clock time and memory from process start to exit. The `--time-matrix-multiplication` flag additionally makes each implementation print an algorithm-only elapsed time to standard error. That algorithm-only timer excludes input parsing and output formatting, and wraps only the core multiplication call.

## Expected Small-Input Output
```text
2 2
58 64
139 154
```
