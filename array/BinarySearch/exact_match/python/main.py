from __future__ import annotations

import sys
import time

from BinarySearchExact import binary_search_exact


def parse_args(argv: list[str]) -> tuple[str, bool]:
    input_path: str | None = None
    benchmark_mode = False

    for argument in argv[1:]:
        if argument == "--time-exact":
            benchmark_mode = True
        elif input_path is None:
            input_path = argument
        else:
            raise ValueError("Usage: main.py <input-file> [--time-exact]")

    if input_path is None:
        raise ValueError("Usage: main.py <input-file> [--time-exact]")

    return input_path, benchmark_mode


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
        input_path, benchmark_mode = parse_args(argv)
        values, queries = read_input(input_path)
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1

    start_time = time.perf_counter()
    results = [binary_search_exact(values, query) for query in queries]
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    if benchmark_mode:
        print(f"Exact binary search time: {elapsed_ms:.3f} ms")
        return 0

    print("Exact-match results:", *results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
