# DFS Recursive Usage

## Shared Inputs
This DFS topic keeps shared inputs in `../inputs/` so both recursive and iterative implementations use the same files:
- `../inputs/input.txt`: the small default input used for the correctness run
- `../inputs/input_large.txt`: a complete binary tree with `2,097,151` nodes and `2,097,150` undirected edges for representative large-workload benchmarking
- `../inputs/input_path.txt`: a path graph with `200,000` nodes and `199,999` edges designed to stress recursive depth overhead

The path input is intentionally adversarial for recursive DFS.
Unlike the balanced-tree workload, it forces recursion depth to grow with the number of nodes, so some languages or environments may hit recursion limits or stack exhaustion.

## Run Commands
Run the default input:

```text
make run_cpp
make run_py
make run_java
make run_rs
```

Run a different shared input file:

```text
make run_cpp INPUT=../inputs/input_large.txt
make run_py INPUT=../inputs/input_large.txt
make run_java INPUT=../inputs/input_large.txt
make run_rs INPUT=../inputs/input_large.txt
```

## Benchmark Commands
Benchmark the representative balanced-tree input:

```text
make benchmark_long
```

Benchmark the deep path input:

```text
make benchmark_path
```

The path benchmark is intentionally allowed to continue even if some recursive implementations fail because of recursion-depth or stack limits.
Both benchmarks measure only the `DFS(...)` call inside `main`, not file parsing, graph construction, sorting, or output printing.
The runners expose timing through `--time-dfs`, and the shared benchmark wrapper also reports sampled peak RSS so the memory output works on both macOS and Linux.

## Parent DFS Commands
From `graph/DFS/`, you can also run the parent orchestration targets:

```text
make benchmark_long_all
make benchmark_path_all
```
