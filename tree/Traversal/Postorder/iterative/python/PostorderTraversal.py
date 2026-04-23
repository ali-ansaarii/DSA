from collections.abc import Sequence


def PostorderTraversal(left_children: Sequence[int], right_children: Sequence[int], root: int) -> list[int]:
    order: list[int] = []
    stack: list[tuple[int, bool]] = [(root, False)]

    while stack:
        node, expanded = stack.pop()

        if expanded:
            order.append(node)
            continue

        stack.append((node, True))

        right_child = right_children[node]
        if right_child != -1:
            stack.append((right_child, False))

        left_child = left_children[node]
        if left_child != -1:
            stack.append((left_child, False))

    return order
