# 2D Prefix Sum Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - longer general benchmark input with many representative rectangle shapes
- `inputs/input_challenge.txt`
  - challenging input with large signed values, boundary rectangles, and cancellation-heavy regions

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
The benchmark wrapper measures whole-program runtime and memory: process startup, input parsing, prefix-table construction, query answering, and output generation. When `--time-prefix-sum-2d` is passed, each implementation also prints an `algorithm_time_ms` line to standard error. That internal timer starts after parsing and covers only prefix-table construction plus answering all queries; it excludes file reading/parsing and final output printing.

## Expected Small-Input Output
```text
3
14
14
27
22
49
```
