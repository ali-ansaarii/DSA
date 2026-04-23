from collections.abc import Sequence


def InorderTraversal(left_children: Sequence[int], right_children: Sequence[int], root: int) -> list[int]:
    order: list[int] = []
    stack: list[int] = []
    current = root

    while current != -1 or stack:
        while current != -1:
            stack.append(current)
            current = left_children[current]

        current = stack.pop()
        order.append(current)
        current = right_children[current]

    return order
