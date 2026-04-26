from __future__ import annotations

import sys
import time
from pathlib import Path

from ShortestPathInDAG import Edge, INF, shortest_path_in_dag


def parse_input(input_path: Path) -> tuple[int, list[Edge], int]:
    with input_path.open("r", encoding="utf-8") as file:
        tokens = file.read().split()

    if len(tokens) < 3:
        raise ValueError("invalid input header")

    iterator = iter(tokens)
    vertex_count = int(next(iterator))
    edge_count = int(next(iterator))
    source = int(next(iterator))
    if vertex_count < 0 or edge_count < 0:
        raise ValueError("vertex and edge counts must be non-negative")

    edges: list[Edge] = []
    for index in range(edge_count):
        try:
            edge_source = int(next(iterator))
            edge_target = int(next(iterator))
            weight = int(next(iterator))
        except StopIteration as exc:
            raise ValueError(f"invalid edge line at index {index}") from exc
        edges.append(Edge(edge_source, edge_target, weight))

    return vertex_count, edges, source


def format_distances(distances: list[int]) -> str:
    return " ".join("INF" if distance == INF else str(distance) for distance in distances)


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_flag_time_shortest_path_in_dag = False

    for argument in sys.argv[1:]:
        if argument == "--time-shortest-path-in-dag":
            time_flag_time_shortest_path_in_dag = True
        else:
            input_path = Path(argument)

    try:
        vertex_count, edges, source = parse_input(input_path)
        if time_flag_time_shortest_path_in_dag:
            start = time.perf_counter()
            distances = shortest_path_in_dag(vertex_count, edges, source)
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            print(f"algorithm_ms {elapsed_ms:.6f}", file=sys.stderr)
        else:
            distances = shortest_path_in_dag(vertex_count, edges, source)
        print(format_distances(distances))
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
