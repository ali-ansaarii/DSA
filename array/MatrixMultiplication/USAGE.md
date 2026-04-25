# Matrix Multiplication Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - general benchmark input with larger square dense matrices
- `inputs/input_challenge.txt`
  - rectangular challenging input with a long shared dimension

## Folder Layout
- `cpp/`, `python/`, `java/`, and `rust/` contain the language implementations.
- `inputs/` contains shared input data and expected output.
- `logs/` is created by benchmark targets and stores benchmark result matrices.

## Run Commands
From this topic folder, run a language implementation with:

```bash
make run_cpp
make run_py
make run_java
make run_rs
```

Convenience alias, defaulting to C++:

```bash
make run
```

You can pass a different input file with `INPUT`:

```bash
make run_cpp INPUT=$PWD/inputs/input_challenge.txt
```

## Build Commands
Build compiled implementations with:

```bash
make build_cpp
make build_java
make build_rs
make build
```

`make build` is a convenience alias for `make build_cpp`. Python does not need a build step.

## Benchmark Commands
General benchmark input across all languages:

```bash
make benchmark_long
```

Algorithm-specific challenge input across all languages:

```bash
make benchmark_challenge
```

Per-language benchmark targets are also available, for example:

```bash
make benchmark_long_cpp
make benchmark_challenge_rs
```

Benchmark targets write each program's result matrix to `logs/<language>-long.out` or `logs/<language>-challenge.out`.

## Benchmark Scope
The benchmark targets invoke each language runner directly with the selected input and the `--time-matrix-multiplication` flag. That flag makes each implementation print an algorithm-only elapsed time to standard error, excluding input parsing and output formatting and wrapping only the core multiplication call.

The current benchmark targets do not use a whole-program timing or memory wrapper, so they do not report process-level memory usage.

## Expected Small-Input Output
```text
2 2
58 64
139 154
```
