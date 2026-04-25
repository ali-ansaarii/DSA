# Segment Tree Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case
- `inputs/input_large.txt`
  - long general workload with many mixed updates and range sums
- `inputs/input_challenge.txt`
  - operation mix concentrated around power-of-two boundaries and edge ranges

## Run Commands
From this topic folder:

```bash
make run_cpp
make run_py
make run_java
make run_rs
```

Convenience alias:

```bash
make run
```

That defaults to `run_cpp`.

## Build Commands
```bash
make build_cpp
make build_java
make build_rs
make build
```

## Benchmark Commands
General benchmark input:

```bash
make benchmark_long
```

Algorithm-specific challenge input:

```bash
make benchmark_challenge
```

## Benchmark Scope
The benchmark timer measures only the segment-tree processing call in each
runner:

- building the tree from the parsed initial array
- applying updates
- answering sum queries

It excludes:

- input parsing
- output printing

So the reported time reflects the segment-tree work itself, not full program
runtime.

## Expected Small-Input Output
```text
Query sums:
15
14
10
```
