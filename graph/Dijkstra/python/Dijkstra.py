from __future__ import annotations

import heapq
from collections.abc import Sequence

INF = 10**30


def Dijkstra(graph: Sequence[Sequence[tuple[int, int]]], start: int) -> list[int]:
    distances = [INF] * len(graph)
    min_heap: list[tuple[int, int]] = [(0, start)]
    distances[start] = 0

    while min_heap:
        distance, node = heapq.heappop(min_heap)

        if distance != distances[node]:
            continue

        for neighbor, weight in graph[node]:
            candidate = distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                heapq.heappush(min_heap, (candidate, neighbor))

    return distances
