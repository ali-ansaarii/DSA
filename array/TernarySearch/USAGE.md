# Ternary Search Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case with an interior maximum
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - longer general benchmark input; values increase from `0` to `100` and then decrease to `0`
- `inputs/input_challenge.txt`
  - algorithm-specific challenging input with the maximum at the left boundary

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
The benchmark targets call each runner with `--time-ternary-search`. The timing line printed by the program measures only the core ternary-search function call. It excludes file parsing, input-array allocation, command-line processing, and final output formatting. The external benchmark wrapper may also report whole-program wall time and memory usage.

## Expected Small-Input Output
```text
Maximum index: 4
Maximum value: 17
```
