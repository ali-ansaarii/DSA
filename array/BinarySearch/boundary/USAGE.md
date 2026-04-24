# Binary Search Boundary Usage

## Shared Inputs
This binary-search topic keeps shared inputs in `../inputs/` so both variants use one source of truth:
- `../inputs/boundary_input.txt`: the small default array and query set for correctness
- `../inputs/boundary_input_large.txt`: a large strictly increasing array with many queries for representative benchmarking
- `../inputs/boundary_input_challenge.txt`: a large array with repeated plateaus and many boundary-sensitive queries

The challenge input is designed to stress correctness on duplicates.
Buggy lower-bound implementations often return:
- the wrong position inside a plateau
- the first value strictly greater than the target
- or an off-by-one answer near the ends

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
make run_cpp INPUT=../inputs/boundary_input_large.txt
make run_py INPUT=../inputs/boundary_input_large.txt
make run_java INPUT=../inputs/boundary_input_large.txt
make run_rs INPUT=../inputs/boundary_input_large.txt
```

## Benchmark Commands
Benchmark the representative long input with both methods:

```text
make benchmark_long
```

Benchmark the duplicates-heavy challenge input with both methods:

```text
make benchmark_challenge
```

If you want just one method, use the explicit targets:

```text
make benchmark_long_range_halving
make benchmark_long_powers_of_two
make benchmark_challenge_range_halving
make benchmark_challenge_powers_of_two
```

All benchmarks measure only the repeated boundary-search calls inside `main`, not file parsing or output printing.
The runners expose timing through `--time-range-halving` and `--time-powers-of-two`, and the shared benchmark wrapper also reports sampled peak RSS so the memory output works on both macOS and Linux.
