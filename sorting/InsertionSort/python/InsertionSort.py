from __future__ import annotations


def insertion_sort(values: list[int]) -> None:
    """Sort values in-place using stable classical insertion sort."""
    for i in range(1, len(values)):
        key = values[i]
        j = i

        while j > 0 and values[j - 1] > key:
            values[j] = values[j - 1]
            j -= 1

        values[j] = key
