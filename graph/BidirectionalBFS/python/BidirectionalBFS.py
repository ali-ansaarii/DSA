from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class BidirectionalBFSResult:
    distance: int
    path: list[int]


def _build_path(
    meeting: int,
    parent_from_source: Sequence[int],
    parent_from_target: Sequence[int],
) -> list[int]:
    left: list[int] = []
    vertex = meeting
    while vertex != -1:
        left.append(vertex)
        if parent_from_source[vertex] == vertex:
            break
        vertex = parent_from_source[vertex]
    left.reverse()

    path = left[:]
    vertex = parent_from_target[meeting]
    while vertex != -1 and vertex != meeting:
        path.append(vertex)
        if parent_from_target[vertex] == vertex:
            break
        vertex = parent_from_target[vertex]
    return path


def _expand_one_level(
    frontier: deque[int],
    parent_this_side: list[int],
    parent_other_side: Sequence[int],
    graph: Sequence[Sequence[int]],
) -> int:
    for _ in range(len(frontier)):
        current = frontier.popleft()
        for neighbor in graph[current]:
            if parent_this_side[neighbor] != -1:
                continue

            parent_this_side[neighbor] = current
            if parent_other_side[neighbor] != -1:
                return neighbor
            frontier.append(neighbor)
    return -1


def shortest_path_bidirectional_bfs(
    graph: Sequence[Sequence[int]],
    source: int,
    target: int,
) -> BidirectionalBFSResult:
    if source == target:
        return BidirectionalBFSResult(distance=0, path=[source])

    n = len(graph)
    parent_from_source = [-1] * n
    parent_from_target = [-1] * n
    source_frontier: deque[int] = deque([source])
    target_frontier: deque[int] = deque([target])

    parent_from_source[source] = source
    parent_from_target[target] = target

    while source_frontier and target_frontier:
        if len(source_frontier) <= len(target_frontier):
            meeting = _expand_one_level(
                source_frontier,
                parent_from_source,
                parent_from_target,
                graph,
            )
        else:
            meeting = _expand_one_level(
                target_frontier,
                parent_from_target,
                parent_from_source,
                graph,
            )

        if meeting != -1:
            path = _build_path(meeting, parent_from_source, parent_from_target)
            return BidirectionalBFSResult(distance=len(path) - 1, path=path)

    return BidirectionalBFSResult(distance=-1, path=[])
