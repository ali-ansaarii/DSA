# Shortest Path in DAG Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case with a negative edge and several competing paths
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - long general benchmark input with many forward edges in a DAG
- `inputs/input_challenge.txt`
  - challenging case with negative weights, unreachable vertices, and long dependency chains

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
The benchmark targets execute the whole program through `scripts/benchmark_with_memory.sh`, so process startup, input parsing, output formatting, and memory usage are included in the wrapper's measurement. When `--time-shortest-path-in-dag` is passed, each implementation also prints an `algorithm_ms` line to standard error that measures only the core topological-order shortest-path function call; parsing and output are excluded from that internal timer.

## Expected Small-Input Output
```text
0 5 3 10 7 5
```
