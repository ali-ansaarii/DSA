from collections.abc import Sequence


def DFS(graph: Sequence[Sequence[int]], start: int) -> list[int]:
    order: list[int] = []
    visited = [False] * len(graph)
    stack = [start]

    while stack:
        node = stack.pop()

        if visited[node]:
            continue

        visited[node] = True
        order.append(node)

        for neighbor in reversed(graph[node]):
            if not visited[neighbor]:
                stack.append(neighbor)

    return order
