from __future__ import annotations

import sys
import time
from pathlib import Path

from FenwickTree import MAX_I64, MIN_I64, Query, QueryType, checked_i64, process_fenwick_queries


def read_input(input_path: Path) -> tuple[list[int], list[Query]]:
    try:
        tokens = input_path.read_text(encoding="utf-8").split()
    except OSError:
        print(f"Failed to open input file: {input_path}", file=sys.stderr)
        raise SystemExit(1)

    cursor = 0

    def next_token() -> str:
        nonlocal cursor
        if cursor >= len(tokens):
            raise ValueError
        token = tokens[cursor]
        cursor += 1
        return token

    try:
        n = int(next_token())
        q = int(next_token())
    except (ValueError, OverflowError):
        print("Invalid input header.", file=sys.stderr)
        raise SystemExit(1)

    if n <= 0 or q < 0:
        print("Invalid input header.", file=sys.stderr)
        raise SystemExit(1)

    initial_values: list[int] = []
    for index in range(n):
        try:
            initial_values.append(checked_i64(int(next_token())))
        except (ValueError, OverflowError):
            print(f"Failed to read initial value at index {index}.", file=sys.stderr)
            raise SystemExit(1)

    queries: list[Query] = []
    for line_index in range(q):
        try:
            operation = next_token()
        except ValueError:
            print(f"Input ended early. Expected {q} operations.", file=sys.stderr)
            raise SystemExit(1)

        if operation == "add":
            try:
                index = int(next_token())
                delta = checked_i64(int(next_token()))
            except (ValueError, OverflowError):
                print(f"Invalid operation at line {line_index + 3}.", file=sys.stderr)
                raise SystemExit(1)
            if not (0 <= index < n):
                print(f"Invalid operation at line {line_index + 3}.", file=sys.stderr)
                raise SystemExit(1)
            queries.append(Query(QueryType.ADD, index, -1, delta))
        elif operation == "sum":
            try:
                left = int(next_token())
                right = int(next_token())
            except ValueError:
                print(f"Invalid operation at line {line_index + 3}.", file=sys.stderr)
                raise SystemExit(1)
            if not (0 <= left <= right < n):
                print(f"Invalid operation at line {line_index + 3}.", file=sys.stderr)
                raise SystemExit(1)
            queries.append(Query(QueryType.SUM, left, right, 0))
        else:
            print(f"Invalid operation at line {line_index + 3}.", file=sys.stderr)
            raise SystemExit(1)

    if cursor != len(tokens):
        print("Input size does not match header.", file=sys.stderr)
        raise SystemExit(1)

    return initial_values, queries


def print_answer(results: list[int]) -> None:
    print("Query sums:")
    for value in results:
        print(value)


def main() -> None:
    input_path = Path("inputs/input.txt")
    time_fenwick_tree = False

    for argument in sys.argv[1:]:
        if argument == "--time-fenwick-tree":
            time_fenwick_tree = True
        else:
            input_path = Path(argument)

    initial_values, queries = read_input(input_path)

    start = time.perf_counter()
    try:
        results = process_fenwick_queries(initial_values, queries)
    except OverflowError:
        print("Fenwick tree overflowed while processing the queries.", file=sys.stderr)
        raise SystemExit(1)
    end = time.perf_counter()

    if time_fenwick_tree:
        print(f"Fenwick-tree time: {(end - start) * 1000.0:.6f} ms")
    else:
        print_answer(results)


if __name__ == "__main__":
    main()
