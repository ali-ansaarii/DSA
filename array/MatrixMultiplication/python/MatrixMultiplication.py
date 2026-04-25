from __future__ import annotations

Matrix = list[list[int]]


def multiply_matrices(left: Matrix, right: Matrix) -> Matrix:
    if not left or not right:
        raise ValueError("matrices must be non-empty")

    rows = len(left)
    shared = len(left[0])
    right_rows = len(right)
    cols = len(right[0])

    if shared == 0 or cols == 0 or shared != right_rows:
        raise ValueError("matrix dimensions are incompatible")
    if any(len(row) != shared for row in left):
        raise ValueError("left matrix rows have inconsistent lengths")
    if any(len(row) != cols for row in right):
        raise ValueError("right matrix rows have inconsistent lengths")

    result = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for k in range(shared):
            value = left[i][k]
            for j in range(cols):
                result[i][j] += value * right[k][j]
    return result
