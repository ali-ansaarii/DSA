from collections.abc import Sequence


def DFS(graph: Sequence[Sequence[int]], start: int) -> list[int]:
    order: list[int] = []
    visited = [False] * len(graph)

    def dfs(node: int) -> None:
        visited[node] = True
        order.append(node)

        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor)

    dfs(start)
    return order
