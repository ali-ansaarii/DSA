# Bellman-Ford Algorithm

## What is Bellman-Ford?
Bellman-Ford finds shortest path distances from one start node to every other reachable node in a weighted directed graph.
Unlike Dijkstra, it supports negative edge weights.

The tradeoff is cost: Bellman-Ford may need up to `n - 1` full passes over the edge list, so its time complexity is `O(n * m)` for `n` nodes and `m` edges.

## Problem in this folder
Given:
- number of nodes
- list of weighted directed edges
- a start node

Run Bellman-Ford from the start node and print the shortest distance to every node.

Nodes are numbered from `0` to `n - 1`.
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
- Line 1: `n m`
- Next `m` lines: `u v w` (directed edge from `u` to `v` with weight `w`)
- Last line: `start`

Shortest-path distances are treated as signed 64-bit values in every language implementation in this folder.
If a relaxation would overflow that range, the program reports overflow and exits instead of silently wrapping.

If a negative-weight cycle is reachable from the start node, shortest paths are undefined.
In that case, the program reports the reachable negative cycle instead of printing distances.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
5 10
0 1 6
0 3 7
1 2 5
1 3 8
1 4 -4
2 1 -2
3 2 -3
3 4 9
4 0 2
4 2 7
0
```

## Intended Output
Expected output:

```text
Shortest distances from 0: 0 2 4 7 -2
```
