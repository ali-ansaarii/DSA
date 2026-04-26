#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TopologicalSortResult {
    pub has_cycle: bool,
    pub order: Vec<usize>,
}

pub fn topological_sort_dfs_based(
    vertex_count: usize,
    edges: &[(usize, usize)],
) -> Result<TopologicalSortResult, String> {
    let mut graph = vec![Vec::new(); vertex_count];
    for &(from, to) in edges {
        if from >= vertex_count || to >= vertex_count {
            return Err(String::from("edge endpoint is outside the vertex range"));
        }
        graph[from].push(to);
    }

    let mut color = vec![0_u8; vertex_count]; // 0 = unvisited, 1 = visiting, 2 = done
    let mut postorder = Vec::with_capacity(vertex_count);

    for start in 0..vertex_count {
        if color[start] != 0 {
            continue;
        }

        color[start] = 1;
        let mut stack = vec![(start, 0_usize)];

        while let Some((vertex, next_index)) = stack.last_mut() {
            if *next_index < graph[*vertex].len() {
                let neighbor = graph[*vertex][*next_index];
                *next_index += 1;

                if color[neighbor] == 0 {
                    color[neighbor] = 1;
                    stack.push((neighbor, 0));
                } else if color[neighbor] == 1 {
                    return Ok(TopologicalSortResult {
                        has_cycle: true,
                        order: Vec::new(),
                    });
                }
            } else {
                color[*vertex] = 2;
                postorder.push(*vertex);
                stack.pop();
            }
        }
    }

    postorder.reverse();
    Ok(TopologicalSortResult {
        has_cycle: false,
        order: postorder,
    })
}
