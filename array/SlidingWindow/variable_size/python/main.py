from __future__ import annotations

import sys
import time

from SlidingWindow import MAX_I64, MIN_I64, min_window_at_least_target


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
        target = int(tokens[1])
    except ValueError:
        print("Invalid input header.", file=sys.stderr)
        return None

    if n <= 0 or target <= 0 or target < MIN_I64 or target > MAX_I64:
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
        if value <= 0 or value < MIN_I64 or value > MAX_I64:
            print("Variable-size sliding window requires positive values.", file=sys.stderr)
            return None
        values.append(value)

    return values, target


def main() -> int:
    input_path = "inputs/input.txt"
    time_variable_window = False

    for argument in sys.argv[1:]:
        if argument == "--time-variable-window":
            time_variable_window = True
        else:
            input_path = argument

    parsed = read_input(input_path)
    if parsed is None:
        return 1

    values, target = parsed
    start = time.perf_counter()
    result = min_window_at_least_target(values, target)
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    if result is None:
        print("Overflow while evaluating variable-size windows.", file=sys.stderr)
        return 1

    best_length, best_left, best_right = result
    if time_variable_window:
        print(f"Variable-window time: {elapsed_ms:.3f} ms")
    elif best_length == -1:
        print("No valid window")
    else:
        print(f"Minimum window length: {best_length}")
        print(f"Minimum window range: {best_left} {best_right}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
