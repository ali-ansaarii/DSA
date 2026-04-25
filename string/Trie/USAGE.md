# Trie Usage

## Available Inputs
- `inputs/input.txt`
  - small default correctness case covering insertion, exact search, prefix search, missing words, and the distinction between a prefix and a complete word
- `inputs/expected_output.txt`
  - exact expected output for `inputs/input.txt`, used by `scripts/verify_topic.sh`
- `inputs/input_large.txt`
  - longer general benchmark input with mixed inserts, successful lookups, failed lookups, and prefix checks
- `inputs/input_challenge.txt`
  - challenging input with many long words sharing a common prefix and near-match searches

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
The benchmark targets run the whole program through `scripts/benchmark_with_memory.sh`, so wall-clock timing and memory include process startup, input parsing, command execution, output generation, and program shutdown. When `--time-trie` is passed, each implementation also prints an algorithm-only timing line to standard error. That algorithm-only timer starts after the input file has been parsed, measures processing the command list against the trie, and excludes file parsing and output printing.

## Expected Small-Input Output
```text
true
false
true
true
true
true
false
false
true
false
true
```
