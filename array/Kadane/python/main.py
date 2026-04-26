from __future__ import annotations

import sys
import time
from pathlib import Path

from Kadane import KadaneResult, max_subarray_kadane


def read_input(input_path: Path) -> list[int]:
    tokens = input_path.read_text(encoding="utf-8").split()
    if not tokens:
        raise ValueError("input must start with a positive element count")

    n = int(tokens[0])
    if n <= 0:
        raise ValueError("input must start with a positive element count")

    if len(tokens) != n + 1:
        raise ValueError(f"expected {n} array values, found {len(tokens) - 1}")

    return [int(token) for token in tokens[1:]]


def format_result(result: KadaneResult, values: list[int]) -> str:
    subarray = " ".join(str(value) for value in values[result.start_index : result.end_index + 1])
    return "\n".join(
        [
            f"maximum_sum: {result.maximum_sum}",
            f"start_index: {result.start_index}",
            f"end_index: {result.end_index}",
            f"subarray: {subarray}",
        ]
    )


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_kadane = False

    for argument in sys.argv[1:]:
        if argument == "--time-kadane":
            time_kadane = True
        else:
            input_path = Path(argument)

    try:
        values = read_input(input_path)

        if time_kadane:
            start = time.perf_counter_ns()
            result = max_subarray_kadane(values)
            elapsed_ns = time.perf_counter_ns() - start
        else:
            result = max_subarray_kadane(values)
            elapsed_ns = None

        print(format_result(result, values))
        if elapsed_ns is not None:
            print(f"algorithm_time_ns: {elapsed_ns}")
    except Exception as error:  # noqa: BLE001 - command-line runner should report any parse/runtime error.
        print(f"error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
