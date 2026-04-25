from __future__ import annotations

import sys
import time
from pathlib import Path

from InsertionSort import insertion_sort


def read_input(input_path: Path) -> list[int]:
    tokens = input_path.read_text(encoding="utf-8").split()
    if not tokens:
        raise ValueError("input must start with the number of elements")

    n = int(tokens[0])
    if n < 0:
        raise ValueError("number of elements must be nonnegative")

    values = [int(token) for token in tokens[1:]]
    if len(values) < n:
        raise ValueError("input ended before all elements were read")
    if len(values) > n:
        values = values[:n]

    return values


def print_values(values: list[int]) -> None:
    print(" ".join(str(value) for value in values))


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_flag_time_insertion_sort = False

    for argument in sys.argv[1:]:
        if argument == "--time-insertion-sort":
            time_flag_time_insertion_sort = True
        else:
            input_path = Path(argument)

    try:
        values = read_input(input_path)

        if time_flag_time_insertion_sort:
            start = time.perf_counter()
            insertion_sort(values)
            elapsed_microseconds = int((time.perf_counter() - start) * 1_000_000)
            print(f"algorithm_time_microseconds={elapsed_microseconds}", file=sys.stderr)
        else:
            insertion_sort(values)

        print_values(values)
    except Exception as error:  # noqa: BLE001 - keep CLI errors concise for all parse failures.
        print(f"error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
