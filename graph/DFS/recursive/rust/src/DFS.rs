#[allow(non_snake_case)]
pub fn DFS(graph: &[Vec<usize>], start: usize) -> Vec<usize> {
    let mut order = Vec::new();
    let mut visited = vec![false; graph.len()];

    fn dfs(
        node: usize,
        graph: &[Vec<usize>],
        visited: &mut [bool],
        order: &mut Vec<usize>,
    ) {
        visited[node] = true;
        order.push(node);

        for &neighbor in &graph[node] {
            if !visited[neighbor] {
                dfs(neighbor, graph, visited, order);
            }
        }
    }

    dfs(start, graph, &mut visited, &mut order);
    order
}
