use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::process;

use disjoint_set_union::{DisjointSetUnion, Operation, OperationType};

fn is_valid_element(element: usize, n: usize) -> bool {
    element < n
}

fn main() {
    let mut input_path = "inputs/input.txt".to_string();
    let mut time_dsu = false;

    for arg in env::args().skip(1) {
        if arg == "--time-dsu" {
            time_dsu = true;
        } else {
            input_path = arg;
        }
    }

    let file = match File::open(&input_path) {
        Ok(file) => file,
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
        eprintln!("Invalid DSU header. Expected: n q");
        process::exit(1);
    }

    let header_parts: Vec<&str> = lines[0].split_whitespace().collect();
    if header_parts.len() != 2 {
        eprintln!("Invalid DSU header. Expected: n q");
        process::exit(1);
    }

    let n: usize = match header_parts[0].parse() {
        Ok(value) => value,
        Err(_) => {
            eprintln!("Invalid DSU header. Expected: n q");
            process::exit(1);
        }
    };
    let q: usize = match header_parts[1].parse() {
        Ok(value) => value,
        Err(_) => {
            eprintln!("Invalid DSU header. Expected: n q");
            process::exit(1);
        }
    };

    if n == 0 {
        eprintln!("Invalid DSU header. Expected: n q");
        process::exit(1);
    }

    if lines.len() < q + 1 {
        eprintln!("Input ended early. Expected {} operations.", q);
        process::exit(1);
    }

    let mut operations = Vec::with_capacity(q);
    for line_index in 1..=q {
        let parts: Vec<&str> = lines[line_index].split_whitespace().collect();
        if parts.is_empty() {
            eprintln!("Invalid operation at line {}", line_index + 1);
            process::exit(1);
        }

        match parts[0] {
            "union" | "connected" => {
                if parts.len() != 3 {
                    eprintln!("Invalid operation at line {}", line_index + 1);
                    process::exit(1);
                }

                let first: usize = match parts[1].parse() {
                    Ok(value) => value,
                    Err(_) => {
                        eprintln!("Invalid operation at line {}", line_index + 1);
                        process::exit(1);
                    }
                };
                let second: usize = match parts[2].parse() {
                    Ok(value) => value,
                    Err(_) => {
                        eprintln!("Invalid operation at line {}", line_index + 1);
                        process::exit(1);
                    }
                };

                if !is_valid_element(first, n) || !is_valid_element(second, n) {
                    eprintln!("Invalid operation at line {}", line_index + 1);
                    process::exit(1);
                }

                operations.push(Operation {
                    kind: if parts[0] == "union" {
                        OperationType::Union
                    } else {
                        OperationType::Connected
                    },
                    first,
                    second,
                });
            }
            "find" => {
                if parts.len() != 2 {
                    eprintln!("Invalid operation at line {}", line_index + 1);
                    process::exit(1);
                }

                let first: usize = match parts[1].parse() {
                    Ok(value) => value,
                    Err(_) => {
                        eprintln!("Invalid operation at line {}", line_index + 1);
                        process::exit(1);
                    }
                };

                if !is_valid_element(first, n) {
                    eprintln!("Invalid operation at line {}", line_index + 1);
                    process::exit(1);
                }

                operations.push(Operation {
                    kind: OperationType::Find,
                    first,
                    second: 0,
                });
            }
            _ => {
                eprintln!("Invalid operation at line {}", line_index + 1);
                process::exit(1);
            }
        }
    }

    let dsu_start = std::time::Instant::now();
    let query_results = DisjointSetUnion(n, &operations);
    let dsu_duration_ms = dsu_start.elapsed().as_secs_f64() * 1000.0;

    if time_dsu {
        println!("Processed operations: {}", operations.len());
        println!("DisjointSetUnion call time (ms): {:.3}", dsu_duration_ms);
    } else {
        println!("Query results:");
        for result in query_results {
            println!("{}", result);
        }
    }
}
