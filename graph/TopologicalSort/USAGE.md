# Topological Sort Usage

## Inputs
This topic includes three input files:
- `inputs/input.txt`: the small default DAG used for the basic correctness run
- `inputs/input_large.txt`: a long chain-like DAG with many forward edges for representative `O(V + E)` performance benchmarking
- `inputs/input_challenge.txt`: a directed graph with a cycle designed to confirm that implementations reject non-DAG input instead of returning a misleading order

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

Run the challenge input:

```text
make benchmark_challenge
```

The long benchmark measures only the `TopologicalSort(...)` call inside `main`, not file parsing, graph construction, sorting, or output printing.
The challenge benchmark also measures the algorithm call, but it intentionally allows failure because the input contains a cycle and topological sort is defined only for DAGs.

The runners expose timing through `--time-toposort`, and the shared benchmark wrapper also reports sampled peak RSS so the memory output works on both macOS and Linux.
