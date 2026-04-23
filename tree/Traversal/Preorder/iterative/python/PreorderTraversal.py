from collections.abc import Sequence


def PreorderTraversal(left_children: Sequence[int], right_children: Sequence[int], root: int) -> list[int]:
    order: list[int] = []
    stack = [root]

    while stack:
        node = stack.pop()
        order.append(node)

        right_child = right_children[node]
        if right_child != -1:
            stack.append(right_child)

        left_child = left_children[node]
        if left_child != -1:
            stack.append(left_child)

    return order
