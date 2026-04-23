from __future__ import annotations

import sys
import time
from pathlib import Path

from InorderTraversal import InorderTraversal


def is_valid_child(child: int, n: int) -> bool:
    return child == -1 or 0 <= child < n


def main() -> int:
    input_path = Path("../inputs/input.txt")
    time_inorder = False

    for arg in sys.argv[1:]:
        if arg == "--time-inorder":
            time_inorder = True
        else:
            input_path = Path(arg)

    try:
        lines = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except OSError:
        print(f"Failed to open input file: {input_path}", file=sys.stderr)
        return 1

    if not lines:
        print("Invalid tree header. Expected: n root", file=sys.stderr)
        return 1

    try:
        n, root = map(int, lines[0].split())
    except ValueError:
        print("Invalid tree header. Expected: n root", file=sys.stderr)
        return 1

    if n <= 0 or root < 0 or root >= n:
        print("Invalid tree header. Expected: n root", file=sys.stderr)
        return 1

    if len(lines) < n + 1:
        print("Input ended early. Expected child pairs for all nodes.", file=sys.stderr)
        return 1

    left_children = [-1] * n
    right_children = [-1] * n

    for node in range(n):
        try:
            left, right = map(int, lines[node + 1].split())
        except ValueError:
            print(f"Invalid child pair at line {node + 2}", file=sys.stderr)
            return 1

        if not is_valid_child(left, n) or not is_valid_child(right, n):
            print(f"Invalid child pair at line {node + 2}", file=sys.stderr)
            return 1

        left_children[node] = left
        right_children[node] = right

    traversal_start = time.perf_counter()
    order = InorderTraversal(left_children, right_children, root)
    traversal_duration_ms = (time.perf_counter() - traversal_start) * 1000

    if time_inorder:
        print(f"Visited nodes: {len(order)}")
        print(f"InorderTraversal call time (ms): {traversal_duration_ms:.3f}")
    else:
        print("Inorder traversal order:", *order)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
