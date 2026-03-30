def bfs_traversal(graph, start, visited=None):
    if visited is None:
        visited = set()

    queue = [start]
    order = []
    visited.add(start)

    while queue:
        node = queue.pop(0)
        order.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order
