from __future__ import annotations

from enum import Enum
from typing import NamedTuple


class OperationType(Enum):
    UNION = "union"
    CONNECTED = "connected"
    FIND = "find"


class Operation(NamedTuple):
    type: OperationType
    first: int
    second: int


def DisjointSetUnion(n: int, operations: list[Operation]) -> list[str]:
    parent = list(range(n))
    component_size = [1] * n

    def find_root(node: int) -> int:
        if parent[node] == node:
            return node

        parent[node] = find_root(parent[node])
        return parent[node]

    query_results: list[str] = []
    for operation in operations:
        if operation.type is OperationType.UNION:
            root_a = find_root(operation.first)
            root_b = find_root(operation.second)

            if root_a == root_b:
                continue

            if component_size[root_a] < component_size[root_b] or (
                component_size[root_a] == component_size[root_b] and root_a > root_b
            ):
                root_a, root_b = root_b, root_a

            parent[root_b] = root_a
            component_size[root_a] += component_size[root_b]
        elif operation.type is OperationType.CONNECTED:
            query_results.append("true" if find_root(operation.first) == find_root(operation.second) else "false")
        else:
            query_results.append(str(find_root(operation.first)))

    return query_results
