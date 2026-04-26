from __future__ import annotations

import sys
import time
from pathlib import Path

from TopologicalSortDFSBased import topological_sort_dfs_based


def parse_input(input_path: Path) -> tuple[int, list[tuple[int, int]]]:
    tokens = input_path.read_text(encoding="utf-8").split()
    if len(tokens) < 2:
        raise ValueError("input must start with: n m")

    vertex_count = int(tokens[0])
    edge_count = int(tokens[1])
    expected_tokens = 2 + 2 * edge_count
    if vertex_count < 0 or edge_count < 0:
        raise ValueError("n and m must be non-negative")
    if len(tokens) != expected_tokens:
        raise ValueError(f"expected {edge_count} edges, found {(len(tokens) - 2) // 2}")

    edges: list[tuple[int, int]] = []
    for index in range(edge_count):
        base = 2 + 2 * index
        edges.append((int(tokens[base]), int(tokens[base + 1])))
    return vertex_count, edges


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_flag_time_topological_sort_dfs_based = False

    for argument in sys.argv[1:]:
        if argument == "--time-topological-sort-dfs-based":
            time_flag_time_topological_sort_dfs_based = True
        else:
            input_path = Path(argument)

    try:
        vertex_count, edges = parse_input(input_path)
        start = time.perf_counter_ns()
        result = topological_sort_dfs_based(vertex_count, edges)
        elapsed = time.perf_counter_ns() - start
    except OSError as error:
        print(f"Failed to read input file: {error}", file=sys.stderr)
        return 1
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    if time_flag_time_topological_sort_dfs_based:
        print(f"algorithm_time_ns {elapsed}", file=sys.stderr)

    if result.has_cycle:
        print("CYCLE DETECTED")
    else:
        print("Topological order:")
        print(" ".join(str(vertex) for vertex in result.order))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
