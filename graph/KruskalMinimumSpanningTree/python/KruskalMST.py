from dataclasses import dataclass
from enum import Enum


I64_MIN = -(1 << 63)
I64_MAX = (1 << 63) - 1


@dataclass(frozen=True)
class Edge:
    source: int
    target: int
    weight: int


class KruskalStatus(Enum):
    OK = "ok"
    DISCONNECTED = "disconnected"
    OVERFLOW = "overflow"


@dataclass
class KruskalResult:
    status: KruskalStatus
    total_weight: int
    chosen_edges: list[Edge]


class DisjointSetUnion:
    def __init__(self, node_count: int) -> None:
        self.parent = list(range(node_count))
        self.size = [1] * node_count

    def find(self, node: int) -> int:
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def unite(self, left: int, right: int) -> bool:
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return False
        if self.size[left] < self.size[right]:
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]
        return True


def _checked_add(left: int, right: int) -> int | None:
    total = left + right
    if total < I64_MIN or total > I64_MAX:
        return None
    return total


def _normalize(edge: Edge) -> Edge:
    if edge.source <= edge.target:
        return edge
    return Edge(edge.target, edge.source, edge.weight)


def kruskal_mst(node_count: int, edges: list[Edge]) -> KruskalResult:
    sorted_edges = sorted((_normalize(edge) for edge in edges), key=lambda edge: (edge.weight, edge.source, edge.target))
    dsu = DisjointSetUnion(node_count)
    chosen_edges: list[Edge] = []
    total_weight = 0

    for edge in sorted_edges:
        if not dsu.unite(edge.source, edge.target):
            continue

        updated = _checked_add(total_weight, edge.weight)
        if updated is None:
            return KruskalResult(KruskalStatus.OVERFLOW, total_weight, chosen_edges)

        total_weight = updated
        chosen_edges.append(edge)

        if len(chosen_edges) == node_count - 1:
            return KruskalResult(KruskalStatus.OK, total_weight, chosen_edges)

    return KruskalResult(KruskalStatus.DISCONNECTED, total_weight, chosen_edges)
