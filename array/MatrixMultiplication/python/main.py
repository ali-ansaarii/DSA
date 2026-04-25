from __future__ import annotations

import sys
import time
from pathlib import Path

from MatrixMultiplication import Matrix, multiply_matrices


def _read_matrix(tokens: list[str], index: int, rows: int, cols: int) -> tuple[Matrix, int]:
    matrix: Matrix = []
    for _ in range(rows):
        row: list[int] = []
        for _ in range(cols):
            if index >= len(tokens):
                raise ValueError("failed to read matrix value")
            row.append(int(tokens[index]))
            index += 1
        matrix.append(row)
    return matrix, index


def _parse_input(input_path: Path) -> tuple[Matrix, Matrix]:
    tokens = input_path.read_text(encoding="utf-8").split()
    if len(tokens) < 4:
        raise ValueError("input is too short")

    index = 0
    m = int(tokens[index])
    index += 1
    n = int(tokens[index])
    index += 1
    left, index = _read_matrix(tokens, index, m, n)

    if index + 2 > len(tokens):
        raise ValueError("failed to read second matrix dimensions")
    n2 = int(tokens[index])
    index += 1
    p = int(tokens[index])
    index += 1
    if n != n2:
        raise ValueError("matrix dimensions are incompatible")
    right, index = _read_matrix(tokens, index, n2, p)
    return left, right


def _print_matrix(matrix: Matrix) -> None:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    print(f"{rows} {cols}")
    for row in matrix:
        print(" ".join(str(value) for value in row))


def main() -> int:
    input_path = Path("inputs/input.txt")
    time_matrix_multiplication = False

    for argument in sys.argv[1:]:
        if argument == "--time-matrix-multiplication":
            time_matrix_multiplication = True
        else:
            input_path = Path(argument)

    try:
        left, right = _parse_input(input_path)
        start = time.perf_counter()
        result = multiply_matrices(left, right)
        elapsed = time.perf_counter() - start

        if time_matrix_multiplication:
            print(f"matrix_multiplication_ms={elapsed * 1000:.6f}", file=sys.stderr)

        _print_matrix(result)
    except Exception as error:  # noqa: BLE001 - command-line runner should report any parse/runtime error.
        print(f"error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
