# Variable-Size Sliding Window Usage

## Inputs
This variant includes three input files:
- `inputs/input.txt`: the small default case used for correctness
- `inputs/input_large.txt`: a large representative workload for benchmarking
- `inputs/input_challenge.txt`: a target-sensitive workload designed to stress
  shrink logic near the end of the array

The challenge input is designed to expose:
- forgetting to shrink repeatedly after reaching the target
- missing a best window that appears at the very end
- off-by-one errors when shrinking the left boundary

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

Benchmark the target-sensitive challenge input:

```text
make benchmark_challenge
```

Both benchmarks measure only the variable-size sliding-window algorithm inside
`main`:
- all window expansions
- all shrink steps after reaching the target

They do not include file parsing or result printing.
The runners expose timing through `--time-variable-window`, and the shared
benchmark wrapper also reports sampled peak RSS so the memory output works on
both macOS and Linux.
