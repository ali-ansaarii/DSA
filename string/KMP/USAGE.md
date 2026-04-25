# KMP Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case with overlapping matches
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - long general benchmark input with repeated natural-looking pattern occurrences
- `inputs/input_challenge.txt`
  - algorithm-specific challenging input with many near-matches for naive search

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

By default these commands read `inputs/input.txt`. To use another file:

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

## Benchmark Scope
The `--time-kmp` flag measures only the core KMP search call after input parsing and before output formatting. Whole-program wall time and memory are still reported by the benchmark wrapper when `scripts/benchmark_with_memory.sh` is available.

## Expected Small-Input Output
```text
0 2 4
```
