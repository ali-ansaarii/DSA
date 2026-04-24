from __future__ import annotations

import sys
import time

from BoundarySearch import lower_bound_powers_of_two, lower_bound_range_halving


def parse_args(argv: list[str]) -> tuple[str, str | None]:
    input_path: str | None = None
    method: str | None = None

    for argument in argv[1:]:
        if argument == "--time-range-halving":
            method = "range_halving"
        elif argument == "--time-powers-of-two":
            method = "powers_of_two"
        elif input_path is None:
            input_path = argument
        else:
            raise ValueError("Usage: main.py <input-file> [--time-range-halving|--time-powers-of-two]")

    if input_path is None:
        raise ValueError("Usage: main.py <input-file> [--time-range-halving|--time-powers-of-two]")

    return input_path, method


def read_input(path: str) -> tuple[list[int], list[int]]:
    with open(path, "r", encoding="utf-8") as handle:
        tokens = handle.read().split()

    if len(tokens) < 2:
        raise ValueError("Invalid input header")

    position = 0
    value_count = int(tokens[position])
    position += 1
    query_count = int(tokens[position])
    position += 1

    if value_count < 0 or query_count < 0:
        raise ValueError("Invalid input header")

    if position + value_count + query_count != len(tokens):
        raise ValueError("Input length does not match n and q")

    values = [int(token) for token in tokens[position:position + value_count]]
    position += value_count
    queries = [int(token) for token in tokens[position:position + query_count]]
    return values, queries


def main(argv: list[str]) -> int:
    try:
        input_path, method = parse_args(argv)
        values, queries = read_input(input_path)
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1

    if method is not None:
        start_time = time.perf_counter()
        if method == "range_halving":
            results = [lower_bound_range_halving(values, query) for query in queries]
        else:
            results = [lower_bound_powers_of_two(values, query) for query in queries]
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        if method == "range_halving":
            print(f"Boundary search time (range-halving): {elapsed_ms:.3f} ms")
        else:
            print(f"Boundary search time (powers-of-two): {elapsed_ms:.3f} ms")
        _ = results
        return 0

    range_results = [lower_bound_range_halving(values, query) for query in queries]
    powers_results = [lower_bound_powers_of_two(values, query) for query in queries]

    if range_results != powers_results:
        print("Boundary-search implementations disagree", file=sys.stderr)
        return 1

    print("Boundary results (range-halving):", *range_results)
    print("Boundary results (powers-of-two):", *powers_results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
