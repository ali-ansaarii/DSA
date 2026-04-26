mod shortest_path_in_dag;

use shortest_path_in_dag::{shortest_path_in_dag, Edge, INF};
use std::env;
use std::fs;
use std::time::Instant;

fn parse_input(input_path: &str) -> Result<(usize, Vec<Edge>, usize), String> {
    let contents = fs::read_to_string(input_path)
        .map_err(|error| format!("failed to read input file: {error}"))?;
    let mut tokens = contents.split_whitespace();

    let vertex_count = tokens
        .next()
        .ok_or_else(|| String::from("invalid input header"))?
        .parse::<usize>()
        .map_err(|error| format!("invalid vertex count: {error}"))?;
    let edge_count = tokens
        .next()
        .ok_or_else(|| String::from("invalid input header"))?
        .parse::<usize>()
        .map_err(|error| format!("invalid edge count: {error}"))?;
    let source = tokens
        .next()
        .ok_or_else(|| String::from("invalid input header"))?
        .parse::<usize>()
        .map_err(|error| format!("invalid source vertex: {error}"))?;

    let mut edges = Vec::with_capacity(edge_count);
    for index in 0..edge_count {
        let from = tokens
            .next()
            .ok_or_else(|| format!("invalid edge line at index {index}"))?
            .parse::<usize>()
            .map_err(|error| format!("invalid edge source at index {index}: {error}"))?;
        let to = tokens
            .next()
            .ok_or_else(|| format!("invalid edge line at index {index}"))?
            .parse::<usize>()
            .map_err(|error| format!("invalid edge target at index {index}: {error}"))?;
        let weight = tokens
            .next()
            .ok_or_else(|| format!("invalid edge line at index {index}"))?
            .parse::<i64>()
            .map_err(|error| format!("invalid edge weight at index {index}: {error}"))?;
        edges.push(Edge { from, to, weight });
    }

    Ok((vertex_count, edges, source))
}

fn format_distances(distances: &[i64]) -> String {
    distances
        .iter()
        .map(|distance| {
            if *distance == INF {
                String::from("INF")
            } else {
                distance.to_string()
            }
        })
        .collect::<Vec<_>>()
        .join(" ")
}

fn main() {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_flag_time_shortest_path_in_dag = false;

    for argument in env::args().skip(1) {
        if argument == "--time-shortest-path-in-dag" {
            time_flag_time_shortest_path_in_dag = true;
        } else {
            input_path = argument;
        }
    }

    let result = (|| -> Result<(), String> {
        let (vertex_count, edges, source) = parse_input(&input_path)?;
        let distances = if time_flag_time_shortest_path_in_dag {
            let start = Instant::now();
            let distances = shortest_path_in_dag(vertex_count, &edges, source)?;
            eprintln!("algorithm_ms {:.6}", start.elapsed().as_secs_f64() * 1000.0);
            distances
        } else {
            shortest_path_in_dag(vertex_count, &edges, source)?
        };
        println!("{}", format_distances(&distances));
        Ok(())
    })();

    if let Err(error) = result {
        eprintln!("{error}");
        std::process::exit(1);
    }
}
