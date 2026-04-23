from collections.abc import Sequence


def PreorderTraversal(left_children: Sequence[int], right_children: Sequence[int], root: int) -> list[int]:
    order: list[int] = []

    def dfs(node: int) -> None:
        order.append(node)

        left_child = left_children[node]
        if left_child != -1:
            dfs(left_child)

        right_child = right_children[node]
        if right_child != -1:
            dfs(right_child)

    dfs(root)
    return order
