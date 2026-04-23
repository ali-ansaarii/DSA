from collections.abc import Sequence


def PostorderTraversal(left_children: Sequence[int], right_children: Sequence[int], root: int) -> list[int]:
    order: list[int] = []

    def traverse(node: int) -> None:
        left_child = left_children[node]
        if left_child != -1:
            traverse(left_child)

        right_child = right_children[node]
        if right_child != -1:
            traverse(right_child)

        order.append(node)

    traverse(root)
    return order
