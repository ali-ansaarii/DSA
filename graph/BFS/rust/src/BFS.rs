use std::collections::VecDeque;

#[allow(non_snake_case)]
pub fn BFS(graph: &[Vec<usize>], start: usize) -> Vec<usize> {
    let mut order = Vec::new();
    let mut visited = vec![false; graph.len()];
    let mut queue = VecDeque::from([start]);

    visited[start] = true;

    while let Some(node) = queue.pop_front() {
        order.push(node);

        for &neighbor in &graph[node] {
            if !visited[neighbor] {
                visited[neighbor] = true;
                queue.push_back(neighbor);
            }
        }
    }

    order
}
