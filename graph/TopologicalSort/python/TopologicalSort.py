from collections import deque
from collections.abc import Sequence


def TopologicalSort(graph: Sequence[Sequence[int]]) -> list[int]:
    indegree = [0] * len(graph)
    for neighbors in graph:
        for neighbor in neighbors:
            indegree[neighbor] += 1

    ready: deque[int] = deque(node for node, degree in enumerate(indegree) if degree == 0)
    order: list[int] = []

    while ready:
        node = ready.popleft()
        order.append(node)

        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                ready.append(neighbor)

    return order
