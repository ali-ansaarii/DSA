# DFS Iterative Usage

## Shared Inputs
This DFS topic keeps shared inputs in `../inputs/` so both recursive and iterative implementations use the same files:
- `../inputs/input.txt`: the small default input used for the correctness run
- `../inputs/input_large.txt`: a complete binary tree with `2,097,151` nodes and `2,097,150` undirected edges for representative large-workload benchmarking
- `../inputs/input_path.txt`: a path graph with `200,000` nodes and `199,999` edges designed to contrast iterative DFS against recursive DFS on deep traversal shapes

The path input is useful because iterative DFS should handle it without recursion-depth risk, while recursive implementations in some languages or environments may overflow the call stack.

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

Both benchmarks measure only the `DFS(...)` call inside `main`, not file parsing, graph construction, sorting, or output printing.
The runners expose timing through `--time-dfs`, and the shared benchmark wrapper also reports sampled peak RSS so the memory output works on both macOS and Linux.

## Parent DFS Commands
From `graph/DFS/`, you can also run the parent orchestration targets:

```text
make benchmark_long_all
make benchmark_path_all
```
