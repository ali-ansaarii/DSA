from __future__ import annotations

import sys
import time

from DifferenceArray import apply_range_add, build_difference_array, reconstruct_values


MIN_I64 = -(1 << 63)
MAX_I64 = (1 << 63) - 1


def checked_i64(value: int) -> int | None:
    if value < MIN_I64 or value > MAX_I64:
        return None
    return value


def read_input(input_path: str) -> tuple[list[int], list[tuple[int, int, int]]] | None:
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
        q = int(tokens[1])
    except ValueError:
        print("Invalid input header.", file=sys.stderr)
        return None

    if n < 0 or q < 0:
        print("Invalid input header.", file=sys.stderr)
        return None

    expected = 2 + n + 3 * q
    if len(tokens) != expected:
        print("Input size does not match header.", file=sys.stderr)
        return None

    values: list[int] = []
    for token in tokens[2 : 2 + n]:
        try:
            values.append(int(token))
        except ValueError:
            print("Invalid array value.", file=sys.stderr)
            return None

    updates = []
    cursor = 2 + n
    for _ in range(q):
        try:
            left = int(tokens[cursor])
            right = int(tokens[cursor + 1])
            delta = int(tokens[cursor + 2])
        except ValueError:
            print("Invalid update.", file=sys.stderr)
            return None
        cursor += 3
        if left < 0 or right < left or right >= n:
            print("Invalid update range.", file=sys.stderr)
            return None
        updates.append((left, right, delta))

    return values, updates


def run_difference_array(values: list[int], updates: list[tuple[int, int, int]]) -> list[int] | None:
    diff = build_difference_array(values)
    for number in diff:
        if checked_i64(number) is None:
            print("Overflow while building the difference array.", file=sys.stderr)
            return None

    for left, right, delta in updates:
        apply_range_add(diff, left, right, delta)
        if checked_i64(diff[left]) is None or (right + 1 < len(diff) and checked_i64(diff[right + 1]) is None):
            print("Overflow while applying a range update.", file=sys.stderr)
            return None

    final_values = reconstruct_values(diff)
    for number in final_values:
        if checked_i64(number) is None:
            print("Overflow while reconstructing the final array.", file=sys.stderr)
            return None

    return final_values


def main() -> int:
    input_path = "inputs/input.txt"
    time_difference_array = False

    for argument in sys.argv[1:]:
        if argument == "--time-difference-array":
            time_difference_array = True
        else:
            input_path = argument

    parsed = read_input(input_path)
    if parsed is None:
        return 1

    values, updates = parsed
    start = time.perf_counter()
    final_values = run_difference_array(values, updates)
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    if final_values is None:
        return 1

    if time_difference_array:
        print(f"Difference-array time: {elapsed_ms:.3f} ms")
    else:
        print("Final array:", *final_values)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
