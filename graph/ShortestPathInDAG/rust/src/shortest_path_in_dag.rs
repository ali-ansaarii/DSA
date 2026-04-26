use std::collections::VecDeque;

pub const INF: i64 = i64::MAX / 4;

#[derive(Clone, Debug)]
pub struct Edge {
    pub from: usize,
    pub to: usize,
    pub weight: i64,
}

pub fn shortest_path_in_dag(
    vertex_count: usize,
    edges: &[Edge],
    source: usize,
) -> Result<Vec<i64>, String> {
    if source >= vertex_count {
        return Err(String::from("source vertex is out of range"));
    }

    let mut adjacency = vec![Vec::<(usize, i64)>::new(); vertex_count];
    let mut indegree = vec![0usize; vertex_count];

    for edge in edges {
        if edge.from >= vertex_count || edge.to >= vertex_count {
            return Err(String::from("edge endpoint is out of range"));
        }
        adjacency[edge.from].push((edge.to, edge.weight));
        indegree[edge.to] += 1;
    }

    let mut ready = VecDeque::new();
    for (vertex, degree) in indegree.iter().enumerate() {
        if *degree == 0 {
            ready.push_back(vertex);
        }
    }

    let mut topological_order = Vec::with_capacity(vertex_count);
    while let Some(vertex) = ready.pop_front() {
        topological_order.push(vertex);
        for (neighbor, _) in &adjacency[vertex] {
            indegree[*neighbor] -= 1;
            if indegree[*neighbor] == 0 {
                ready.push_back(*neighbor);
            }
        }
    }

    if topological_order.len() != vertex_count {
        return Err(String::from("input graph is not a DAG"));
    }

    let mut distance = vec![INF; vertex_count];
    distance[source] = 0;

    for vertex in topological_order {
        if distance[vertex] == INF {
            continue;
        }
        for (neighbor, weight) in &adjacency[vertex] {
            let candidate = distance[vertex] + *weight;
            if candidate < distance[*neighbor] {
                distance[*neighbor] = candidate;
            }
        }
    }

    Ok(distance)
}
