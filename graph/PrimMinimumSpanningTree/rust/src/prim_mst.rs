use std::cmp::Reverse;
use std::collections::BinaryHeap;

#[derive(Clone, Copy)]
pub struct Edge {
    pub source: usize,
    pub target: usize,
    pub weight: i64,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum Status {
    Ok,
    Disconnected,
    Overflow,
}

pub struct Result {
    pub status: Status,
    pub total_weight: i64,
    pub chosen_edges: Vec<Edge>,
}

fn normalize(edge: Edge) -> Edge {
    if edge.source <= edge.target {
        edge
    } else {
        Edge {
            source: edge.target,
            target: edge.source,
            weight: edge.weight,
        }
    }
}

pub fn prim_mst(node_count: usize, edges: &[Edge]) -> Result {
    if node_count <= 1 {
        return Result {
            status: Status::Ok,
            total_weight: 0,
            chosen_edges: Vec::new(),
        };
    }

    let mut adjacency = vec![Vec::<Edge>::new(); node_count];
    for edge in edges {
        let normalized = normalize(*edge);
        adjacency[normalized.source].push(Edge {
            source: normalized.source,
            target: normalized.target,
            weight: normalized.weight,
        });
        adjacency[normalized.target].push(Edge {
            source: normalized.target,
            target: normalized.source,
            weight: normalized.weight,
        });
    }

    let mut visited = vec![false; node_count];
    let mut heap = BinaryHeap::<Reverse<(i64, usize, usize, usize)>>::new();
    let mut chosen_edges = Vec::with_capacity(node_count.saturating_sub(1));
    let mut total_weight = 0_i64;

    let mut push_candidates =
        |node: usize, visited: &[bool], heap: &mut BinaryHeap<Reverse<(i64, usize, usize, usize)>>| {
        for edge in &adjacency[node] {
            if visited[edge.target] {
                continue;
            }
            let normalized = normalize(Edge {
                source: edge.source,
                target: edge.target,
                weight: edge.weight,
            });
            heap.push(Reverse((normalized.weight, normalized.source, normalized.target, edge.target)));
        }
    };

    visited[0] = true;
    let mut visited_count = 1_usize;
    push_candidates(0, &visited, &mut heap);

    while let Some(Reverse((weight, source, target, next_node))) = heap.pop() {
        if visited_count >= node_count {
            break;
        }
        if visited[next_node] {
            continue;
        }

        let Some(updated) = total_weight.checked_add(weight) else {
            return Result {
                status: Status::Overflow,
                total_weight,
                chosen_edges,
            };
        };

        total_weight = updated;
        chosen_edges.push(Edge { source, target, weight });
        visited[next_node] = true;
        visited_count += 1;
        push_candidates(next_node, &visited, &mut heap);
    }

    if visited_count != node_count {
        return Result {
            status: Status::Disconnected,
            total_weight,
            chosen_edges,
        };
    }

    Result {
        status: Status::Ok,
        total_weight,
        chosen_edges,
    }
}
