# Selection Sort Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case with negatives and duplicates
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - longer mixed integer input for general benchmark runs
- `inputs/input_challenge.txt`
  - reverse-sorted input that stresses Selection Sort's quadratic scan behavior

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

Python does not require a build step.

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
The `benchmark_long_*` and `benchmark_challenge_*` targets run the complete program through `scripts/benchmark_with_memory.sh`, so the wrapper's wall-clock and memory measurements include process startup, input parsing, the Selection Sort call, and output. When `--time-selection-sort` is passed, each implementation also writes an `algorithm_time_ms=...` line to standard error that measures only the core Selection Sort function call after parsing and before output formatting.

## Expected Small-Input Output
```text
-10 -3 0 4 8 11 12 22 25 25 64 99
```
