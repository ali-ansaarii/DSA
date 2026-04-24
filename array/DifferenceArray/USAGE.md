# Difference Array Usage

## Inputs
This topic includes three input files:
- `inputs/input.txt`: the small default case used for correctness
- `inputs/input_large.txt`: a large representative workload for benchmarking
- `inputs/input_challenge.txt`: a boundary-heavy workload designed to expose
  off-by-one mistakes in range updates

The challenge input is designed to stress:
- updates starting at `0`
- updates ending at `n - 1`
- single-element updates
- positive and negative deltas mixed together

Those cases are where incorrect `right + 1` handling usually breaks.

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

Both benchmarks measure the difference-array algorithm work inside `main`:
- building the difference array
- applying all updates
- reconstructing the final array

They do not include file parsing or final-array printing.
The runners expose timing through `--time-difference-array`, and the shared
benchmark wrapper also reports sampled peak RSS so the memory output works on
both macOS and Linux.
