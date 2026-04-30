from __future__ import annotations

from collections import deque
from typing import Iterable, NamedTuple

INF = 10**30


class Edge(NamedTuple):
    source: int
    target: int
    weight: int


def shortest_path_in_dag(vertex_count: int, edges: Iterable[Edge], source: int) -> list[int]:
    """Return distances from source in a weighted DAG using topological relaxation."""
    if vertex_count < 0:
        raise ValueError("vertex count cannot be negative")
    if source < 0 or source >= vertex_count:
        raise ValueError("source vertex is out of range")

    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    indegree = [0] * vertex_count

    for edge in edges:
        if not (0 <= edge.source < vertex_count and 0 <= edge.target < vertex_count):
            raise ValueError("edge endpoint is out of range")
        adjacency[edge.source].append((edge.target, edge.weight))
        indegree[edge.target] += 1

    ready = deque(vertex for vertex, degree in enumerate(indegree) if degree == 0)
    topological_order: list[int] = []

    while ready:
        vertex = ready.popleft()
        topological_order.append(vertex)
        for neighbor, _weight in adjacency[vertex]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                ready.append(neighbor)

    if len(topological_order) != vertex_count:
        raise ValueError("input graph is not a DAG")

    distance = [INF] * vertex_count
    distance[source] = 0

    for vertex in topological_order:
        if distance[vertex] == INF:
            continue
        for neighbor, weight in adjacency[vertex]:
            candidate = distance[vertex] + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate

    return distance
