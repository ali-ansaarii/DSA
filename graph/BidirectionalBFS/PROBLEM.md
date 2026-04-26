# Bidirectional BFS

## What is Bidirectional BFS?
Bidirectional BFS is a shortest-path algorithm for unweighted graphs when both the source and target are known. Instead of growing one breadth-first search wave from the source until it reaches the target, it grows two BFS frontiers: one from the source and one from the target. When the two searches meet, the source-to-meeting and meeting-to-target halves form a shortest path.

## Problem in this folder
Given an undirected, unweighted graph, one source vertex, and one target vertex, compute a shortest path from the source to the target using Bidirectional BFS. The program prints the shortest distance followed by one shortest path. If the target is unreachable from the source, the distance is `-1` and the path line is empty.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
The algorithm keeps a queue and a parent array for each direction. `parent_from_source[v]` records how the source-side BFS first reached `v`; `parent_from_target[v]` records how the target-side BFS first reached `v`. At each step, the implementation expands one whole BFS level from the smaller frontier. Whenever a newly reached vertex has already been reached by the opposite search, that vertex is the meeting point. The final path is reconstructed by walking parents from the meeting point back to the source and then from the meeting point forward to the target.

## Input Format
All language implementations use the same file format:

```text
n m
u1 v1
u2 v2
...
um vm
source target
```

- `n`: number of vertices, labeled `0` through `n - 1`
- `m`: number of undirected edges
- each `ui vi`: one undirected, unweighted edge
- `source target`: the query endpoints

## Output Format
```text
distance: <integer>
path: <space-separated vertices>
```

If the target is unreachable, the output is:

```text
distance: -1
path:
```

## Time Complexity
`O(V + E)` in the worst case, where `V` is the number of vertices and `E` is the number of undirected edges. In many practical one-source-one-target searches, Bidirectional BFS visits much less of the graph than ordinary one-direction BFS.

## Space Complexity
`O(V + E)` for the adjacency list plus `O(V)` for parent arrays and queues.

## Why the challenge input is challenging
`inputs/input_challenge.txt` contains two separate connected components with the source in one component and the target in the other. Because no path exists, the algorithm cannot stop early at a meeting point; it must exhaust the reachable search space from both sides before returning `-1`. This stresses the unreachable-target behavior and confirms that the implementation reports an empty path rather than a partial path.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
9 11
0 1
0 2
1 3
2 3
2 5
3 4
4 8
5 6
6 7
7 8
1 6
0 8
```

## Intended Output
Expected output:

```text
distance: 4
path: 0 1 3 4 8
```
