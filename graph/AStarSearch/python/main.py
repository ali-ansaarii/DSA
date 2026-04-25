from __future__ import annotations

import sys
import time
from pathlib import Path

from AStarSearch import shortest_path_length_a_star


def parse_input(input_path: Path) -> tuple[list[str], int, int, int, int]:
    tokens = input_path.read_text(encoding="utf-8").split()
    if len(tokens) < 6:
        raise ValueError("input must contain rows, cols, start, and goal coordinates")

    rows = int(tokens[0])
    cols = int(tokens[1])
    start_row = int(tokens[2])
    start_col = int(tokens[3])
    goal_row = int(tokens[4])
    goal_col = int(tokens[5])

    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must be positive")

    grid = tokens[6 : 6 + rows]
    if len(grid) != rows:
        raise ValueError("missing grid rows")

    for row_index, row in enumerate(grid):
        if len(row) != cols:
            raise ValueError(f"grid row {row_index} has the wrong length")
        if any(cell not in ".#" for cell in row):
            raise ValueError("grid may contain only '.' and '#'")

    return grid, start_row, start_col, goal_row, goal_col


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_flag_time_a_star_search = False

    for argument in sys.argv[1:]:
        if argument == "--time-a-star-search":
            time_flag_time_a_star_search = True
        else:
            input_path = Path(argument)

    try:
        grid, start_row, start_col, goal_row, goal_col = parse_input(input_path)

        if time_flag_time_a_star_search:
            started_at = time.perf_counter_ns()
            distance = shortest_path_length_a_star(grid, start_row, start_col, goal_row, goal_col)
            elapsed_microseconds = (time.perf_counter_ns() - started_at) // 1_000
            print(f"Algorithm time (microseconds): {elapsed_microseconds}", file=sys.stderr)
        else:
            distance = shortest_path_length_a_star(grid, start_row, start_col, goal_row, goal_col)

        if distance >= 0:
            print(f"Shortest path length: {distance}")
        else:
            print("UNREACHABLE")
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
