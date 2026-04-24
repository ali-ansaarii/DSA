# Monotonic Queue Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case
- `inputs/input_large.txt`
  - long general benchmark input with many windows
- `inputs/input_challenge.txt`
  - adversarial-style input with decreasing runs, spikes, and equal plateaus

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

`build` defaults to `build_cpp`.

## Benchmark Commands
General benchmark input:

```bash
make benchmark_long
```

Algorithm-specific challenging input:

```bash
make benchmark_challenge
```

## Benchmark Scope
The benchmark timer measures only the call to the monotonic-queue algorithm in
each runner:

- input parsing is excluded
- output printing is excluded

The benchmark therefore reflects the deque-based sliding-window maximum logic
itself, not full program runtime.

## Expected Small-Input Output
```text
Window maxima: 3 3 5 5 6 7
```
