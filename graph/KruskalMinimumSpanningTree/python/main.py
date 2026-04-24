from __future__ import annotations

import sys
import time

from KruskalMST import Edge, KruskalStatus, kruskal_mst


def parse_args(argv: list[str]) -> tuple[str, bool]:
    input_path: str | None = None
    benchmark_mode = False

    for argument in argv[1:]:
        if argument == "--time-kruskal":
            benchmark_mode = True
        elif input_path is None:
            input_path = argument
        else:
            raise ValueError("Usage: main.py <input-file> [--time-kruskal]")

    if input_path is None:
        raise ValueError("Usage: main.py <input-file> [--time-kruskal]")

    return input_path, benchmark_mode


def read_input(path: str) -> tuple[int, list[Edge]]:
    with open(path, "r", encoding="utf-8") as handle:
        tokens = handle.read().split()

    if len(tokens) < 2:
        raise ValueError("Invalid graph input")

    position = 0
    node_count = int(tokens[position])
    position += 1
    edge_count = int(tokens[position])
    position += 1

    if node_count <= 0 or edge_count < 0:
        raise ValueError("Invalid graph header")

    edges: list[Edge] = []
    for index in range(edge_count):
        if position + 3 > len(tokens):
            raise ValueError(f"Invalid edge at index {index}")

        source = int(tokens[position])
        target = int(tokens[position + 1])
        weight = int(tokens[position + 2])
        position += 3

        if not (0 <= source < node_count and 0 <= target < node_count):
            raise ValueError(f"Edge node out of range at index {index}")

        edges.append(Edge(source, target, weight))

    return node_count, edges


def print_result(total_weight: int, chosen_edges: list[Edge]) -> None:
    print(f"MST total weight: {total_weight}")
    print("MST edges:")
    for edge in chosen_edges:
        print(f"{edge.source} {edge.target} {edge.weight}")


def main(argv: list[str]) -> int:
    try:
        input_path, benchmark_mode = parse_args(argv)
        node_count, edges = read_input(input_path)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1
    except OSError as error:
        print(f"Failed to open input file: {error}", file=sys.stderr)
        return 1

    start_time = time.perf_counter()
    result = kruskal_mst(node_count, edges)
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    if benchmark_mode:
        print(f"Kruskal time: {elapsed_ms:.3f} ms")

    if result.status == KruskalStatus.OVERFLOW:
        print("Overflow detected while summing MST edge weights", file=sys.stderr)
        return 1

    if result.status == KruskalStatus.DISCONNECTED:
        print("Graph is disconnected; MST does not exist")
        return 0

    if not benchmark_mode:
        print_result(result.total_weight, result.chosen_edges)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
