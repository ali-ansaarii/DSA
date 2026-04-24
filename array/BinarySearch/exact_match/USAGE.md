# Binary Search Exact Match Usage

## Shared Inputs
This binary-search topic keeps shared inputs in `../inputs/` so both variants use one source of truth:
- `../inputs/exact_input.txt`: the small default array and query set for correctness
- `../inputs/exact_input_large.txt`: a large sorted array with many hit and miss queries for representative benchmarking
- `../inputs/exact_input_challenge.txt`: a one-element array with many boundary-style queries designed to stress off-by-one handling

The challenge input is educational rather than performance-heavy.
Its goal is to expose the common edge cases where buggy exact-match binary searches fail:
- target smaller than the only element
- target equal to the only element
- target larger than the only element

## Run Commands
Run the default input:

```text
make run_cpp
make run_py
make run_java
make run_rs
```

Run a different shared input file:

```text
make run_cpp INPUT=../inputs/exact_input_large.txt
make run_py INPUT=../inputs/exact_input_large.txt
make run_java INPUT=../inputs/exact_input_large.txt
make run_rs INPUT=../inputs/exact_input_large.txt
```

## Benchmark Commands
Benchmark the representative long input:

```text
make benchmark_long
```

Benchmark the edge-case challenge input:

```text
make benchmark_challenge
```

Both benchmarks measure only the repeated `BinarySearchExact(...)` calls inside `main`, not file parsing or result printing.
The runners expose timing through `--time-exact`, and the shared benchmark wrapper also reports sampled peak RSS so the memory output works on both macOS and Linux.
