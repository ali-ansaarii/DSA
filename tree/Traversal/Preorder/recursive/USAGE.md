# Preorder Recursive Usage

## Shared Inputs
This preorder topic keeps shared inputs in `../inputs/` so both recursive and iterative implementations use the same files:
- `../inputs/input.txt`: the small default tree used for the correctness run
- `../inputs/input_large.txt`: a complete binary tree with `1,048,575` nodes for representative traversal benchmarking
- `../inputs/input_challenge.txt`: a left-skewed tree with `200,000` nodes designed to stress recursion depth

The challenge input is intentionally adversarial for recursive preorder traversal.
Unlike the balanced-tree workload, it forces recursion depth to grow linearly with the number of nodes, so some languages or environments may hit recursion limits or stack exhaustion.

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

Benchmark the deep skewed-tree input:

```text
make benchmark_challenge
```

The challenge benchmark is intentionally allowed to continue even if some recursive implementations fail because of recursion-depth or stack limits.
Both benchmarks measure only the `PreorderTraversal(...)` call inside `main`, not file parsing, tree construction, or output printing.
The runners expose timing through `--time-preorder`, and the shared benchmark wrapper also reports sampled peak RSS so the memory output works on both macOS and Linux.

## Parent Preorder Commands
From `tree/Traversal/Preorder/`, you can also run the parent orchestration targets:

```text
make benchmark_long_all
make benchmark_challenge_all
```
