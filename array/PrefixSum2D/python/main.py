from __future__ import annotations

import sys
import time
from pathlib import Path

from PrefixSum2D import RectQuery, answer_rectangle_queries


def parse_input(input_path: Path) -> tuple[list[list[int]], list[RectQuery]]:
    values = input_path.read_text(encoding="utf-8").split()
    index = 0

    rows = int(values[index])
    index += 1
    cols = int(values[index])
    index += 1

    matrix: list[list[int]] = []
    for _ in range(rows):
        row = [int(values[index + c]) for c in range(cols)]
        index += cols
        matrix.append(row)

    query_count = int(values[index])
    index += 1
    queries: list[RectQuery] = []
    for _ in range(query_count):
        r1 = int(values[index])
        c1 = int(values[index + 1])
        r2 = int(values[index + 2])
        c2 = int(values[index + 3])
        index += 4
        queries.append(RectQuery(r1, c1, r2, c2))

    return matrix, queries


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_flag_time_prefix_sum_2d = False

    for argument in sys.argv[1:]:
        if argument == "--time-prefix-sum-2d":
            time_flag_time_prefix_sum_2d = True
        else:
            input_path = Path(argument)

    matrix, queries = parse_input(input_path)

    start = time.perf_counter()
    answers = answer_rectangle_queries(matrix, queries)
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    if time_flag_time_prefix_sum_2d:
        print(f"algorithm_time_ms {elapsed_ms:.3f}", file=sys.stderr)

    sys.stdout.write("".join(f"{answer}\n" for answer in answers))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
