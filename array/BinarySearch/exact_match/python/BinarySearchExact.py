def binary_search_exact(values: list[int], target: int) -> int:
    left = 0
    right = len(values) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if values[mid] == target:
            return mid

        if values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
