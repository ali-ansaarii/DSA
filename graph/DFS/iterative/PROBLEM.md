# Depth-First Search (DFS) - Iterative Version

## What is DFS?
Depth-First Search (DFS) is a way to visit all nodes in a graph.

DFS starts from one node and explores one path as deeply as possible before returning to try another path.
In this folder, DFS is implemented iteratively with an explicit stack instead of recursion.

## Problem in this folder
Given:
- number of nodes
- list of undirected edges
- a start node

Run iterative DFS from the start node and print traversal order.

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
Adjacency lists are sorted before traversal. Neighbors are pushed onto the stack in reverse order so the iterative DFS matches the natural left-to-right recursive visitation order.

Expected output:

```text
DFS traversal order: 0 1 3 5 2 6 4
```

## Large Stress Input
This topic also includes `../inputs/input_large.txt` for performance testing.

It contains a complete binary tree with `2,097,151` nodes and `2,097,150` undirected edges, starting from node `0`.
This keeps the recursive companion case stack-safe and gives both versions the same large workload for comparison.

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

This case is included specifically to contrast iterative DFS against recursive DFS on deep traversal shapes.
Iterative DFS should handle this graph without recursion-depth risk, while recursive versions in some languages or environments may overflow the call stack.

Run it with:

```text
make benchmark_path
```

This path benchmark also reports peak process memory through the same cross-platform wrapper.
