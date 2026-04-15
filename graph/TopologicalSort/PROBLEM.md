# Topological Sort

## What is Topological Sort?
Topological sort orders the nodes of a directed acyclic graph (DAG) so every directed edge `u -> v` places `u` before `v`.

This folder implements Kahn's algorithm. It repeatedly selects nodes with indegree `0`, appends them to the order, and removes their outgoing edges by reducing neighbors' indegrees.

## Problem in this folder
Given:
- number of nodes
- list of directed edges

Print one valid topological ordering of the graph.

Nodes are numbered from `0` to `n-1`.
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
- Line 1: `n m`
- Next `m` lines: `u v` (directed edge from `u` to `v`)

The graph is treated as directed in every implementation in this folder.
If the graph contains a cycle, a complete topological order does not exist and the runner reports that clearly.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
6 6
5 2
5 0
4 0
4 1
2 3
3 1
```

## Intended Output
The produced order is deterministic: initial nodes with indegree `0` are scanned in increasing node order, and newly ready neighbors are enqueued according to each sorted adjacency list.
This FIFO version of Kahn's algorithm does not always choose the globally smallest available node; that variant would use a min-priority queue.

Expected output:

```text
Topological order: 4 5 0 2 3 1
```
