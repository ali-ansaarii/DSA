from __future__ import annotations


def selection_sort(values: list[int]) -> None:
    """Sort values in ascending order in place using classic Selection Sort."""
    n = len(values)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if values[j] < values[min_index]:
                min_index = j
        if min_index != i:
            values[i], values[min_index] = values[min_index], values[i]
