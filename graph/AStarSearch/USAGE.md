# A* Search Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case with a shortest path length of `10`
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - larger general benchmark grid with several obstacle corridors
- `inputs/input_challenge.txt`
  - adversarial unreachable grid separated by a solid wall; intended to force A* to exhaust the reachable side before reporting `UNREACHABLE`

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

To run a non-default input, override `INPUT`:

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
The `--time-a-star-search` flag measures only the core A* function call after input parsing and grid construction are complete. It excludes file I/O, parsing, setup, and final output formatting. The topic-level benchmark wrapper may additionally report whole-process runtime and memory usage around the command invocation.

## Expected Small-Input Output
```text
Shortest path length: 10
```
