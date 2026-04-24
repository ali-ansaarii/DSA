I64_MIN = -(1 << 63)
I64_MAX = (1 << 63) - 1


def _checked_add(left: int, right: int) -> int | None:
    total = left + right
    if total < I64_MIN or total > I64_MAX:
        return None
    return total


def _checked_sub(left: int, right: int) -> int | None:
    total = left - right
    if total < I64_MIN or total > I64_MAX:
        return None
    return total


def build_prefix_sums(values: list[int]) -> list[int] | None:
    prefix = [0] * (len(values) + 1)
    for index, value in enumerate(values):
        total = _checked_add(prefix[index], value)
        if total is None:
            return None
        prefix[index + 1] = total
    return prefix


def range_sum(prefix: list[int], left: int, right: int) -> int | None:
    return _checked_sub(prefix[right + 1], prefix[left])
