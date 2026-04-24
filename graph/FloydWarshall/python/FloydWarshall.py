from dataclasses import dataclass
from enum import Enum


I64_MIN = -(1 << 63)
I64_MAX = (1 << 63) - 1


@dataclass(frozen=True)
class Edge:
    source: int
    target: int
    weight: int


class FloydWarshallStatus(Enum):
    OK = "ok"
    NEGATIVE_CYCLE = "negative_cycle"
    OVERFLOW = "overflow"


@dataclass
class FloydWarshallResult:
    status: FloydWarshallStatus
    distances: list[list[int | None]]


def _checked_add(left: int, right: int) -> int | None:
    total = left + right
    if total < I64_MIN or total > I64_MAX:
        return None
    return total


def floyd_warshall(node_count: int, edges: list[Edge]) -> FloydWarshallResult:
    distances: list[list[int | None]] = [[None] * node_count for _ in range(node_count)]

    for node in range(node_count):
        distances[node][node] = 0

    for edge in edges:
        current = distances[edge.source][edge.target]
        if current is None or edge.weight < current:
            distances[edge.source][edge.target] = edge.weight

    for intermediate in range(node_count):
        for source in range(node_count):
            left = distances[source][intermediate]
            if left is None:
                continue

            for target in range(node_count):
                right = distances[intermediate][target]
                if right is None:
                    continue

                candidate = _checked_add(left, right)
                if candidate is None:
                    return FloydWarshallResult(FloydWarshallStatus.OVERFLOW, distances)

                current = distances[source][target]
                if current is None or candidate < current:
                    distances[source][target] = candidate

    for node in range(node_count):
        diagonal = distances[node][node]
        if diagonal is not None and diagonal < 0:
            return FloydWarshallResult(FloydWarshallStatus.NEGATIVE_CYCLE, distances)

    return FloydWarshallResult(FloydWarshallStatus.OK, distances)
