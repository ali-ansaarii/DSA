# Prim Minimum Spanning Tree

## What is Prim?
Prim's algorithm builds a minimum spanning tree by starting from one node and repeatedly adding the lightest edge that connects the current tree to a new node.

It is a classic greedy algorithm for undirected weighted graphs.
The usual implementation uses a min-heap priority queue to choose the next candidate edge efficiently.

Its time complexity with a heap and adjacency lists is `O(m log m)` in this repository's implementation.

## Problem in this folder
Given:
- number of nodes
- list of weighted undirected edges

Run Prim's algorithm and print:
- the total weight of the minimum spanning tree
- the chosen edges in deterministic order

Nodes are numbered from `0` to `n - 1`.
The implementations start Prim from node `0`.
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
0 1 4
1 2 2
1 3 5
3 5 1
3 4 2
```
