# Kadane's Algorithm Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case with a mixed-sign array
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - longer representative mixed-sign input for general benchmarking
- `inputs/input_challenge.txt`
  - all-negative input that verifies the non-empty, all-negative-safe baseline

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

To run a specific input file:

```bash
make run_cpp INPUT=inputs/input_challenge.txt
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
When `--time-kadane` is passed, each program measures and prints `algorithm_time_ns`, which covers only the core Kadane function call. Input parsing, file I/O, setup, and output formatting are outside that in-program timer.

The Makefile benchmark targets also run the command through `scripts/benchmark_with_memory.sh` when that repository helper is available, so wrapper-reported time/memory may reflect whole-process execution in addition to the program's algorithm-only timer.

## Expected Small-Input Output
```text
maximum_sum: 10
start_index: 3
end_index: 6
subarray: 4 -1 2 5
```
