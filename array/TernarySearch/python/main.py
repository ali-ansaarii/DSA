from __future__ import annotations

import sys
from pathlib import Path
from time import perf_counter_ns

from TernarySearch import find_unimodal_maximum


def read_input(input_path: Path) -> list[int]:
    tokens = input_path.read_text(encoding="utf-8").split()
    if not tokens:
        raise ValueError("input must start with a positive element count")

    n = int(tokens[0])
    if n <= 0:
        raise ValueError("input must start with a positive element count")
    if len(tokens) - 1 < n:
        raise ValueError("input ended before all array values were read")

    return [int(token) for token in tokens[1 : n + 1]]


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_ternary_search = False

    for argument in sys.argv[1:]:
        if argument == "--time-ternary-search":
            time_ternary_search = True
        else:
            input_path = Path(argument)

    try:
        values = read_input(input_path)

        elapsed_ns = 0
        if time_ternary_search:
            start = perf_counter_ns()
            result = find_unimodal_maximum(values)
            elapsed_ns = perf_counter_ns() - start
        else:
            result = find_unimodal_maximum(values)

        print(f"Maximum index: {result.index}")
        print(f"Maximum value: {result.value}")
        if time_ternary_search:
            print(f"Algorithm time (ns): {elapsed_ns}")
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
