# Disjoint Set Union Usage

## Inputs
This topic includes three input files:
- `inputs/input.txt`: the small default operation set used for correctness
- `inputs/input_large.txt`: a representative large workload with chained unions, connectivity checks, and representative queries
- `inputs/input_challenge.txt`: a sequence of chain unions followed by many reverse-order `find` and `connected` queries designed to punish DSU implementations that skip path compression or union heuristics

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

Benchmark the challenge input:

```text
make benchmark_challenge
```

Both benchmarks measure only the `DisjointSetUnion(...)` operation-processing call inside `main`, not input parsing or output formatting.
The runners expose timing through `--time-dsu`, and the shared benchmark wrapper also reports sampled peak RSS so the memory output works on both macOS and Linux.
