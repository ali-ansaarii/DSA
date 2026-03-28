from __future__ import annotations

import sys
from pathlib import Path

from DFS import DFS


def main() -> int:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("input.txt")

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

    traversal_order = DFS(graph, start)
    print("DFS traversal order:", *traversal_order)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
