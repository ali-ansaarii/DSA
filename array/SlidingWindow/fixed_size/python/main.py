from __future__ import annotations

import sys
import time

from SlidingWindow import MAX_I64, MIN_I64, best_fixed_window


def read_input(input_path: str) -> tuple[list[int], int] | None:
    try:
        with open(input_path, "r", encoding="utf-8") as handle:
            tokens = handle.read().split()
    except OSError:
        print(f"Failed to open input file: {input_path}", file=sys.stderr)
        return None

    if len(tokens) < 2:
        print("Invalid input header.", file=sys.stderr)
        return None

    try:
        n = int(tokens[0])
        k = int(tokens[1])
    except ValueError:
        print("Invalid input header.", file=sys.stderr)
        return None

    if n <= 0 or k <= 0 or k > n:
        print("Invalid input header.", file=sys.stderr)
        return None

    if len(tokens) != 2 + n:
        print("Input size does not match header.", file=sys.stderr)
        return None

    values: list[int] = []
    for token in tokens[2:]:
        try:
            value = int(token)
        except ValueError:
            print("Invalid array value.", file=sys.stderr)
            return None
        if value < MIN_I64 or value > MAX_I64:
            print("Invalid array value.", file=sys.stderr)
            return None
        values.append(value)

    return values, k


def main() -> int:
    input_path = "inputs/input.txt"
    time_fixed_window = False

    for argument in sys.argv[1:]:
        if argument == "--time-fixed-window":
            time_fixed_window = True
        else:
            input_path = argument

    parsed = read_input(input_path)
    if parsed is None:
        return 1

    values, k = parsed
    start = time.perf_counter()
    result = best_fixed_window(values, k)
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    if result is None:
        print("Overflow while evaluating fixed-size windows.", file=sys.stderr)
        return 1

    best_sum, best_left, best_right = result
    if time_fixed_window:
        print(f"Fixed-window time: {elapsed_ms:.3f} ms")
    else:
        print(f"Best window sum: {best_sum}")
        print(f"Best window range: {best_left} {best_right}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
