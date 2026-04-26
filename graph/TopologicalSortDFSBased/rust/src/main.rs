mod topological_sort_dfs_based;

use std::env;
use std::fs;
use std::process;
use std::time::Instant;

use topological_sort_dfs_based::topological_sort_dfs_based;

fn parse_input(input_path: &str) -> Result<(usize, Vec<(usize, usize)>), String> {
    let contents = fs::read_to_string(input_path)
        .map_err(|error| format!("Failed to read input file: {error}"))?;
    let tokens: Vec<&str> = contents.split_whitespace().collect();
    if tokens.len() < 2 {
        return Err(String::from("input must start with: n m"));
    }

    let vertex_count = tokens[0]
        .parse::<usize>()
        .map_err(|_| String::from("invalid vertex count"))?;
    let edge_count = tokens[1]
        .parse::<usize>()
        .map_err(|_| String::from("invalid edge count"))?;

    let expected_tokens = 2 + 2 * edge_count;
    if tokens.len() != expected_tokens {
        return Err(format!(
            "expected {edge_count} edges, found {}",
            (tokens.len().saturating_sub(2)) / 2
        ));
    }

    let mut edges = Vec::with_capacity(edge_count);
    for index in 0..edge_count {
        let base = 2 + 2 * index;
        let from = tokens[base]
            .parse::<usize>()
            .map_err(|_| format!("invalid from endpoint at edge {index}"))?;
        let to = tokens[base + 1]
            .parse::<usize>()
            .map_err(|_| format!("invalid to endpoint at edge {index}"))?;
        edges.push((from, to));
    }

    Ok((vertex_count, edges))
}

fn main() {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_flag_time_topological_sort_dfs_based = false;

    for argument in env::args().skip(1) {
        if argument == "--time-topological-sort-dfs-based" {
            time_flag_time_topological_sort_dfs_based = true;
        } else {
            input_path = argument;
        }
    }

    let (vertex_count, edges) = match parse_input(&input_path) {
        Ok(parsed) => parsed,
        Err(error) => {
            eprintln!("{error}");
            process::exit(1);
        }
    };

    let start = Instant::now();
    let result = match topological_sort_dfs_based(vertex_count, &edges) {
        Ok(result) => result,
        Err(error) => {
            eprintln!("{error}");
            process::exit(1);
        }
    };
    let elapsed = start.elapsed();

    if time_flag_time_topological_sort_dfs_based {
        eprintln!("algorithm_time_ns {}", elapsed.as_nanos());
    }

    if result.has_cycle {
        println!("CYCLE DETECTED");
        return;
    }

    println!("Topological order:");
    let line = result
        .order
        .iter()
        .map(|vertex| vertex.to_string())
        .collect::<Vec<_>>()
        .join(" ");
    println!("{line}");
}
