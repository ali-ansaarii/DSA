from __future__ import annotations

import sys
import time
from pathlib import Path

from SelectionSort import selection_sort


def read_input(input_path: Path) -> list[int]:
    tokens = input_path.read_text(encoding="utf-8").split()
    if not tokens:
        raise ValueError("input must start with the array length")

    n = int(tokens[0])
    if n < 0:
        raise ValueError("array length must be non-negative")

    values = [int(token) for token in tokens[1:]]
    if len(values) < n:
        raise ValueError("input ended before reading all array values")
    return values[:n]


def format_values(values: list[int]) -> str:
    return " ".join(str(value) for value in values)


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_flag_time_selection_sort = False

    for argument in sys.argv[1:]:
        if argument == "--time-selection-sort":
            time_flag_time_selection_sort = True
        else:
            input_path = Path(argument)

    try:
        values = read_input(input_path)

        if time_flag_time_selection_sort:
            start = time.perf_counter()
            selection_sort(values)
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            print(f"algorithm_time_ms={elapsed_ms:.6f}", file=sys.stderr)
        else:
            selection_sort(values)

        print(format_values(values))
    except Exception as error:  # noqa: BLE001 - keep command-line errors concise.
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
