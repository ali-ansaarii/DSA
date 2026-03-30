from __future__ import annotations

import sys
import time
from pathlib import Path

from DFS import DFS


def main() -> int:
    input_path = Path("../inputs/input.txt")
    time_dfs = False

    for arg in sys.argv[1:]:
        if arg == "--time-dfs":
            time_dfs = True
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

    graph = [[] for _ in range(n)]

    for i in range(1, m + 1):
        try:
            u, v = map(int, lines[i].split())
        except ValueError:
            print(f"Invalid edge at line {i + 1}", file=sys.stderr)
            return 1

        if u < 0 or u >= n or v < 0 or v >= n:
            print(f"Invalid edge at line {i + 1}", file=sys.stderr)
            return 1

        # Undirected graph: add both directions.
        graph[u].append(v)
        graph[v].append(u)

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

    dfs_start = time.perf_counter()
    traversal_order = DFS(graph, start)
    dfs_duration_ms = (time.perf_counter() - dfs_start) * 1000

    if time_dfs:
        print(f"DFS visited nodes: {len(traversal_order)}")
        print(f"DFS call time (ms): {dfs_duration_ms:.3f}")
    else:
        print("DFS traversal order:", *traversal_order)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
