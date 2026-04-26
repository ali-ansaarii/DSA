from __future__ import annotations

import sys
import time
from pathlib import Path

from BidirectionalBFS import shortest_path_bidirectional_bfs


def _read_input(input_path: Path) -> tuple[list[list[int]], int, int]:
    values = [int(token) for token in input_path.read_text(encoding="utf-8").split()]
    if len(values) < 2:
        raise ValueError("input is missing graph header")

    n, m = values[0], values[1]
    if n < 0 or m < 0:
        raise ValueError("n and m must be non-negative")

    expected_values = 2 + 2 * m + 2
    if len(values) != expected_values:
        raise ValueError(f"expected {expected_values} integers, found {len(values)}")

    graph: list[list[int]] = [[] for _ in range(n)]
    offset = 2
    for edge_index in range(m):
        u = values[offset]
        v = values[offset + 1]
        offset += 2
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError(f"invalid edge at index {edge_index}")
        graph[u].append(v)
        graph[v].append(u)

    source = values[offset]
    target = values[offset + 1]
    if not (0 <= source < n and 0 <= target < n):
        raise ValueError("invalid source/target query")

    return graph, source, target


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_flag_time_bidirectional_bfs = False

    for argument in sys.argv[1:]:
        if argument == "--time-bidirectional-bfs":
            time_flag_time_bidirectional_bfs = True
        else:
            input_path = Path(argument)

    graph, source, target = _read_input(input_path)

    if time_flag_time_bidirectional_bfs:
        start = time.perf_counter_ns()
        result = shortest_path_bidirectional_bfs(graph, source, target)
        end = time.perf_counter_ns()
        print(f"algorithm_time_ns: {end - start}", file=sys.stderr)
    else:
        result = shortest_path_bidirectional_bfs(graph, source, target)

    print(f"distance: {result.distance}")
    if result.path:
        print("path: " + " ".join(str(vertex) for vertex in result.path))
    else:
        print("path:")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
