use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::collections::VecDeque;

pub const MAX_DISTANCE: u64 = i64::MAX as u64;

pub struct DijkstraResult {
    pub distances: Vec<u64>,
    pub reachable: Vec<bool>,
}

#[allow(non_snake_case)]
pub fn Dijkstra(graph: &[Vec<(usize, u64)>], start: usize) -> Result<DijkstraResult, &'static str> {
    let mut graph_reachable = vec![false; graph.len()];
    let mut traversal_queue = VecDeque::from([start]);
    graph_reachable[start] = true;

    while let Some(node) = traversal_queue.pop_front() {
        for &(neighbor, _weight) in &graph[node] {
            if !graph_reachable[neighbor] {
                graph_reachable[neighbor] = true;
                traversal_queue.push_back(neighbor);
            }
        }
    }

    let mut distances = vec![0; graph.len()];
    let mut reachable = vec![false; graph.len()];
    let mut min_heap = BinaryHeap::new();

    reachable[start] = true;
    distances[start] = 0;
    min_heap.push((Reverse(0_u64), start));

    while let Some((Reverse(distance), node)) = min_heap.pop() {
        if !reachable[node] || distance != distances[node] {
            continue;
        }

        for &(neighbor, weight) in &graph[node] {
            let candidate = match distance.checked_add(weight) {
                Some(value) if value <= MAX_DISTANCE => value,
                _ => continue,
            };

            if !reachable[neighbor] || candidate < distances[neighbor] {
                reachable[neighbor] = true;
                distances[neighbor] = candidate;
                min_heap.push((Reverse(candidate), neighbor));
            }
        }
    }

    if graph_reachable
        .iter()
        .zip(reachable.iter())
        .any(|(&is_graph_reachable, &is_reachable)| is_graph_reachable && !is_reachable)
    {
        return Err("Shortest-path overflow: a path distance exceeded the signed 64-bit integer range.");
    }

    Ok(DijkstraResult {
        distances,
        reachable,
    })
}
