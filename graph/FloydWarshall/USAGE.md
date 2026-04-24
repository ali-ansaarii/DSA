# Floyd-Warshall Usage

## Inputs
This topic includes three input files:
- `inputs/input.txt`: the small default graph used for the basic correctness run
- `inputs/input_large.txt`: a larger weighted directed graph for representative all-pairs benchmarking
- `inputs/input_challenge.txt`: a larger acyclic graph with negative forward edges and no cycles

The challenge input is difficult in an algorithm-design sense because the graph is a DAG, so a structure-aware approach could avoid cubic work.
Floyd-Warshall does not exploit that structure and still performs the full `O(n^3)` dynamic program.
The challenge input therefore highlights the cost of choosing a general all-pairs algorithm when the graph has exploitable structure.

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

Benchmark the DAG challenge input:

```text
make benchmark_challenge
```

Both benchmarks measure only the `FloydWarshall(...)` call inside `main`, not file parsing, matrix setup, or output printing.
The runners expose timing through `--time-floyd-warshall`, and the shared benchmark wrapper also reports sampled peak RSS so the memory output works on both macOS and Linux.
