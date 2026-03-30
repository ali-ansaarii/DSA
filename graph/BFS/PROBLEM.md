# Breadth-First Search (BFS)

## What is BFS?
Breadth-First Search (BFS) is a way to visit all reachable nodes in a graph level by level.

BFS starts at one node, visits all of its immediate neighbors first, then visits the neighbors of those neighbors, and so on.
It uses a queue to process nodes in the order they are discovered.

## Problem in this folder
Given:
- number of nodes
- list of undirected edges
- a start node

Run iterative BFS from the start node and print traversal order.

Nodes are numbered from `0` to `n-1`.

## Input Format
- Line 1: `n m`
- Next `m` lines: `u v` (undirected edge between `u` and `v`)
- Last line: `start`

## Test Case
This is the test case currently used in `input.txt`:

```text
7 8
0 1
0 2
1 3
1 4
2 5
2 6
4 6
3 5
0
```

## Intended Output
Adjacency lists are sorted before traversal, so the BFS order is deterministic.
Nodes are visited in increasing distance from the start node, with sorted neighbors breaking ties within the same level.

Expected output:

```text
BFS traversal order: 0 1 2 3 4 5 6
```

## Large Stress Input
This topic also includes `input_large.txt` for performance testing.

It contains a complete binary tree with `1,048,575` nodes and `1,048,574` undirected edges, starting from node `0`.
This gives BFS a large but representative connected workload without being intentionally adversarial.

Run it with:

```text
make run_cpp INPUT=input_large.txt
make run_py INPUT=input_large.txt
make run_java INPUT=input_large.txt
make run_rs INPUT=input_large.txt
```

To time all four language implementations in this folder on the long input:

```text
make benchmark_long
```

This benchmark measures only the `BFS(...)` call inside `main`, not file parsing, graph construction, sorting, or output printing.
The runners expose the timing mode through an optional `--time-bfs` flag.
The benchmark wrapper also reports sampled peak RSS in kilobytes so the memory output works on both macOS and Linux.

## Challenge Input
This topic also includes `input_challenge.txt`, a star graph with `300,000` nodes and `299,999` edges.

This input is intentionally designed to stress BFS queue growth.
From the start node `0`, BFS discovers almost the entire graph in one step, creating a very wide frontier.

Run it with:

```text
make benchmark_challenge
```

This challenge benchmark also reports peak process memory through the same cross-platform wrapper.
