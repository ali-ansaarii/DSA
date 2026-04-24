def build_difference_array(values):
    if not values:
        return []

    diff = [0] * len(values)
    diff[0] = values[0]
    for index in range(1, len(values)):
        diff[index] = values[index] - values[index - 1]
    return diff


def apply_range_add(diff, left, right, delta):
    diff[left] += delta
    if right + 1 < len(diff):
        diff[right + 1] -= delta


def reconstruct_values(diff):
    if not diff:
        return []

    values = [0] * len(diff)
    values[0] = diff[0]
    for index in range(1, len(diff)):
        values[index] = values[index - 1] + diff[index]
    return values
