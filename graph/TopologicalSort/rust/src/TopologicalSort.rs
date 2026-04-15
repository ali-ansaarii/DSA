use std::collections::VecDeque;

#[allow(non_snake_case)]
pub fn TopologicalSort(graph: &[Vec<usize>]) -> Vec<usize> {
    let mut indegree = vec![0usize; graph.len()];
    for neighbors in graph {
        for &neighbor in neighbors {
            indegree[neighbor] += 1;
        }
    }

    let mut ready = VecDeque::new();
    for (node, &degree) in indegree.iter().enumerate() {
        if degree == 0 {
            ready.push_back(node);
        }
    }

    let mut order = Vec::new();
    while let Some(node) = ready.pop_front() {
        order.push(node);

        for &neighbor in &graph[node] {
            indegree[neighbor] -= 1;
            if indegree[neighbor] == 0 {
                ready.push_back(neighbor);
            }
        }
    }

    order
}
