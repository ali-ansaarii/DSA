#[derive(Clone, Copy)]
pub struct Edge {
    pub source: usize,
    pub target: usize,
    pub weight: i64,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum Status {
    Ok,
    NegativeCycle,
    Overflow,
}

pub struct Result {
    pub status: Status,
    pub distances: Vec<Option<i64>>,
}

pub fn bellman_ford(node_count: usize, edges: &[Edge], start: usize) -> Result {
    let mut distances = vec![None; node_count];
    distances[start] = Some(0_i64);

    for _ in 0..node_count.saturating_sub(1) {
        let mut updated = false;

        for edge in edges {
            let Some(source_distance) = distances[edge.source] else {
                continue;
            };

            let Some(candidate) = source_distance.checked_add(edge.weight) else {
                return Result {
                    status: Status::Overflow,
                    distances,
                };
            };

            match distances[edge.target] {
                Some(target_distance) if candidate >= target_distance => {}
                _ => {
                    distances[edge.target] = Some(candidate);
                    updated = true;
                }
            }
        }

        if !updated {
            break;
        }
    }

    for edge in edges {
        let Some(source_distance) = distances[edge.source] else {
            continue;
        };

        let Some(candidate) = source_distance.checked_add(edge.weight) else {
            return Result {
                status: Status::Overflow,
                distances,
            };
        };

        match distances[edge.target] {
            Some(target_distance) if candidate >= target_distance => {}
            _ => {
                return Result {
                    status: Status::NegativeCycle,
                    distances,
                };
            }
        }
    }

    Result {
        status: Status::Ok,
        distances,
    }
}
