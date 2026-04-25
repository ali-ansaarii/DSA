use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn manhattan(row: usize, col: usize, goal_row: usize, goal_col: usize) -> usize {
    row.abs_diff(goal_row) + col.abs_diff(goal_col)
}

fn is_open(grid: &[String], row: usize, col: usize) -> bool {
    row < grid.len() && col < grid[row].len() && grid[row].as_bytes()[col] != b'#'
}

pub fn shortest_path_length_a_star(
    grid: &[String],
    start: (usize, usize),
    goal: (usize, usize),
) -> Option<usize> {
    if grid.is_empty() || grid[0].is_empty() {
        return None;
    }

    let rows = grid.len();
    let cols = grid[0].len();
    let (start_row, start_col) = start;
    let (goal_row, goal_col) = goal;

    if start_row >= rows
        || start_col >= cols
        || goal_row >= rows
        || goal_col >= cols
        || !is_open(grid, start_row, start_col)
        || !is_open(grid, goal_row, goal_col)
    {
        return None;
    }

    let mut distance = vec![vec![usize::MAX; cols]; rows];
    let mut open: BinaryHeap<Reverse<(usize, usize, usize, usize, usize)>> = BinaryHeap::new();

    let start_h = manhattan(start_row, start_col, goal_row, goal_col);
    distance[start_row][start_col] = 0;
    // (f_score, h_score, g_score, row, col). Lower h_score breaks f_score ties
    // toward the goal without affecting optimality.
    open.push(Reverse((start_h, start_h, 0, start_row, start_col)));

    let directions: [(isize, isize); 4] = [(1, 0), (-1, 0), (0, 1), (0, -1)];

    while let Some(Reverse((_, _, current_distance, row, col))) = open.pop() {
        if current_distance != distance[row][col] {
            continue;
        }

        if row == goal_row && col == goal_col {
            return Some(current_distance);
        }

        for (d_row, d_col) in directions {
            let Some(next_row) = row.checked_add_signed(d_row) else {
                continue;
            };
            let Some(next_col) = col.checked_add_signed(d_col) else {
                continue;
            };

            if !is_open(grid, next_row, next_col) {
                continue;
            }

            let next_distance = current_distance + 1;
            if next_distance < distance[next_row][next_col] {
                distance[next_row][next_col] = next_distance;
                let heuristic = manhattan(next_row, next_col, goal_row, goal_col);
                open.push(Reverse((
                    next_distance + heuristic,
                    heuristic,
                    next_distance,
                    next_row,
                    next_col,
                )));
            }
        }
    }

    None
}
