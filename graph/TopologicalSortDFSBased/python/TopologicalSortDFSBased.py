from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class TopologicalSortResult:
    has_cycle: bool
    order: list[int]


def topological_sort_dfs_based(vertex_count: int, edges: Iterable[tuple[int, int]]) -> TopologicalSortResult:
    if vertex_count < 0:
        raise ValueError("vertex count must be non-negative")

    graph: list[list[int]] = [[] for _ in range(vertex_count)]
    for from_vertex, to_vertex in edges:
        if not (0 <= from_vertex < vertex_count and 0 <= to_vertex < vertex_count):
            raise ValueError("edge endpoint is outside the vertex range")
        graph[from_vertex].append(to_vertex)

    color = [0] * vertex_count  # 0 = unvisited, 1 = visiting, 2 = done
    postorder: list[int] = []

    for start in range(vertex_count):
        if color[start] != 0:
            continue

        color[start] = 1
        stack: list[tuple[int, int]] = [(start, 0)]

        while stack:
            vertex, next_index = stack[-1]
            if next_index < len(graph[vertex]):
                neighbor = graph[vertex][next_index]
                stack[-1] = (vertex, next_index + 1)

                if color[neighbor] == 0:
                    color[neighbor] = 1
                    stack.append((neighbor, 0))
                elif color[neighbor] == 1:
                    return TopologicalSortResult(True, [])
            else:
                color[vertex] = 2
                postorder.append(vertex)
                stack.pop()

    postorder.reverse()
    return TopologicalSortResult(False, postorder)
