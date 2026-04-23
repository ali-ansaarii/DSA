from collections.abc import Sequence


def InorderTraversal(left_children: Sequence[int], right_children: Sequence[int], root: int) -> list[int]:
    order: list[int] = []

    def traverse(node: int) -> None:
        left_child = left_children[node]
        if left_child != -1:
            traverse(left_child)

        order.append(node)

        right_child = right_children[node]
        if right_child != -1:
            traverse(right_child)

    traverse(root)
    return order
