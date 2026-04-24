MIN_I64 = -(1 << 63)
MAX_I64 = (1 << 63) - 1


def _checked_i64(value: int) -> int | None:
    if value < MIN_I64 or value > MAX_I64:
        return None
    return value


def min_window_at_least_target(values: list[int], target: int) -> tuple[int, int, int] | None:
    window_sum = 0
    left = 0
    best_length = -1
    best_left = -1
    best_right = -1

    for right, value in enumerate(values):
        window_sum += value
        if _checked_i64(window_sum) is None:
            return None

        while window_sum >= target:
            current_length = right - left + 1
            if best_length == -1 or current_length < best_length:
                best_length = current_length
                best_left = left
                best_right = right
            window_sum -= values[left]
            if _checked_i64(window_sum) is None:
                return None
            left += 1

    return best_length, best_left, best_right
