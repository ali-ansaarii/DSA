mod floyd_warshall;

use floyd_warshall::{floyd_warshall, Edge, Status};
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
        if argument == "--time-floyd-warshall" {
            benchmark_mode = true;
        } else if input_path.is_none() {
            input_path = Some(argument.clone());
        } else {
            return Err("Usage: floyd_warshall <input-file> [--time-floyd-warshall]".to_string());
        }
    }

    let Some(input_path) = input_path else {
        return Err("Usage: floyd_warshall <input-file> [--time-floyd-warshall]".to_string());
    };

    Ok(ProgramOptions {
        input_path,
        benchmark_mode,
    })
}

fn read_input(path: &str) -> Result<(usize, Vec<Edge>), String> {
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

    Ok((node_count, edges))
}

fn print_matrix(distances: &[Vec<Option<i64>>]) {
    println!("All-pairs shortest distances:");
    for row in distances {
        let rendered = row
            .iter()
            .map(|value| match value {
                Some(distance) => distance.to_string(),
                None => "INF".to_string(),
            })
            .collect::<Vec<String>>()
            .join(" ");
        println!("{rendered}");
    }
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

    let (node_count, edges) = match read_input(&options.input_path) {
        Ok(parsed) => parsed,
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(1);
        }
    };

    let begin = Instant::now();
    let result = floyd_warshall(node_count, &edges);
    let elapsed_ms = begin.elapsed().as_secs_f64() * 1000.0;

    if options.benchmark_mode {
        println!("Floyd-Warshall time: {:.3} ms", elapsed_ms);
    }

    match result.status {
        Status::Overflow => {
            eprintln!("Overflow detected while updating the distance matrix");
            std::process::exit(1);
        }
        Status::NegativeCycle => {
            println!("Negative cycle detected");
        }
        Status::Ok => {
            if !options.benchmark_mode {
                print_matrix(&result.distances);
            }
        }
    }
}
