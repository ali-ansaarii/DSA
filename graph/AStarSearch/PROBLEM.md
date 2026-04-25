# A* Search

## What is A* Search?
A* Search is a best-first shortest-path algorithm that combines the exact cost already paid from the start (`g`) with a heuristic estimate of the remaining cost to the goal (`h`). It expands the open state with the smallest `f = g + h`. When `h` is admissible, meaning it never overestimates the true remaining distance, A* returns an optimal shortest path while often exploring fewer states than uninformed Dijkstra search.

## Problem in this folder
This topic solves shortest path on a rectangular 4-direction grid. Each cell is either open (`.`) or blocked (`#`). From an open cell, movement is allowed one step up, down, left, or right into another open cell, and each step costs `1`. Given a start cell and a goal cell, the program prints the shortest path length, or `UNREACHABLE` if no valid path exists.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
The priority queue stores candidate cells ordered by `f = g + h`, where `g` is the shortest distance currently known from the start to that cell and `h` is Manhattan distance to the goal:

```text
h(row, col) = |row - goal_row| + |col - goal_col|
```

For this baseline problem, Manhattan distance is admissible because a 4-direction move changes Manhattan distance by at most one and every move costs exactly one. Obstacles can only make the real path longer; they cannot make a path shorter than the Manhattan lower bound. The heuristic is also consistent for the same reason, so once the goal is popped from the priority queue with the smallest `f`, its `g` value is the optimal shortest path length.

## Input Format
All language implementations use the same whitespace-separated input format:

```text
rows cols
start_row start_col
goal_row goal_col
grid_row_0
grid_row_1
...
grid_row_(rows-1)
```

Rules:

- `rows` and `cols` are positive integers.
- Coordinates are zero-indexed.
- Each grid row contains exactly `cols` characters.
- `.` means an open cell.
- `#` means a blocked cell.
- If the start or goal is out of bounds or blocked, the result is `UNREACHABLE`.

## Output Contract
If a path exists:

```text
Shortest path length: <distance>
```

If no path exists:

```text
UNREACHABLE
```

## Time Complexity
For a grid with `V = rows * cols` cells and up to `E <= 4V` directed neighbor relaxations, the worst-case time complexity is `O(E log V)`, which is `O(V log V)` for this grid. A good admissible heuristic can reduce the number of expanded cells in practice, but the worst case remains the same order as Dijkstra search.

## Space Complexity
The algorithm stores the distance table and priority queue over grid cells, so the worst-case space complexity is `O(V)`.

## Why the challenge input is challenging
`inputs/input_challenge.txt` places the start and goal on opposite sides of a solid wall. The Manhattan heuristic still points directly toward the goal, but no path exists. Because the goal cannot be reached, A* must exhaust the reachable region before proving `UNREACHABLE`, stressing the algorithm's worst-case behavior rather than a successful direct path.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
5 7
0 0
4 6
.......
.#####.
.....#.
.###.#.
...#...
```

## Intended Output
Expected output:

```text
Shortest path length: 10
```
