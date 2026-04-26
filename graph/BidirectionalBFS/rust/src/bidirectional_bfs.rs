use std::collections::VecDeque;

pub struct BidirectionalBFSResult {
    pub distance: isize,
    pub path: Vec<usize>,
}

pub fn shortest_path_bidirectional_bfs(
    graph: &[Vec<usize>],
    source: usize,
    target: usize,
) -> BidirectionalBFSResult {
    if source == target {
        return BidirectionalBFSResult {
            distance: 0,
            path: vec![source],
        };
    }

    let n = graph.len();
    let mut parent_from_source = vec![None; n];
    let mut parent_from_target = vec![None; n];
    let mut source_frontier = VecDeque::new();
    let mut target_frontier = VecDeque::new();

    parent_from_source[source] = Some(source);
    parent_from_target[target] = Some(target);
    source_frontier.push_back(source);
    target_frontier.push_back(target);

    while !source_frontier.is_empty() && !target_frontier.is_empty() {
        let meeting = if source_frontier.len() <= target_frontier.len() {
            expand_one_level(
                &mut source_frontier,
                &mut parent_from_source,
                &parent_from_target,
                graph,
            )
        } else {
            expand_one_level(
                &mut target_frontier,
                &mut parent_from_target,
                &parent_from_source,
                graph,
            )
        };

        if let Some(meeting_vertex) = meeting {
            let path = build_path(meeting_vertex, &parent_from_source, &parent_from_target);
            return BidirectionalBFSResult {
                distance: path.len() as isize - 1,
                path,
            };
        }
    }

    BidirectionalBFSResult {
        distance: -1,
        path: Vec::new(),
    }
}

fn expand_one_level(
    frontier: &mut VecDeque<usize>,
    parent_this_side: &mut [Option<usize>],
    parent_other_side: &[Option<usize>],
    graph: &[Vec<usize>],
) -> Option<usize> {
    let level_size = frontier.len();
    for _ in 0..level_size {
        let current = frontier.pop_front().expect("frontier size was measured");
        for &neighbor in &graph[current] {
            if parent_this_side[neighbor].is_some() {
                continue;
            }

            parent_this_side[neighbor] = Some(current);
            if parent_other_side[neighbor].is_some() {
                return Some(neighbor);
            }
            frontier.push_back(neighbor);
        }
    }
    None
}

fn build_path(
    meeting: usize,
    parent_from_source: &[Option<usize>],
    parent_from_target: &[Option<usize>],
) -> Vec<usize> {
    let mut left = Vec::new();
    let mut vertex = Some(meeting);
    while let Some(current) = vertex {
        left.push(current);
        vertex = parent_from_source[current];
        if vertex == Some(current) {
            vertex = None;
        }
    }
    left.reverse();

    let mut path = left;
    vertex = parent_from_target[meeting];
    while let Some(current) = vertex {
        if current == meeting {
            break;
        }
        path.push(current);
        vertex = parent_from_target[current];
        if vertex == Some(current) {
            vertex = None;
        }
    }
    path
}
