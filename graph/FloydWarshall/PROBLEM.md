# Floyd-Warshall Algorithm

## What is Floyd-Warshall?
Floyd-Warshall computes shortest path distances between every pair of nodes in a weighted directed graph.
It supports negative edge weights as long as the graph does not contain a negative-weight cycle.

The algorithm builds answers by gradually allowing more intermediate nodes in candidate paths.
Its main advantage is that it solves the all-pairs shortest path problem directly.
Its main cost is time: `O(n^3)` for `n` nodes, plus `O(n^2)` memory for the distance matrix.

## Problem in this folder
Given:
- number of nodes
- list of weighted directed edges

Run Floyd-Warshall and print the shortest distance from every node to every other node.

Nodes are numbered from `0` to `n - 1`.
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
- Line 1: `n m`
- Next `m` lines: `u v w` (directed edge from `u` to `v` with weight `w`)

Shortest-path distances are treated as signed 64-bit values in every language implementation in this folder.
If a relaxation would overflow that range, the program reports overflow and exits instead of silently wrapping.

If any negative-weight cycle exists, shortest paths are undefined for at least part of the graph.
In that case, the program reports the negative cycle instead of printing the matrix.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
5 9
0 1 3
0 2 8
0 4 -4
1 3 1
1 4 7
2 1 4
3 0 2
3 2 -5
4 3 6
```

## Intended Output
Expected output:

```text
All-pairs shortest distances:
0 1 -3 2 -4
3 0 -4 1 -1
7 4 0 5 3
2 -1 -5 0 -2
8 5 1 6 0
```
