# Fixed-Size Sliding Window Usage

## Inputs
This variant includes three input files:
- `inputs/input.txt`: the small default case used for correctness
- `inputs/input_large.txt`: a large representative workload for benchmarking
- `inputs/input_challenge.txt`: a boundary-focused workload that stresses the
  first and last possible fixed windows

The challenge input is designed to expose:
- off-by-one mistakes near the final window
- incorrect window initialization
- tie-handling mistakes when many windows have similar sums

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

Both benchmarks measure only the fixed-size sliding-window algorithm inside
`main`:
- initial window construction
- all subsequent window slides

They do not include file parsing or result printing.
The runners expose timing through `--time-fixed-window`, and the shared
benchmark wrapper also reports sampled peak RSS so the memory output works on
both macOS and Linux.
