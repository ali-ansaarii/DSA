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
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
- Line 1: `n m`
- Next `m` lines: `u v` (undirected edge between `u` and `v`)
- Last line: `start`

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
