from dataclasses import dataclass
from enum import Enum
import heapq


I64_MIN = -(1 << 63)
I64_MAX = (1 << 63) - 1


@dataclass(frozen=True)
class Edge:
    source: int
    target: int
    weight: int


class PrimStatus(Enum):
    OK = "ok"
    DISCONNECTED = "disconnected"
    OVERFLOW = "overflow"


@dataclass
class PrimResult:
    status: PrimStatus
    total_weight: int
    chosen_edges: list[Edge]


def _checked_add(left: int, right: int) -> int | None:
    total = left + right
    if total < I64_MIN or total > I64_MAX:
        return None
    return total


def _normalize(edge: Edge) -> Edge:
    if edge.source <= edge.target:
        return edge
    return Edge(edge.target, edge.source, edge.weight)


def prim_mst(node_count: int, edges: list[Edge]) -> PrimResult:
    if node_count <= 1:
        return PrimResult(PrimStatus.OK, 0, [])

    adjacency: list[list[Edge]] = [[] for _ in range(node_count)]
    for edge in edges:
        normalized = _normalize(edge)
        adjacency[normalized.source].append(Edge(normalized.source, normalized.target, normalized.weight))
        adjacency[normalized.target].append(Edge(normalized.target, normalized.source, normalized.weight))

    visited = [False] * node_count
    heap: list[tuple[int, int, int, int]] = []
    chosen_edges: list[Edge] = []
    total_weight = 0

    def push_candidates(node: int) -> None:
        for edge in adjacency[node]:
            if visited[edge.target]:
                continue
            normalized = _normalize(Edge(edge.source, edge.target, edge.weight))
            heapq.heappush(heap, (normalized.weight, normalized.source, normalized.target, edge.target))

    visited[0] = True
    visited_count = 1
    push_candidates(0)

    while heap and visited_count < node_count:
        weight, source, target, next_node = heapq.heappop(heap)
        if visited[next_node]:
            continue

        updated = _checked_add(total_weight, weight)
        if updated is None:
            return PrimResult(PrimStatus.OVERFLOW, total_weight, chosen_edges)

        total_weight = updated
        chosen_edges.append(Edge(source, target, weight))
        visited[next_node] = True
        visited_count += 1
        push_candidates(next_node)

    if visited_count != node_count:
        return PrimResult(PrimStatus.DISCONNECTED, total_weight, chosen_edges)

    return PrimResult(PrimStatus.OK, total_weight, chosen_edges)
