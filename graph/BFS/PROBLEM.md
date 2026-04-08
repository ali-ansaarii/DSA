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
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
- Line 1: `n m`
- Next `m` lines: `u v` (undirected edge between `u` and `v`)
- Last line: `start`

The graph is treated as undirected in every implementation in this folder.

## Test Case
This is the test case currently used in `inputs/input.txt`:

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
