from __future__ import annotations

import sys
import time

from MonotonicStack import next_greater_elements


MIN_I64 = -(1 << 63)
MAX_I64 = (1 << 63) - 1


def read_input(input_path: str) -> list[int] | None:
    try:
        with open(input_path, "r", encoding="utf-8") as handle:
            tokens = handle.read().split()
    except OSError:
        print(f"Failed to open input file: {input_path}", file=sys.stderr)
        return None

    if not tokens:
        print("Invalid input header.", file=sys.stderr)
        return None

    try:
        n = int(tokens[0])
    except ValueError:
        print("Invalid input header.", file=sys.stderr)
        return None

    if n <= 0:
        print("Invalid input header.", file=sys.stderr)
        return None

    if len(tokens) != 1 + n:
        print("Input size does not match header.", file=sys.stderr)
        return None

    values: list[int] = []
    for token in tokens[1:]:
        try:
            value = int(token)
        except ValueError:
            print("Invalid array value.", file=sys.stderr)
            return None
        if value < MIN_I64 or value > MAX_I64:
            print("Invalid array value.", file=sys.stderr)
            return None
        values.append(value)

    return values


def main() -> int:
    input_path = "inputs/input.txt"
    time_monotonic_stack = False

    for argument in sys.argv[1:]:
        if argument == "--time-monotonic-stack":
            time_monotonic_stack = True
        else:
            input_path = argument

    values = read_input(input_path)
    if values is None:
        return 1

    start = time.perf_counter()
    answer = next_greater_elements(values)
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    if time_monotonic_stack:
        print(f"Monotonic-stack time: {elapsed_ms:.3f} ms")
    else:
        print("Next greater elements:", *answer)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
