# Kruskal Minimum Spanning Tree Usage

## Inputs
This topic includes three input files:
- `inputs/input.txt`: the small default graph used for the basic correctness run
- `inputs/input_large.txt`: a larger sparse undirected graph for representative benchmarking
- `inputs/input_challenge.txt`: a graph with many cheap intra-block edges and slightly heavier connector edges

The challenge input is difficult because Kruskal must sort and inspect many low-weight edges that end up being rejected after components inside each block are already connected.
That stresses the edge-sorting cost plus the repeated DSU cycle checks on redundant candidate edges.

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

Benchmark the redundant-edge challenge input:

```text
make benchmark_challenge
```

Both benchmarks measure only the `KruskalMST(...)` call inside `main`, not file parsing or output printing.
That timing does include edge normalization, edge sorting, DSU operations, and MST weight accumulation performed inside `KruskalMST(...)`.
The runners expose timing through `--time-kruskal`, and the shared benchmark wrapper also reports sampled peak RSS so the memory output works on both macOS and Linux.
