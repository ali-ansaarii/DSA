from __future__ import annotations


def merge_sort(values: list[int]) -> list[int]:
    """Return a stable, nondecreasing ordering of the input values."""
    sorted_values = list(values)
    buffer = [0] * len(sorted_values)

    def sort_range(left: int, right: int) -> None:
        if right - left <= 1:
            return

        mid = left + (right - left) // 2
        sort_range(left, mid)
        sort_range(mid, right)

        i = left
        j = mid
        k = left

        while i < mid and j < right:
            if sorted_values[i] <= sorted_values[j]:
                buffer[k] = sorted_values[i]
                i += 1
            else:
                buffer[k] = sorted_values[j]
                j += 1
            k += 1

        while i < mid:
            buffer[k] = sorted_values[i]
            i += 1
            k += 1

        while j < right:
            buffer[k] = sorted_values[j]
            j += 1
            k += 1

        sorted_values[left:right] = buffer[left:right]

    sort_range(0, len(sorted_values))
    return sorted_values
