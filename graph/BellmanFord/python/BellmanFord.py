from dataclasses import dataclass
from enum import Enum


I64_MIN = -(1 << 63)
I64_MAX = (1 << 63) - 1


@dataclass(frozen=True)
class Edge:
    source: int
    target: int
    weight: int


class BellmanFordStatus(Enum):
    OK = "ok"
    NEGATIVE_CYCLE = "negative_cycle"
    OVERFLOW = "overflow"


@dataclass
class BellmanFordResult:
    status: BellmanFordStatus
    distances: list[int | None]


def _checked_add(left: int, right: int) -> int | None:
    total = left + right
    if total < I64_MIN or total > I64_MAX:
        return None
    return total


def bellman_ford(node_count: int, edges: list[Edge], start: int) -> BellmanFordResult:
    distances: list[int | None] = [None] * node_count
    distances[start] = 0

    for _ in range(node_count - 1):
        updated = False

        for edge in edges:
            source_distance = distances[edge.source]
            if source_distance is None:
                continue

            candidate = _checked_add(source_distance, edge.weight)
            if candidate is None:
                return BellmanFordResult(BellmanFordStatus.OVERFLOW, distances)

            target_distance = distances[edge.target]
            if target_distance is None or candidate < target_distance:
                distances[edge.target] = candidate
                updated = True

        if not updated:
            break

    for edge in edges:
        source_distance = distances[edge.source]
        if source_distance is None:
            continue

        candidate = _checked_add(source_distance, edge.weight)
        if candidate is None:
            return BellmanFordResult(BellmanFordStatus.OVERFLOW, distances)

        target_distance = distances[edge.target]
        if target_distance is None or candidate < target_distance:
            return BellmanFordResult(BellmanFordStatus.NEGATIVE_CYCLE, distances)

    return BellmanFordResult(BellmanFordStatus.OK, distances)
