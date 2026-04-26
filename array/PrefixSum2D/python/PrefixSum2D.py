from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class RectQuery:
    r1: int
    c1: int
    r2: int
    c2: int


class PrefixSum2D:
    def __init__(self, matrix: Sequence[Sequence[int]]) -> None:
        rows = len(matrix)
        cols = len(matrix[0]) if rows else 0
        self._prefix = [[0] * (cols + 1) for _ in range(rows + 1)]

        for r in range(rows):
            for c in range(cols):
                self._prefix[r + 1][c + 1] = (
                    matrix[r][c]
                    + self._prefix[r][c + 1]
                    + self._prefix[r + 1][c]
                    - self._prefix[r][c]
                )

    def rectangle_sum(self, r1: int, c1: int, r2: int, c2: int) -> int:
        return (
            self._prefix[r2 + 1][c2 + 1]
            - self._prefix[r1][c2 + 1]
            - self._prefix[r2 + 1][c1]
            + self._prefix[r1][c1]
        )


def answer_rectangle_queries(
    matrix: Sequence[Sequence[int]], queries: Iterable[RectQuery]
) -> list[int]:
    prefix_sum = PrefixSum2D(matrix)
    return [
        prefix_sum.rectangle_sum(query.r1, query.c1, query.r2, query.c2)
        for query in queries
    ]
