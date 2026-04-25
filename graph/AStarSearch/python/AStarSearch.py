from __future__ import annotations

from heapq import heappop, heappush
from typing import Sequence


def _manhattan(row: int, col: int, goal_row: int, goal_col: int) -> int:
    return abs(row - goal_row) + abs(col - goal_col)


def shortest_path_length_a_star(
    grid: Sequence[str], start_row: int, start_col: int, goal_row: int, goal_col: int
) -> int:
    if not grid or not grid[0]:
        return -1

    rows = len(grid)
    cols = len(grid[0])

    def is_open(row: int, col: int) -> bool:
        return 0 <= row < rows and 0 <= col < cols and grid[row][col] != "#"

    if not is_open(start_row, start_col) or not is_open(goal_row, goal_col):
        return -1

    infinity = 10**18
    distance = [[infinity] * cols for _ in range(rows)]

    start_h = _manhattan(start_row, start_col, goal_row, goal_col)
    # (f_score, h_score, g_score, row, col). h_score tie-breaking favors cells
    # closer to the goal while preserving optimality with an admissible heuristic.
    open_heap: list[tuple[int, int, int, int, int]] = [(start_h, start_h, 0, start_row, start_col)]
    distance[start_row][start_col] = 0

    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    while open_heap:
        _, _, current_distance, row, col = heappop(open_heap)
        if current_distance != distance[row][col]:
            continue

        if row == goal_row and col == goal_col:
            return current_distance

        for d_row, d_col in directions:
            next_row = row + d_row
            next_col = col + d_col
            if not is_open(next_row, next_col):
                continue

            next_distance = current_distance + 1
            if next_distance < distance[next_row][next_col]:
                distance[next_row][next_col] = next_distance
                heuristic = _manhattan(next_row, next_col, goal_row, goal_col)
                heappush(
                    open_heap,
                    (next_distance + heuristic, heuristic, next_distance, next_row, next_col),
                )

    return -1
