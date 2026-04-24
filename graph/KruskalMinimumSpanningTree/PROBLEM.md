# Kruskal Minimum Spanning Tree

## What is Kruskal?
Kruskal's algorithm builds a minimum spanning tree by sorting all edges by weight and then adding edges that connect two different components.

It is a classic greedy algorithm for undirected weighted graphs.
The usual implementation uses Disjoint Set Union (DSU), also called Union-Find, to test whether an edge would create a cycle.

Its time complexity is dominated by sorting: `O(m log m)` for `m` edges.

## Problem in this folder
Given:
- number of nodes
- list of weighted undirected edges

Run Kruskal's algorithm and print:
- the total weight of the minimum spanning tree
- the chosen edges in deterministic order

Nodes are numbered from `0` to `n - 1`.
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
- Line 1: `n m`
- Next `m` lines: `u v w` (undirected edge between `u` and `v` with weight `w`)

Edge weights and the final MST weight are treated as signed 64-bit values in every language implementation in this folder.
If summing chosen edge weights would overflow that range, the program reports overflow and exits instead of silently wrapping.

If the graph is disconnected, a minimum spanning tree over all nodes does not exist.
In that case, the program reports that the graph is disconnected instead of printing an MST.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
6 9
0 1 4
0 2 4
1 2 2
1 3 5
2 3 5
2 4 11
3 4 2
3 5 1
4 5 7
```

## Intended Output
Expected output:

```text
MST total weight: 14
MST edges:
3 5 1
1 2 2
3 4 2
0 1 4
1 3 5
```
