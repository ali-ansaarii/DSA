use std::fs::File;
use std::io::{BufRead, BufReader};
use std::env;
use std::process;

use dfs::DFS;

fn main() {
    let mut input_path = "../inputs/input.txt".to_string();
    let mut time_dfs = false;

    for arg in env::args().skip(1) {
        if arg == "--time-dfs" {
            time_dfs = true;
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
    let lines: Vec<String> = reader.lines()
        .filter_map(Result::ok)
        .map(|line| line.trim().to_string())
        .filter(|line| !line.is_empty())
        .collect();

    if lines.len() < 2 {
        eprintln!("Invalid graph header. Expected: n m");
        process::exit(1);
    }

    let header: Vec<usize> = lines[0]
        .split_whitespace()
        .filter_map(|s| s.parse().ok())
        .collect();

    if header.len() != 2 {
        eprintln!("Invalid graph header. Expected: n m");
        process::exit(1);
    }

    let n = header[0];
    let m = header[1];

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
        let edge_parts: Vec<usize> = lines[i + 1]
            .split_whitespace()
            .filter_map(|s| s.parse().ok())
            .collect();

        if edge_parts.len() != 2 {
            eprintln!("Invalid edge at line {}", i + 2);
            process::exit(1);
        }

        let u = edge_parts[0];
        let v = edge_parts[1];

        if u >= n || v >= n {
            eprintln!("Invalid edge at line {}", i + 2);
            process::exit(1);
        }

        // Undirected graph: add both directions.
        graph[u].push(v);
        graph[v].push(u);
    }

    let start_str = &lines[m + 1];
    let start: usize = match start_str.parse() {
        Ok(s) => s,
        Err(_) => {
            eprintln!("Invalid start node. Expected a node in [0, n).");
            process::exit(1);
        }
    };

    if start >= n {
        eprintln!("Invalid start node. Expected a node in [0, n).");
        process::exit(1);
    }

    // Sort adjacency lists for deterministic traversal.
    for neighbors in &mut graph {
        neighbors.sort_unstable();
    }

    let dfs_start = std::time::Instant::now();
    let traversal_order = DFS(&graph, start);
    let dfs_duration_ms = dfs_start.elapsed().as_secs_f64() * 1000.0;

    if time_dfs {
        println!("DFS visited nodes: {}", traversal_order.len());
        println!("DFS call time (ms): {:.3}", dfs_duration_ms);
    } else {
        print!("DFS traversal order:");
        for node in traversal_order {
            print!(" {}", node);
        }
        println!();
    }
}
