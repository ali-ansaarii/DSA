# Shortest Path in DAG

## What is Shortest Path in DAG?
Shortest Path in a Directed Acyclic Graph (DAG) computes the minimum distance from one source vertex to every other vertex in a weighted directed graph that has no directed cycle. Because every edge goes forward in at least one topological ordering, vertices can be processed once in topological order and each outgoing edge can be relaxed exactly once.

## Problem in this folder
Given a weighted DAG with vertices numbered `0` through `n - 1` and a source vertex `s`, output the final distance array from `s`. Unreachable vertices are printed as `INF`.

This implementation uses the classical topological-order relaxation baseline:

1. Build adjacency lists and indegrees.
2. Compute a topological order with Kahn's algorithm.
3. Set `distance[source] = 0` and all other distances to infinity.
4. Visit vertices in topological order; when a visited vertex has a finite distance, relax all outgoing edges.

Unlike Dijkstra's algorithm, this method allows negative edge weights because acyclicity prevents negative cycles. Unlike Bellman-Ford, it does not need repeated passes over all edges; one topological pass is enough. The tradeoff is that the graph must be a DAG.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
In a topological order, every predecessor of a vertex appears before that vertex. Therefore, by the time the algorithm reaches vertex `v`, every possible shortest path ending at `v` has already had its final incoming edge considered. After that point, `distance[v]` is final and can safely be used to relax edges leaving `v`.

## Input Format
All language implementations use the same text format:

```text
n m source
u1 v1 w1
u2 v2 w2
...
um vm wm
```

- `n`: number of vertices.
- `m`: number of directed weighted edges.
- `source`: source vertex.
- Each edge line `u v w` represents a directed edge from `u` to `v` with integer weight `w`.
- Vertices are zero-indexed and must be in the range `[0, n - 1]`.
- The graph is expected to be acyclic.

## Output Format
Print one line containing `n` space-separated entries: the distance from `source` to each vertex, or `INF` if the vertex is unreachable.

## Time Complexity
`O(V + E)`, where `V` is the number of vertices and `E` is the number of edges. Building indegrees, computing the topological order, and relaxing all edges each take linear time.

## Space Complexity
`O(V + E)` for the adjacency list, indegree array, topological queue/order, and distance array.

## Why the challenge input is challenging
`inputs/input_challenge.txt` contains negative edge weights, multiple competing routes to the same vertices, unreachable components, and long dependency chains. It stresses the key DAG-shortest-path properties: the implementation must not assume non-negative weights, must skip unreachable vertices rather than relaxing from infinity, and must process vertices in a valid topological order.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
6 9 0
0 1 5
0 2 3
1 3 6
1 2 2
2 4 4
2 5 2
2 3 7
3 4 -1
4 5 -2
```

## Intended Output
Expected output:

```text
0 5 3 10 7 5
```
