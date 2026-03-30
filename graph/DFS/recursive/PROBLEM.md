# Depth-First Search (DFS) - Plain Explanation

## What is DFS?
Depth-First Search (DFS) is a way to visit all nodes in a graph.

Think of a graph as cities (nodes) connected by roads (edges).
DFS starts at one city and keeps moving forward to an unvisited neighboring city as far as possible.
When it cannot go further, it goes back (backtracks) to the previous city and tries another path.

So DFS behavior is:
1. Visit current node.
2. Go to an unvisited neighbor.
3. Repeat until stuck.
4. Backtrack and continue with the next unvisited neighbor.

## Problem in this folder
Given:
- number of nodes
- list of undirected edges
- a start node

Run recursive DFS from the start node and print traversal order.

Nodes are numbered from `0` to `n-1`.

## Input Format
- Line 1: `n m`
- Next `m` lines: `u v` (undirected edge between `u` and `v`)
- Last line: `start`

## Shared Inputs
This DFS topic now keeps shared inputs in `../inputs/` so both recursive and iterative implementations use the same files:
- `../inputs/input.txt`
- `../inputs/input_large.txt`
- `../inputs/input_path.txt`

## Test Case
This is the test case currently used in `../inputs/input.txt`:

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
Because adjacency lists are sorted before DFS, traversal is deterministic.
Expected output:

```text
DFS traversal order: 0 1 3 5 2 6 4
```

## Large Stress Input
This topic also includes `../inputs/input_large.txt` for performance testing.

It contains a complete binary tree with `2,097,151` nodes and `2,097,150` undirected edges, starting from node `0`.
That keeps recursive DFS stack depth around the tree height instead of the node count, while still creating a large traversal and output workload.

Run it with:

```text
make run_cpp INPUT=../inputs/input_large.txt
make run_py INPUT=../inputs/input_large.txt
make run_java INPUT=../inputs/input_large.txt
make run_rs INPUT=../inputs/input_large.txt
```

To time all four language implementations in this folder on the long input:

```text
make benchmark_long
```

This benchmark measures only the `DFS(...)` call inside `main`, not file parsing, graph construction, sorting, or output printing.
The runners expose the timing mode through an optional `--time-dfs` flag.
The benchmark wrapper also reports sampled peak RSS in kilobytes so the memory output works on both macOS and Linux.

## Path Stress Input
This topic also includes `../inputs/input_path.txt`, a path graph with `200,000` nodes and `199,999` edges.

This input is intentionally designed to stress recursive depth overhead.
Unlike the balanced-tree stress case, a path forces recursive DFS to build a call stack proportional to the number of nodes.
Some recursive implementations may fail on this input because of recursion limits or stack exhaustion, which is part of the educational point of the test.

Run it with:

```text
make benchmark_path
```

This path benchmark also reports peak process memory through the same cross-platform wrapper.
