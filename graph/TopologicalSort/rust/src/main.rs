use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::process;

use topological_sort::TopologicalSort;

fn main() {
    let mut input_path = "inputs/input.txt".to_string();
    let mut time_topological_sort = false;

    for arg in env::args().skip(1) {
        if arg == "--time-toposort" {
            time_topological_sort = true;
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

    if lines.is_empty() {
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

    if lines.len() < m + 1 {
        eprintln!("Input ended early. Expected directed edges.");
        process::exit(1);
    }

    let mut graph = vec![Vec::new(); n];

    for i in 0..m {
        let edge_parts: Vec<&str> = lines[i + 1].split_whitespace().collect();
        if edge_parts.len() != 2 {
            eprintln!("Invalid directed edge at line {}", i + 2);
            process::exit(1);
        }

        let u: usize = match edge_parts[0].parse() {
            Ok(value) => value,
            Err(_) => {
                eprintln!("Invalid directed edge at line {}", i + 2);
                process::exit(1);
            }
        };
        let v: usize = match edge_parts[1].parse() {
            Ok(value) => value,
            Err(_) => {
                eprintln!("Invalid directed edge at line {}", i + 2);
                process::exit(1);
            }
        };

        if u >= n || v >= n {
            eprintln!("Invalid directed edge at line {}", i + 2);
            process::exit(1);
        }

        graph[u].push(v);
    }

    for neighbors in &mut graph {
        neighbors.sort_unstable();
    }

    let topological_sort_start = std::time::Instant::now();
    let order = TopologicalSort(&graph);
    let topological_sort_duration_ms = topological_sort_start.elapsed().as_secs_f64() * 1000.0;

    if time_topological_sort {
        println!("Processed nodes: {}", order.len());
        println!(
            "TopologicalSort call time (ms): {:.3}",
            topological_sort_duration_ms
        );
    }

    if order.len() != graph.len() {
        eprintln!("Cycle detected. Topological sort requires a DAG.");
        process::exit(1);
    }

    if !time_topological_sort {
        print!("Topological order:");
        for node in order {
            print!(" {}", node);
        }
        println!();
    }
}
