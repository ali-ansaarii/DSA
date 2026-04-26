# Topological Sort, DFS-based

## What is Topological Sort, DFS-based?
Topological sorting orders the vertices of a directed acyclic graph (DAG) so that every directed edge `u -> v` places `u` before `v`. The DFS-based method performs a depth-first traversal and appends each vertex to a postorder list only after all of its outgoing neighbors have been fully processed; reversing that postorder list yields a valid topological ordering.

## Problem in this folder
Given a directed graph using the same DAG-style edge contract as Kahn-based topological sort (`u v` means `u` must come before `v`), output one deterministic topological order. Vertices are visited from `0` to `n - 1`, and each adjacency list is explored in input order, so the output is deterministic for a fixed input file.

If the input graph contains a directed cycle, no topological ordering exists. All implementations detect this with DFS colors and print `CYCLE DETECTED` instead of an order.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
DFS maintains three states for each vertex: unvisited, visiting, and done. When DFS first enters a vertex, it becomes visiting. Seeing an edge to another visiting vertex proves there is a directed cycle. When every outgoing edge has been considered, the vertex becomes done and is appended to a postorder list. Because a vertex is appended after all reachable descendants, reversing postorder places each prerequisite before the vertices that depend on it.

The implementations use an explicit stack to perform DFS. This keeps the algorithm DFS-based and reverse-postorder-driven while avoiding language call-stack limits on long dependency chains.

## Input Format
All language implementations read the same whitespace-separated file format:

```text
n m
u1 v1
u2 v2
...
um vm
```

- `n` is the number of vertices, labeled `0` through `n - 1`.
- `m` is the number of directed edges.
- Each edge `u v` means `u` must appear before `v` in the topological order.
- The intended contract is a DAG, but cycle detection is implemented and documented.

## Output Format
For an acyclic graph:

```text
Topological order:
<space-separated vertex order>
```

For a cyclic graph:

```text
CYCLE DETECTED
```

## Time Complexity
`O(n + m)`, where `n` is the number of vertices and `m` is the number of directed edges. Each vertex is entered and finished once, and each edge is examined once.

## Space Complexity
`O(n + m)` for the adjacency list plus `O(n)` for color state, the explicit DFS stack, and the reverse-postorder list.

## Why the challenge input is challenging
`inputs/input_challenge.txt` is a long, narrow dependency chain with a few forward skip edges. A recursive DFS implementation would risk deep call-stack growth on larger versions of this shape. These implementations use an explicit stack, so the challenge stresses DFS depth and postorder construction without relying on process recursion limits.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
6 6
0 1
0 2
1 3
2 3
3 4
2 5
```

## Intended Output
Expected output:

```text
Topological order:
0 2 5 1 3 4
```
