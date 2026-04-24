MIN_I64 = -(1 << 63)
MAX_I64 = (1 << 63) - 1


def _checked_i64(value: int) -> int | None:
    if value < MIN_I64 or value > MAX_I64:
        return None
    return value


def best_fixed_window(values: list[int], k: int) -> tuple[int, int, int] | None:
    window_sum = sum(values[:k])
    if _checked_i64(window_sum) is None:
        return None

    best_sum = window_sum
    best_left = 0
    best_right = k - 1

    for right in range(k, len(values)):
        window_sum = window_sum - values[right - k] + values[right]
        if _checked_i64(window_sum) is None:
            return None
        left = right - k + 1
        if window_sum > best_sum:
            best_sum = window_sum
            best_left = left
            best_right = right

    return best_sum, best_left, best_right
