from __future__ import annotations

import sys
import time
from pathlib import Path

from DisjointSetUnion import DisjointSetUnion, Operation, OperationType


def is_valid_element(element: int, n: int) -> bool:
    return 0 <= element < n


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_dsu = False

    for arg in sys.argv[1:]:
        if arg == "--time-dsu":
            time_dsu = True
        else:
            input_path = Path(arg)

    try:
        lines = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except OSError:
        print(f"Failed to open input file: {input_path}", file=sys.stderr)
        return 1

    if not lines:
        print("Invalid DSU header. Expected: n q", file=sys.stderr)
        return 1

    try:
        n, q = map(int, lines[0].split())
    except ValueError:
        print("Invalid DSU header. Expected: n q", file=sys.stderr)
        return 1

    if n <= 0 or q < 0:
        print("Invalid DSU header. Expected: n q", file=sys.stderr)
        return 1

    if len(lines) < q + 1:
        print(f"Input ended early. Expected {q} operations.", file=sys.stderr)
        return 1

    operations: list[Operation] = []
    for line_index in range(1, q + 1):
        parts = lines[line_index].split()
        if not parts:
            print(f"Invalid operation at line {line_index + 1}", file=sys.stderr)
            return 1

        op = parts[0]
        if op in {"union", "connected"}:
            if len(parts) != 3:
                print(f"Invalid operation at line {line_index + 1}", file=sys.stderr)
                return 1

            try:
                a, b = map(int, parts[1:])
            except ValueError:
                print(f"Invalid operation at line {line_index + 1}", file=sys.stderr)
                return 1

            if not is_valid_element(a, n) or not is_valid_element(b, n):
                print(f"Invalid operation at line {line_index + 1}", file=sys.stderr)
                return 1

            operations.append(
                Operation(OperationType.UNION if op == "union" else OperationType.CONNECTED, a, b)
            )
        elif op == "find":
            if len(parts) != 2:
                print(f"Invalid operation at line {line_index + 1}", file=sys.stderr)
                return 1

            try:
                a = int(parts[1])
            except ValueError:
                print(f"Invalid operation at line {line_index + 1}", file=sys.stderr)
                return 1

            if not is_valid_element(a, n):
                print(f"Invalid operation at line {line_index + 1}", file=sys.stderr)
                return 1

            operations.append(Operation(OperationType.FIND, a, -1))
        else:
            print(f"Invalid operation at line {line_index + 1}", file=sys.stderr)
            return 1

    dsu_start = time.perf_counter()
    query_results = DisjointSetUnion(n, operations)
    dsu_duration_ms = (time.perf_counter() - dsu_start) * 1000

    if time_dsu:
        print(f"Processed operations: {len(operations)}")
        print(f"DisjointSetUnion call time (ms): {dsu_duration_ms:.3f}")
    else:
        print("Query results:")
        for result in query_results:
            print(result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
