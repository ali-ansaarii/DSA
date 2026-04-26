from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class KadaneResult:
    maximum_sum: int
    start_index: int
    end_index: int


def max_subarray_kadane(values: Sequence[int]) -> KadaneResult:
    """Return the maximum non-empty subarray sum and inclusive bounds."""
    if not values:
        raise ValueError("Kadane's Algorithm requires a non-empty array")

    current_sum = values[0]
    best_sum = values[0]
    current_start = 0
    best_start = 0
    best_end = 0

    for index in range(1, len(values)):
        value = values[index]
        extended_sum = current_sum + value

        if extended_sum < value:
            current_sum = value
            current_start = index
        else:
            current_sum = extended_sum

        if current_sum > best_sum:
            best_sum = current_sum
            best_start = current_start
            best_end = index

    return KadaneResult(best_sum, best_start, best_end)
