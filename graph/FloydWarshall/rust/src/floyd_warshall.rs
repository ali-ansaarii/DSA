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
    pub distances: Vec<Vec<Option<i64>>>,
}

pub fn floyd_warshall(node_count: usize, edges: &[Edge]) -> Result {
    let mut distances = vec![vec![None; node_count]; node_count];

    for (node, row) in distances.iter_mut().enumerate().take(node_count) {
        row[node] = Some(0_i64);
    }

    for edge in edges {
        match distances[edge.source][edge.target] {
            Some(current) if current <= edge.weight => {}
            _ => distances[edge.source][edge.target] = Some(edge.weight),
        }
    }

    for intermediate in 0..node_count {
        for source in 0..node_count {
            let Some(left) = distances[source][intermediate] else {
                continue;
            };

            for target in 0..node_count {
                let Some(right) = distances[intermediate][target] else {
                    continue;
                };

                let Some(candidate) = left.checked_add(right) else {
                    return Result {
                        status: Status::Overflow,
                        distances,
                    };
                };

                match distances[source][target] {
                    Some(current) if current <= candidate => {}
                    _ => distances[source][target] = Some(candidate),
                }
            }
        }
    }

    for (node, row) in distances.iter().enumerate().take(node_count) {
        if let Some(diagonal) = row[node] {
            if diagonal < 0 {
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
