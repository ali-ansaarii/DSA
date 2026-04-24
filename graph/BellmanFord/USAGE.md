# Bellman-Ford Usage

## Inputs
This topic includes three input files:
- `inputs/input.txt`: the small default graph used for the basic correctness run
- `inputs/input_large.txt`: a larger directed graph with no negative cycles for representative benchmarking
- `inputs/input_challenge.txt`: a directed chain whose edge order intentionally forces Bellman-Ford to perform nearly all passes before converging

The challenge input is difficult because Bellman-Ford scans edges in input order.
The chain edges are listed in the reverse of the useful propagation order, so each pass advances the frontier by only one node.
That stresses the algorithm's `O(n * m)` worst-case behavior without relying on a negative cycle.

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

Benchmark the worst-case pass-order challenge input:

```text
make benchmark_challenge
```

Both benchmarks measure only the `BellmanFord(...)` call inside `main`, not file parsing, edge-list construction, or output printing.
The runners expose timing through `--time-bellman-ford`, and the shared benchmark wrapper also reports sampled peak RSS so the memory output works on both macOS and Linux.
