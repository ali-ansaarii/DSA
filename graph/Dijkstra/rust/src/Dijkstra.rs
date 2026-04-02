use std::cmp::Reverse;
use std::collections::BinaryHeap;

pub const INF: u64 = u64::MAX / 4;

#[allow(non_snake_case)]
pub fn Dijkstra(graph: &[Vec<(usize, u64)>], start: usize) -> Vec<u64> {
    let mut distances = vec![INF; graph.len()];
    let mut min_heap = BinaryHeap::new();

    distances[start] = 0;
    min_heap.push((Reverse(0_u64), start));

    while let Some((Reverse(distance), node)) = min_heap.pop() {
        if distance != distances[node] {
            continue;
        }

        for &(neighbor, weight) in &graph[node] {
            let candidate = distance + weight;
            if candidate < distances[neighbor] {
                distances[neighbor] = candidate;
                min_heap.push((Reverse(candidate), neighbor));
            }
        }
    }

    distances
}
