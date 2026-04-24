def lower_bound_range_halving(values: list[int], target: int) -> int:
    left = 0
    right = len(values)

    while left < right:
        mid = left + (right - left) // 2
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left


def lower_bound_powers_of_two(values: list[int], target: int) -> int:
    position = -1
    step = 1
    while step < len(values):
        step <<= 1

    while step > 0:
        next_index = position + step
        if next_index < len(values) and values[next_index] < target:
            position = next_index
        step >>= 1

    return position + 1
