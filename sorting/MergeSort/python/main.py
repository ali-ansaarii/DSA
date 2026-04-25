from __future__ import annotations

import sys
import time
from pathlib import Path

from MergeSort import merge_sort


def read_input(input_path: Path) -> list[int]:
    tokens = input_path.read_text(encoding="utf-8").split()
    if not tokens:
        raise ValueError("input must start with the element count")

    n = int(tokens[0])
    values = [int(token) for token in tokens[1:]]
    if len(values) != n:
        raise ValueError(f"declared {n} elements but found {len(values)}")
    return values


def format_values(values: list[int]) -> str:
    return " ".join(str(value) for value in values)


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_flag_time_merge_sort = False

    for argument in sys.argv[1:]:
        if argument == "--time-merge-sort":
            time_flag_time_merge_sort = True
        else:
            input_path = Path(argument)

    try:
        values = read_input(input_path)

        if time_flag_time_merge_sort:
            start = time.perf_counter()
            sorted_values = merge_sort(values)
            elapsed = time.perf_counter() - start
            print(f"merge_sort_seconds={elapsed:.9f}", file=sys.stderr)
        else:
            sorted_values = merge_sort(values)

        print(format_values(sorted_values))
    except Exception as error:  # noqa: BLE001 - keep command-line error reporting simple.
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
