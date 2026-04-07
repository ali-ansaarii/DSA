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
Because adjacency lists are sorted before DFS, traversal is deterministic.
Expected output:

```text
DFS traversal order: 0 1 3 5 2 6 4
```
