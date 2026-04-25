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


class QueryType(Enum):
    ADD = auto()
    SUM = auto()


@dataclass(frozen=True)
class Query:
    type: QueryType
    left: int
    right: int
    delta: int


class SegmentTree:
    def __init__(self, initial_values: Sequence[int]) -> None:
        self._n = len(initial_values)
        self._tree = [0] * (2 * self._n)
        for index, value in enumerate(initial_values):
            self._tree[self._n + index] = value
        for node in range(self._n - 1, 0, -1):
            self._tree[node] = checked_add(self._tree[2 * node], self._tree[2 * node + 1])

    def add(self, index: int, delta: int) -> None:
        node = index + self._n
        self._tree[node] = checked_add(self._tree[node], delta)
        node //= 2
        while node > 0:
            self._tree[node] = checked_add(self._tree[2 * node], self._tree[2 * node + 1])
            node //= 2

    def range_sum(self, left: int, right: int) -> int:
        result = 0
        l = left + self._n
        r = right + self._n + 1
        while l < r:
            if l & 1:
                result = checked_add(result, self._tree[l])
                l += 1
            if r & 1:
                r -= 1
                result = checked_add(result, self._tree[r])
            l //= 2
            r //= 2
        return result


def process_segment_tree_queries(initial_values: Sequence[int], queries: Sequence[Query]) -> list[int]:
    tree = SegmentTree(initial_values)
    results: list[int] = []
    for query in queries:
        if query.type is QueryType.ADD:
            tree.add(query.left, query.delta)
        else:
            results.append(tree.range_sum(query.left, query.right))
    return results
