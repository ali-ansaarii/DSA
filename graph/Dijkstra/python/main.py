from __future__ import annotations

import sys
import time
from pathlib import Path

from Dijkstra import Dijkstra, INF


def main() -> int:
    input_path = Path("input.txt")
    time_dijkstra = False

    for arg in sys.argv[1:]:
        if arg == "--time-dijkstra":
            time_dijkstra = True
        else:
            input_path = Path(arg)

    try:
        lines = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except OSError:
        print(f"Failed to open input file: {input_path}", file=sys.stderr)
        return 1

    if not lines:
        print("Invalid graph header. Expected: n m", file=sys.stderr)
        return 1

    try:
        n, m = map(int, lines[0].split())
    except ValueError:
        print("Invalid graph header. Expected: n m", file=sys.stderr)
        return 1

    if n <= 0 or m < 0:
        print("Invalid graph header. Expected: n m", file=sys.stderr)
        return 1

    if len(lines) < m + 2:
        print("Input ended early. Expected edges and start node.", file=sys.stderr)
        return 1

    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]

    for i in range(1, m + 1):
        try:
            u, v, w = map(int, lines[i].split())
        except ValueError:
            print(f"Invalid weighted edge at line {i + 1}", file=sys.stderr)
            return 1

        if u < 0 or u >= n or v < 0 or v >= n or w < 0:
            print(f"Invalid weighted edge at line {i + 1}", file=sys.stderr)
            return 1

        graph[u].append((v, w))
        graph[v].append((u, w))

    try:
        start = int(lines[m + 1])
    except ValueError:
        print("Invalid start node. Expected a node in [0, n).", file=sys.stderr)
        return 1

    if start < 0 or start >= n:
        print("Invalid start node. Expected a node in [0, n).", file=sys.stderr)
        return 1

    for neighbors in graph:
        neighbors.sort()

    dijkstra_start = time.perf_counter()
    distances = Dijkstra(graph, start)
    dijkstra_duration_ms = (time.perf_counter() - dijkstra_start) * 1000
    reachable_nodes = sum(distance < INF // 2 for distance in distances)

    if time_dijkstra:
        print(f"Reachable nodes: {reachable_nodes}")
        print(f"Dijkstra call time (ms): {dijkstra_duration_ms:.3f}")
    else:
        formatted = [str(distance) if distance < INF // 2 else "INF" for distance in distances]
        print(f"Shortest distances from {start}:", *formatted)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
