from collections import deque
from collections.abc import Sequence


def BFS(graph: Sequence[Sequence[int]], start: int) -> list[int]:
    order: list[int] = []
    visited = [False] * len(graph)
    queue: deque[int] = deque([start])
    visited[start] = True

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)

    return order
