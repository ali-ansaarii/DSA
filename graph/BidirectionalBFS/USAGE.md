# Bidirectional BFS Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case with a reachable target
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - longer general benchmark input with many redundant edges and a short source-to-target route
- `inputs/input_challenge.txt`
  - unreachable-target challenge input with source and target in different components

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
The benchmark targets run the whole program through `scripts/benchmark_with_memory.sh`, so the wrapper measures process-level runtime and memory including startup, input parsing, graph construction, the algorithm call, and output. When `--time-bidirectional-bfs` is passed, each implementation also writes `algorithm_time_ns: <value>` to standard error; that internal timer covers only the core Bidirectional BFS function call and excludes parsing, graph construction, and final output formatting.

## Expected Small-Input Output
```text
distance: 4
path: 0 1 3 4 8
```
