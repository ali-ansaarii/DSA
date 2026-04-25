# Insertion Sort Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case containing duplicates, negative values, zero, and signed 64-bit extremes
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - longer general benchmark input with mixed positive and negative values
- `inputs/input_challenge.txt`
  - reverse-sorted input that triggers insertion sort's worst-case quadratic shifting behavior

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
The benchmark targets invoke `scripts/benchmark_with_memory.sh`, so the wrapper's wall-clock and memory measurements cover the whole program: file parsing, setup, the insertion sort call, and printing the sorted output. When `--time-insertion-sort` is passed, each implementation also reports an algorithm-only elapsed time to standard error; that internal timer covers only the call to the insertion sort function and excludes parsing and output.

## Expected Small-Input Output
```text
-9223372036854775808 -3 -3 0 1 5 5 5 7 9 42 9223372036854775807
```
