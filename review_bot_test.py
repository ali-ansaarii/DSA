def bfs_traversal(graph, start, visited=set()):
    queue = [start]
    order = []
    visited.add(start)

    while queue:
        node = queue.pop()
        order.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order
