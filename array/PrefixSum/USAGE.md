# Prefix Sum Usage

## Inputs
This topic includes three input files:
- `inputs/input.txt`: the small default array and query set used for correctness
- `inputs/input_large.txt`: a large array with many representative range queries for benchmarking
- `inputs/input_challenge.txt`: a large array with alternating signs and many boundary-sensitive queries

The challenge input is designed to make off-by-one mistakes visible.
It emphasizes:
- ranges starting at `0`
- ranges ending at `n - 1`
- single-element ranges
- negative values that punish accidental assumptions about monotonic sums

## Run Commands
Run the default input:

```text
make run_cpp
make run_py
make run_java
make run_rs
```

Run a different input file:

```text
make run_cpp INPUT=inputs/input_large.txt
make run_py INPUT=inputs/input_large.txt
make run_java INPUT=inputs/input_large.txt
make run_rs INPUT=inputs/input_large.txt
```

## Benchmark Commands
Benchmark the representative long input:

```text
make benchmark_long
```

Benchmark the boundary-heavy challenge input:

```text
make benchmark_challenge
```

Both benchmarks measure the prefix-sum preprocessing plus all range-query answers inside `main`, not file parsing or output printing.
The runners expose timing through `--time-prefix-sum`, and the shared benchmark wrapper also reports sampled peak RSS so the memory output works on both macOS and Linux.
