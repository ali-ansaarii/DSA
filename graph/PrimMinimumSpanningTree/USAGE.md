# Prim Minimum Spanning Tree Usage

## Inputs
This topic includes four input files:
- `inputs/input.txt`: the small default graph used for the basic correctness run
- `inputs/input_single_node.txt`: a one-node graph used to verify the MST base case
- `inputs/input_large.txt`: a larger sparse undirected graph for representative benchmarking
- `inputs/input_challenge.txt`: a dense graph designed to create many redundant heap candidates

The challenge input is difficult because many low-cost edges remain in the heap after one endpoint has already been absorbed into the tree.
That stresses the priority-queue churn and repeated visited-node skips that appear in heap-based Prim implementations.

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

Benchmark the redundant-heap-entry challenge input:

```text
make benchmark_challenge
```

Both benchmarks measure only the `PrimMST(...)` call inside `main`, not file parsing or output printing.
That timing does include adjacency-list construction, heap operations, visited tracking, and MST weight accumulation performed inside `PrimMST(...)`.
The runners expose timing through `--time-prim`, and the shared benchmark wrapper also reports sampled peak RSS so the memory output works on both macOS and Linux.
