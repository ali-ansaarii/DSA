# Dijkstra's Algorithm

## What is Dijkstra?
Dijkstra's algorithm finds the shortest path distances from one start node to every other reachable node in a graph with non-negative edge weights.

It repeatedly takes the not-yet-finalized node with the smallest known distance and relaxes its outgoing edges.
In these implementations, a min-heap priority queue is used to select the next node efficiently.

## Problem in this folder
Given:
- number of nodes
- list of weighted undirected edges
- a start node

Run Dijkstra from the start node and print the shortest distance to every node.

Nodes are numbered from `0` to `n-1`.
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
- Line 1: `n m`
- Next `m` lines: `u v w` (undirected edge between `u` and `v` with weight `w`)
- Last line: `start`

All edge weights must be non-negative.
Shortest-path distances are treated as signed 64-bit values in every language implementation in this folder.
If a valid shortest path would exceed that range, the program reports overflow and exits instead of silently wrapping or mislabeling the result.

## Test Case
This is the test case currently used in `input.txt`:

```text
6 9
0 1 7
0 2 9
0 5 14
1 2 10
1 3 15
2 3 11
2 5 2
3 4 6
4 5 9
0
```

## Intended Output
Expected output:

```text
Shortest distances from 0: 0 7 9 20 20 11
```
