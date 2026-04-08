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

## Large Stress Input
This topic also includes `input_large.txt` for performance testing.

It contains a weighted undirected grid graph with `160,000` nodes and `319,200` edges, starting from node `0`.
This gives Dijkstra a large but representative sparse workload where the heap and relaxation logic both matter.

Run it with:

```text
make run_cpp INPUT=input_large.txt
make run_py INPUT=input_large.txt
make run_java INPUT=input_large.txt
make run_rs INPUT=input_large.txt
```

To time all four language implementations in this folder on the long input:

```text
make benchmark_long
```

This benchmark measures only the `Dijkstra(...)` call inside `main`, not file parsing, graph construction, or output printing.
The runners expose the timing mode through an optional `--time-dijkstra` flag.
The benchmark wrapper also reports sampled peak RSS in kilobytes so the memory output works on both macOS and Linux.

## Challenge Input
This topic also includes `input_challenge.txt`, a weighted graph with `220,000` nodes and `439,998` edges.

It is intentionally designed to create many stale priority-queue entries.
The source node has a direct but poor edge to every other node, while a light chain between consecutive nodes keeps discovering better paths later.
That means the heap accumulates many entries that are no longer optimal by the time they are popped.

Run it with:

```text
make benchmark_challenge
```

This challenge benchmark also reports peak process memory through the same cross-platform wrapper.
