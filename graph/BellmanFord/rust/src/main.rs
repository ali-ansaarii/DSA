mod bellman_ford;

use bellman_ford::{bellman_ford, Edge, Status};
use std::env;
use std::fs;
use std::time::Instant;

struct ProgramOptions {
    input_path: String,
    benchmark_mode: bool,
}

fn parse_arguments(args: &[String]) -> Result<ProgramOptions, String> {
    let mut input_path: Option<String> = None;
    let mut benchmark_mode = false;

    for argument in args.iter().skip(1) {
        if argument == "--time-bellman-ford" {
            benchmark_mode = true;
        } else if input_path.is_none() {
            input_path = Some(argument.clone());
        } else {
            return Err("Usage: bellman_ford <input-file> [--time-bellman-ford]".to_string());
        }
    }

    let Some(input_path) = input_path else {
        return Err("Usage: bellman_ford <input-file> [--time-bellman-ford]".to_string());
    };

    Ok(ProgramOptions {
        input_path,
        benchmark_mode,
    })
}

fn read_input(path: &str) -> Result<(usize, Vec<Edge>, usize), String> {
    let contents = fs::read_to_string(path).map_err(|error| format!("Failed to open input file: {error}"))?;
    let mut tokens = contents.split_whitespace();

    let node_count: usize = tokens
        .next()
        .ok_or_else(|| "Invalid graph input".to_string())?
        .parse()
        .map_err(|_| "Invalid node count".to_string())?;
    let edge_count: usize = tokens
        .next()
        .ok_or_else(|| "Invalid graph input".to_string())?
        .parse()
        .map_err(|_| "Invalid edge count".to_string())?;

    if node_count == 0 {
        return Err("Invalid graph header".to_string());
    }

    let mut edges = Vec::with_capacity(edge_count);
    for index in 0..edge_count {
        let source: usize = tokens
            .next()
            .ok_or_else(|| format!("Invalid edge at index {index}"))?
            .parse()
            .map_err(|_| format!("Invalid edge source at index {index}"))?;
        let target: usize = tokens
            .next()
            .ok_or_else(|| format!("Invalid edge at index {index}"))?
            .parse()
            .map_err(|_| format!("Invalid edge target at index {index}"))?;
        let weight: i64 = tokens
            .next()
            .ok_or_else(|| format!("Invalid edge at index {index}"))?
            .parse()
            .map_err(|_| format!("Invalid edge weight at index {index}"))?;

        if source >= node_count || target >= node_count {
            return Err(format!("Edge node out of range at index {index}"));
        }

        edges.push(Edge {
            source,
            target,
            weight,
        });
    }

    let start: usize = tokens
        .next()
        .ok_or_else(|| "Missing start node".to_string())?
        .parse()
        .map_err(|_| "Invalid start node".to_string())?;

    if start >= node_count {
        return Err("Invalid start node".to_string());
    }

    Ok((node_count, edges, start))
}

fn print_distances(distances: &[Option<i64>], start: usize) {
    print!("Shortest distances from {start}:");
    for distance in distances {
        match distance {
            Some(value) => print!(" {value}"),
            None => print!(" INF"),
        }
    }
    println!();
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let options = match parse_arguments(&args) {
        Ok(options) => options,
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(1);
        }
    };

    let (node_count, edges, start) = match read_input(&options.input_path) {
        Ok(parsed) => parsed,
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(1);
        }
    };

    let begin = Instant::now();
    let result = bellman_ford(node_count, &edges, start);
    let elapsed_ms = begin.elapsed().as_secs_f64() * 1000.0;

    if options.benchmark_mode {
        println!("Bellman-Ford time: {:.3} ms", elapsed_ms);
    }

    match result.status {
        Status::Overflow => {
            eprintln!("Overflow detected while relaxing edges");
            std::process::exit(1);
        }
        Status::NegativeCycle => {
            println!("Negative cycle reachable from {start}");
        }
        Status::Ok => {
            if !options.benchmark_mode {
                print_distances(&result.distances, start);
            }
        }
    }
}
