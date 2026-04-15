from __future__ import annotations

import sys
import time
from pathlib import Path

from TopologicalSort import TopologicalSort


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_topological_sort = False

    for arg in sys.argv[1:]:
        if arg == "--time-toposort":
            time_topological_sort = True
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

    if len(lines) < m + 1:
        print("Input ended early. Expected directed edges.", file=sys.stderr)
        return 1

    graph: list[list[int]] = [[] for _ in range(n)]

    for i in range(1, m + 1):
        try:
            u, v = map(int, lines[i].split())
        except ValueError:
            print(f"Invalid directed edge at line {i + 1}", file=sys.stderr)
            return 1

        if u < 0 or u >= n or v < 0 or v >= n:
            print(f"Invalid directed edge at line {i + 1}", file=sys.stderr)
            return 1

        graph[u].append(v)

    for neighbors in graph:
        neighbors.sort()

    topological_sort_start = time.perf_counter()
    order = TopologicalSort(graph)
    topological_sort_duration_ms = (time.perf_counter() - topological_sort_start) * 1000

    if time_topological_sort:
        print(f"Processed nodes: {len(order)}")
        print(f"TopologicalSort call time (ms): {topological_sort_duration_ms:.3f}")

    if len(order) != len(graph):
        print("Cycle detected. Topological sort requires a DAG.", file=sys.stderr)
        return 1

    if not time_topological_sort:
        print("Topological order:", *order)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
