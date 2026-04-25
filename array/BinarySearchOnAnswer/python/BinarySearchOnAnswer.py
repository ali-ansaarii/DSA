from __future__ import annotations


def can_partition_with_max_group_sum(values: list[int], max_groups: int, limit: int) -> bool:
    """Return whether values can be split into at most max_groups under limit."""
    if max_groups <= 0:
        return False

    groups_used = 1
    current_sum = 0

    for value in values:
        if value < 0:
            raise ValueError("Binary Search on Answer partition baseline requires non-negative values")
        if value > limit:
            return False
        if current_sum + value > limit:
            groups_used += 1
            current_sum = value
            if groups_used > max_groups:
                return False
        else:
            current_sum += value

    return True


def minimize_largest_group_sum(values: list[int], max_groups: int) -> int:
    """Minimize the largest contiguous group sum using answer-space binary search."""
    if not values:
        return 0
    if max_groups <= 0:
        raise ValueError("max_groups must be positive")

    low = max(values)
    high = sum(values)

    while low < high:
        mid = low + (high - low) // 2
        if can_partition_with_max_group_sum(values, max_groups, mid):
            high = mid
        else:
            low = mid + 1

    return low
