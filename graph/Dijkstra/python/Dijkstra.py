from __future__ import annotations

from collections import deque
import heapq
from collections.abc import Sequence

MAX_DISTANCE = (1 << 63) - 1


def Dijkstra(graph: Sequence[Sequence[tuple[int, int]]], start: int) -> tuple[list[int], list[bool]]:
    graph_reachable = [False] * len(graph)
    traversal_queue: deque[int] = deque([start])
    graph_reachable[start] = True

    while traversal_queue:
        node = traversal_queue.popleft()
        for neighbor, _weight in graph[node]:
            if not graph_reachable[neighbor]:
                graph_reachable[neighbor] = True
                traversal_queue.append(neighbor)

    distances = [0] * len(graph)
    reachable = [False] * len(graph)
    min_heap: list[tuple[int, int]] = [(0, start)]
    reachable[start] = True
    distances[start] = 0

    while min_heap:
        distance, node = heapq.heappop(min_heap)

        if not reachable[node] or distance != distances[node]:
            continue

        for neighbor, weight in graph[node]:
            if distance > MAX_DISTANCE - weight:
                continue

            candidate = distance + weight
            if not reachable[neighbor] or candidate < distances[neighbor]:
                reachable[neighbor] = True
                distances[neighbor] = candidate
                heapq.heappush(min_heap, (candidate, neighbor))

    if any(is_graph_reachable and not is_reachable for is_graph_reachable, is_reachable in zip(graph_reachable, reachable)):
        raise OverflowError("Shortest-path overflow: a path distance exceeded the signed 64-bit integer range.")

    return distances, reachable
