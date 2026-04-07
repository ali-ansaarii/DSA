# BFS Usage

## Inputs
This topic includes three input files:
- `input.txt`: the small default input used for the basic correctness run
- `input_large.txt`: a complete binary tree with `1,048,575` nodes and `1,048,574` undirected edges for representative performance benchmarking
- `input_challenge.txt`: a star graph with `300,000` nodes and `299,999` edges designed to stress BFS queue growth and memory pressure

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
make run_cpp INPUT=input_large.txt
make run_py INPUT=input_large.txt
make run_java INPUT=input_large.txt
make run_rs INPUT=input_large.txt
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

Both benchmarks measure only the `BFS(...)` call inside `main`, not file parsing, graph construction, sorting, or output printing.
The runners expose timing through `--time-bfs`, and the shared benchmark wrapper also reports sampled peak RSS so the memory output works on both macOS and Linux.
