# Dijkstra Usage

## Inputs
This topic includes three input files:
- `inputs/input.txt`: the small default weighted graph used for the basic correctness run
- `inputs/input_large.txt`: a weighted undirected 400x400 grid with `160,000` nodes and `319,200` edges for representative sparse-graph benchmarking
- `inputs/input_challenge.txt`: a weighted graph with `220,000` nodes and `439,998` edges designed to create many stale priority-queue entries

The challenge input works by giving the source a direct but poor edge to every other node while a light chain keeps discovering better paths later.
That forces the heap to accumulate many entries that are no longer optimal by the time they are popped.

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

Benchmark the stale-priority-queue challenge input:

```text
make benchmark_challenge
```

Both benchmarks measure only the `Dijkstra(...)` call inside `main`, not file parsing, graph construction, or output printing.
The runners expose timing through `--time-dijkstra`, and the shared benchmark wrapper also reports sampled peak RSS so the memory output works on both macOS and Linux.
