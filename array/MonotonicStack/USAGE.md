# Monotonic Stack Usage

## Inputs
This topic includes three input files:
- `inputs/input.txt`: the small default case used for correctness
- `inputs/input_large.txt`: a large representative workload for benchmarking
- `inputs/input_challenge.txt`: a workload designed to force heavy stack growth
  and repeated pops

The challenge input is designed to stress:
- long decreasing prefixes that keep many candidates alive
- later large values that pop many stack entries at once
- correctness around `<=` versus `<` handling

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

Benchmark the pop-heavy challenge input:

```text
make benchmark_challenge
```

Both benchmarks measure only the monotonic-stack algorithm inside `main`:
- the right-to-left scan
- stack push/pop operations
- answer construction

They do not include file parsing or result printing.
The runners expose timing through `--time-monotonic-stack`, and the shared
benchmark wrapper also reports sampled peak RSS so the memory output works on
both macOS and Linux.
