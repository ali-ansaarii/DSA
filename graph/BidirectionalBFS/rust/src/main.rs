mod bidirectional_bfs;

use bidirectional_bfs::shortest_path_bidirectional_bfs;
use std::env;
use std::fs;
use std::process;
use std::time::Instant;

fn main() {
    if let Err(error) = run() {
        eprintln!("{error}");
        process::exit(1);
    }
}

fn run() -> Result<(), String> {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_flag_time_bidirectional_bfs = false;

    for argument in env::args().skip(1) {
        if argument == "--time-bidirectional-bfs" {
            time_flag_time_bidirectional_bfs = true;
        } else {
            input_path = argument;
        }
    }

    let (graph, source, target) = read_input(&input_path)?;

    let result = if time_flag_time_bidirectional_bfs {
        let start = Instant::now();
        let result = shortest_path_bidirectional_bfs(&graph, source, target);
        eprintln!("algorithm_time_ns: {}", start.elapsed().as_nanos());
        result
    } else {
        shortest_path_bidirectional_bfs(&graph, source, target)
    };

    println!("distance: {}", result.distance);
    print!("path:");
    for vertex in result.path {
        print!(" {vertex}");
    }
    println!();

    Ok(())
}

fn read_input(path: &str) -> Result<(Vec<Vec<usize>>, usize, usize), String> {
    let content = fs::read_to_string(path)
        .map_err(|error| format!("failed to read input file '{path}': {error}"))?;
    let values: Vec<usize> = content
        .split_whitespace()
        .map(|token| {
            token
                .parse::<usize>()
                .map_err(|error| format!("invalid integer '{token}': {error}"))
        })
        .collect::<Result<_, _>>()?;

    if values.len() < 2 {
        return Err(String::from("input is missing graph header"));
    }

    let n = values[0];
    let m = values[1];
    let expected_values = 2 + 2 * m + 2;
    if values.len() != expected_values {
        return Err(format!(
            "expected {expected_values} integers, found {}",
            values.len()
        ));
    }

    let mut graph = vec![Vec::new(); n];
    let mut offset = 2;
    for edge_index in 0..m {
        let u = values[offset];
        let v = values[offset + 1];
        offset += 2;
        if u >= n || v >= n {
            return Err(format!("invalid edge at index {edge_index}"));
        }
        graph[u].push(v);
        graph[v].push(u);
    }

    let source = values[offset];
    let target = values[offset + 1];
    if source >= n || target >= n {
        return Err(String::from("invalid source/target query"));
    }

    Ok((graph, source, target))
}
