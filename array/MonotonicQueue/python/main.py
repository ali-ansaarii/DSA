from __future__ import annotations

import sys
import time
from pathlib import Path

from MonotonicQueue import sliding_window_maximum

MIN_I64 = -(1 << 63)
MAX_I64 = (1 << 63) - 1


def checked_i64(value: int) -> int:
    if value < MIN_I64 or value > MAX_I64:
        raise ValueError("Value out of signed 64-bit range.")
    return value


def read_input(input_path: Path) -> tuple[list[int], int]:
    try:
        tokens = input_path.read_text(encoding="utf-8").split()
    except OSError:
        print(f"Failed to open input file: {input_path}", file=sys.stderr)
        raise SystemExit(1)

    if len(tokens) < 2:
        print("Invalid input header.", file=sys.stderr)
        raise SystemExit(1)

    try:
        n = int(tokens[0])
        window_size = int(tokens[1])
    except ValueError:
        print("Invalid input header.", file=sys.stderr)
        raise SystemExit(1)

    if n <= 0 or window_size <= 0 or window_size > n:
        print("Invalid input header.", file=sys.stderr)
        raise SystemExit(1)

    if len(tokens) != n + 2:
        print("Input size does not match header.", file=sys.stderr)
        raise SystemExit(1)

    values: list[int] = []
    for index, token in enumerate(tokens[2:]):
        try:
            values.append(checked_i64(int(token)))
        except ValueError:
            print(f"Failed to read array value at index {index}.", file=sys.stderr)
            raise SystemExit(1)

    return values, window_size


def print_answer(maxima: list[int]) -> None:
    print("Window maxima:", *maxima)


def main() -> None:
    input_path = Path("inputs/input.txt")
    time_monotonic_queue = False

    for argument in sys.argv[1:]:
        if argument == "--time-monotonic-queue":
            time_monotonic_queue = True
        else:
            input_path = Path(argument)

    values, window_size = read_input(input_path)

    start = time.perf_counter()
    maxima = sliding_window_maximum(values, window_size)
    end = time.perf_counter()

    if time_monotonic_queue:
        print(f"Monotonic-queue time: {(end - start) * 1000.0:.6f} ms")
    else:
        print_answer(maxima)


if __name__ == "__main__":
    main()
