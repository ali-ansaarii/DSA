mod a_star_search;

use a_star_search::shortest_path_length_a_star;
use std::env;
use std::error::Error;
use std::fs;
use std::time::Instant;

struct ParsedInput {
    grid: Vec<String>,
    start: (usize, usize),
    goal: (usize, usize),
}

fn parse_input(input_path: &str) -> Result<ParsedInput, Box<dyn Error>> {
    let content = fs::read_to_string(input_path)?;
    let tokens: Vec<&str> = content.split_whitespace().collect();
    if tokens.len() < 6 {
        return Err("input must contain rows, cols, start, and goal coordinates".into());
    }

    let rows: usize = tokens[0].parse()?;
    let cols: usize = tokens[1].parse()?;
    let start_row: usize = tokens[2].parse()?;
    let start_col: usize = tokens[3].parse()?;
    let goal_row: usize = tokens[4].parse()?;
    let goal_col: usize = tokens[5].parse()?;

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

    let distance = if time_flag_time_a_star_search {
        let started_at = Instant::now();
        let result = shortest_path_length_a_star(&parsed.grid, parsed.start, parsed.goal);
        eprintln!(
            "Algorithm time (microseconds): {}",
            started_at.elapsed().as_micros()
        );
        result
    } else {
        shortest_path_length_a_star(&parsed.grid, parsed.start, parsed.goal)
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
