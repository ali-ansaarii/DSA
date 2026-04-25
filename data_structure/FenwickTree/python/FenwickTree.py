from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Sequence

MIN_I64 = -(1 << 63)
MAX_I64 = (1 << 63) - 1


def checked_i64(value: int) -> int:
    if value < MIN_I64 or value > MAX_I64:
        raise OverflowError
    return value


def checked_add(a: int, b: int) -> int:
    return checked_i64(a + b)


def checked_sub(a: int, b: int) -> int:
    return checked_i64(a - b)


class QueryType(Enum):
    ADD = auto()
    SUM = auto()


@dataclass(frozen=True)
class Query:
    type: QueryType
    left: int
    right: int
    delta: int


class FenwickTree:
    def __init__(self, size: int) -> None:
        self._tree = [0] * (size + 1)

    def add(self, index: int, delta: int) -> None:
        i = index + 1
        while i < len(self._tree):
            self._tree[i] = checked_add(self._tree[i], delta)
            i += i & -i

    def prefix_sum(self, index: int) -> int:
        result = 0
        i = index + 1
        while i > 0:
            result = checked_add(result, self._tree[i])
            i -= i & -i
        return result

    def range_sum(self, left: int, right: int) -> int:
        right_prefix = self.prefix_sum(right)
        if left == 0:
            return right_prefix
        return checked_sub(right_prefix, self.prefix_sum(left - 1))


def process_fenwick_queries(initial_values: Sequence[int], queries: Sequence[Query]) -> list[int]:
    tree = FenwickTree(len(initial_values))
    for index, value in enumerate(initial_values):
        tree.add(index, value)

    results: list[int] = []
    for query in queries:
        if query.type is QueryType.ADD:
            tree.add(query.left, query.delta)
        else:
            results.append(tree.range_sum(query.left, query.right))

    return results
