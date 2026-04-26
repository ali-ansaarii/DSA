from __future__ import annotations

import sys
import time
from pathlib import Path

from BinarySearchOnAnswer import minimize_largest_group_sum


def read_input(input_path: Path) -> tuple[int, list[int]]:
    tokens = input_path.read_text(encoding="utf-8").split()
    if len(tokens) < 2:
        raise ValueError("Input must start with n and k")

    n = int(tokens[0])
    k = int(tokens[1])
    if n < 0:
        raise ValueError("n must be non-negative")
    if len(tokens) < 2 + n:
        raise ValueError("Input ended before reading all array values")

    values = [int(token) for token in tokens[2 : 2 + n]]
    return k, values


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_flag_time_binary_search_on_answer = False

    for argument in sys.argv[1:]:
        if argument == "--time-binary-search-on-answer":
            time_flag_time_binary_search_on_answer = True
        else:
            input_path = Path(argument)

    try:
        k, values = read_input(input_path)

        if time_flag_time_binary_search_on_answer:
            start_ns = time.perf_counter_ns()
            answer = minimize_largest_group_sum(values, k)
            elapsed_ns = time.perf_counter_ns() - start_ns
            print(f"algorithm_time_ns {elapsed_ns}", file=sys.stderr)
        else:
            answer = minimize_largest_group_sum(values, k)

        print(answer)
    except Exception as error:  # noqa: BLE001 - keep CLI error handling compact for examples.
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
