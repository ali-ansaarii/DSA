#[allow(non_snake_case)]
pub fn DFS(graph: &[Vec<usize>], start: usize) -> Vec<usize> {
    let mut order = Vec::new();
    let mut visited = vec![false; graph.len()];
    let mut stack = vec![start];

    while let Some(node) = stack.pop() {
        if visited[node] {
            continue;
        }

        visited[node] = true;
        order.push(node);

        for &neighbor in graph[node].iter().rev() {
            if !visited[neighbor] {
                stack.push(neighbor);
            }
        }
    }

    order
}
