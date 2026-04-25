mod a_star_search;

use a_star_search::shortest_path_length_a_star;
use std::env;
use std::error::Error;
use std::fs;
use std::time::Instant;

struct ParsedInput {
    grid: Vec<String>,
    start: (isize, isize),
    goal: (isize, isize),
}

fn parse_input(input_path: &str) -> Result<ParsedInput, Box<dyn Error>> {
    let content = fs::read_to_string(input_path)?;
    let tokens: Vec<&str> = content.split_whitespace().collect();
    if tokens.len() < 6 {
        return Err("input must contain rows, cols, start, and goal coordinates".into());
    }

    let rows: usize = tokens[0].parse()?;
    let cols: usize = tokens[1].parse()?;
    let start_row: isize = tokens[2].parse()?;
    let start_col: isize = tokens[3].parse()?;
    let goal_row: isize = tokens[4].parse()?;
    let goal_col: isize = tokens[5].parse()?;

    if rows == 0 || cols == 0 {
        return Err("rows and cols must be positive".into());
    }
    if tokens.len() < 6 + rows {
        return Err("missing grid rows".into());
    }

    let mut grid = Vec::with_capacity(rows);
    for row in 0..rows {
        let line = tokens[6 + row].to_string();
        if line.len() != cols {
            return Err(format!("grid row {row} has the wrong length").into());
        }
        if !line.bytes().all(|cell| cell == b'.' || cell == b'#') {
            return Err("grid may contain only '.' and '#'".into());
        }
        grid.push(line);
    }

    Ok(ParsedInput {
        grid,
        start: (start_row, start_col),
        goal: (goal_row, goal_col),
    })
}

fn nonnegative_coordinate_pair(coordinates: (isize, isize)) -> Option<(usize, usize)> {
    let (row, col) = coordinates;
    if row < 0 || col < 0 {
        None
    } else {
        Some((row as usize, col as usize))
    }
}

fn run() -> Result<(), Box<dyn Error>> {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_flag_time_a_star_search = false;

    for argument in env::args().skip(1) {
        if argument == "--time-a-star-search" {
            time_flag_time_a_star_search = true;
        } else {
            input_path = argument;
        }
    }

    let parsed = parse_input(&input_path)?;
    let start = nonnegative_coordinate_pair(parsed.start);
    let goal = nonnegative_coordinate_pair(parsed.goal);

    let distance = match (start, goal) {
        (Some(start), Some(goal)) => {
            if time_flag_time_a_star_search {
                let started_at = Instant::now();
                let result = shortest_path_length_a_star(&parsed.grid, start, goal);
                eprintln!(
                    "Algorithm time (microseconds): {}",
                    started_at.elapsed().as_micros()
                );
                result
            } else {
                shortest_path_length_a_star(&parsed.grid, start, goal)
            }
        }
        _ => None,
    };

    match distance {
        Some(value) => println!("Shortest path length: {value}"),
        None => println!("UNREACHABLE"),
    }

    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("Error: {error}");
        std::process::exit(1);
    }
}
