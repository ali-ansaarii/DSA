from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class TernarySearchResult:
    index: int
    value: int


def find_unimodal_maximum(values: Sequence[int]) -> TernarySearchResult:
    """Return the index and value of the maximum in a non-empty unimodal array."""
    if not values:
        raise ValueError("ternary search requires a non-empty array")

    left = 0
    right = len(values) - 1

    while right > left + 3:
        third = (right - left) // 3
        mid1 = left + third
        mid2 = right - third

        if values[mid1] < values[mid2]:
            left = mid1 + 1
        elif values[mid1] > values[mid2]:
            right = mid2 - 1
        else:
            left = mid1
            right = mid2

    best_index = left
    for index in range(left + 1, right + 1):
        if values[index] > values[best_index]:
            best_index = index

    return TernarySearchResult(best_index, values[best_index])
