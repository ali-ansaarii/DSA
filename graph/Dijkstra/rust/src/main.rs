use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::process;

use dijkstra::Dijkstra;

const MAX_SIGNED_DISTANCE: u64 = i64::MAX as u64;

fn main() {
    let mut input_path = "inputs/input.txt".to_string();
    let mut time_dijkstra = false;

    for arg in env::args().skip(1) {
        if arg == "--time-dijkstra" {
            time_dijkstra = true;
        } else {
            input_path = arg;
        }
    }

    let file = match File::open(&input_path) {
        Ok(f) => f,
        Err(_) => {
            eprintln!("Failed to open input file: {}", input_path);
            process::exit(1);
        }
    };

    let reader = BufReader::new(file);
    let raw_lines: Vec<String> = match reader.lines().collect() {
        Ok(lines) => lines,
        Err(_) => {
            eprintln!("Failed while reading input file: {}", input_path);
            process::exit(1);
        }
    };
    let lines: Vec<String> = raw_lines
        .into_iter()
        .map(|line| line.trim().to_string())
        .filter(|line| !line.is_empty())
        .collect();

    if lines.len() < 2 {
        eprintln!("Invalid graph header. Expected: n m");
        process::exit(1);
    }

    let header_parts: Vec<&str> = lines[0].split_whitespace().collect();
    if header_parts.len() != 2 {
        eprintln!("Invalid graph header. Expected: n m");
        process::exit(1);
    }

    let n: usize = match header_parts[0].parse() {
        Ok(value) => value,
        Err(_) => {
            eprintln!("Invalid graph header. Expected: n m");
            process::exit(1);
        }
    };
    let m: usize = match header_parts[1].parse() {
        Ok(value) => value,
        Err(_) => {
            eprintln!("Invalid graph header. Expected: n m");
            process::exit(1);
        }
    };

    if n == 0 {
        eprintln!("Invalid graph header. Expected: n m");
        process::exit(1);
    }

    if lines.len() < m + 2 {
        eprintln!("Input ended early. Expected edges and start node.");
        process::exit(1);
    }

    let mut graph = vec![Vec::new(); n];

    for i in 0..m {
        let edge_parts: Vec<&str> = lines[i + 1].split_whitespace().collect();
        if edge_parts.len() != 3 {
            eprintln!("Invalid weighted edge at line {}", i + 2);
            process::exit(1);
        }

        let u: usize = match edge_parts[0].parse() {
            Ok(value) => value,
            Err(_) => {
                eprintln!("Invalid weighted edge at line {}", i + 2);
                process::exit(1);
            }
        };
        let v: usize = match edge_parts[1].parse() {
            Ok(value) => value,
            Err(_) => {
                eprintln!("Invalid weighted edge at line {}", i + 2);
                process::exit(1);
            }
        };
        let w: u64 = match edge_parts[2].parse() {
            Ok(value) => value,
            Err(_) => {
                eprintln!("Invalid weighted edge at line {}", i + 2);
                process::exit(1);
            }
        };

        if u >= n || v >= n || w > MAX_SIGNED_DISTANCE {
            eprintln!("Invalid weighted edge at line {}", i + 2);
            process::exit(1);
        }

        graph[u].push((v, w));
        graph[v].push((u, w));
    }

    let start: usize = match lines[m + 1].parse() {
        Ok(value) => value,
        Err(_) => {
            eprintln!("Invalid start node. Expected a node in [0, n).");
            process::exit(1);
        }
    };

    if start >= n {
        eprintln!("Invalid start node. Expected a node in [0, n).");
        process::exit(1);
    }

    for neighbors in &mut graph {
        neighbors.sort_unstable_by_key(|edge| edge.0);
    }

    let dijkstra_start = std::time::Instant::now();
    let result = match Dijkstra(&graph, start) {
        Ok(value) => value,
        Err(message) => {
            eprintln!("{}", message);
            process::exit(1);
        }
    };
    let dijkstra_duration_ms = dijkstra_start.elapsed().as_secs_f64() * 1000.0;
    let reachable_nodes = result.reachable.iter().filter(|&&is_reachable| is_reachable).count();

    if time_dijkstra {
        println!("Reachable nodes: {}", reachable_nodes);
        println!("Dijkstra call time (ms): {:.3}", dijkstra_duration_ms);
    } else {
        print!("Shortest distances from {}:", start);
        for (distance, is_reachable) in result.distances.iter().zip(result.reachable.iter()) {
            if !is_reachable {
                print!(" INF");
            } else {
                print!(" {}", distance);
            }
        }
        println!();
    }
}
