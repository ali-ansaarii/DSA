# Topological Sort, DFS-based Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - larger representative DAG benchmark with layered dependencies
- `inputs/input_challenge.txt`
  - long, narrow DAG that stresses DFS depth and reverse-postorder construction

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
The benchmark targets call each complete program through `scripts/benchmark_with_memory.sh`, so wrapper measurements include process startup, input parsing, adjacency-list construction, the DFS-based topological sort call, and output. When `--time-topological-sort-dfs-based` is passed, each program also writes an `algorithm_time_ns` line to standard error that measures only the core topological-sort function call, excluding parsing and printing.

## Expected Small-Input Output
```text
Topological order:
0 2 5 1 3 4
```
