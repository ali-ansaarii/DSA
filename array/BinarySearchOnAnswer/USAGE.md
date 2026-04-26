# Binary Search on Answer Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - long general benchmark input
- `inputs/input_challenge.txt`
  - algorithm-specific challenging input with a wide numeric answer range

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

To run a different input file:

```bash
make run_cpp INPUT=inputs/input_large.txt
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

Individual benchmark targets are also available, for example:

```bash
make benchmark_long_cpp
make benchmark_challenge_py
```

## Benchmark Scope
The `benchmark_*` targets run each whole program through `scripts/benchmark_with_memory.sh`, so wrapper-level timing and memory include process startup, input parsing, the algorithm call, and output. When the program receives `--time-binary-search-on-answer`, it also reports an `algorithm_time_ns` line to standard error; that measurement wraps only the core Binary Search on Answer function call and excludes parsing and output.

## Expected Small-Input Output
```text
14
```
