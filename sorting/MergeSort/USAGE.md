# Merge Sort Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case with duplicates and signed 64-bit boundary values
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - longer general benchmark input with mixed positive, negative, duplicate, and partially ordered values
- `inputs/input_challenge.txt`
  - reverse-sorted, duplicate-heavy input with signed 64-bit extremes; it stresses merge movement, stability-preserving tie handling, and integer range handling

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
The benchmark targets run the full program through `scripts/benchmark_with_memory.sh`, so the wrapper's wall-clock and memory measurements include process startup, input parsing, the merge sort call, and output generation. When `--time-merge-sort` is passed, each implementation also prints an `merge_sort_seconds=...` line to standard error that measures only the core merge sort function call, excluding file reading, parsing, and output formatting.

## Expected Small-Input Output
```text
-9223372036854775808 -3 -3 -1 0 5 5 8 17 17 42 9223372036854775807
```
