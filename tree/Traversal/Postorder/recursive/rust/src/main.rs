use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::process;

use postorder_recursive::PostorderTraversal;

fn is_valid_child(child: i32, n: usize) -> bool {
    child == -1 || (child >= 0 && (child as usize) < n)
}

fn main() {
    let mut input_path = "../inputs/input.txt".to_string();
    let mut time_postorder = false;

    for arg in env::args().skip(1) {
        if arg == "--time-postorder" {
            time_postorder = true;
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
        eprintln!("Invalid tree header. Expected: n root");
        process::exit(1);
    }

    let header_parts: Vec<&str> = lines[0].split_whitespace().collect();
    if header_parts.len() != 2 {
        eprintln!("Invalid tree header. Expected: n root");
        process::exit(1);
    }

    let n: usize = match header_parts[0].parse() {
        Ok(value) => value,
        Err(_) => {
            eprintln!("Invalid tree header. Expected: n root");
            process::exit(1);
        }
    };
    let root: usize = match header_parts[1].parse() {
        Ok(value) => value,
        Err(_) => {
            eprintln!("Invalid tree header. Expected: n root");
            process::exit(1);
        }
    };

    if n == 0 || root >= n {
        eprintln!("Invalid tree header. Expected: n root");
        process::exit(1);
    }

    if lines.len() < n + 1 {
        eprintln!("Input ended early. Expected child pairs for all nodes.");
        process::exit(1);
    }

    let mut left_children = vec![-1; n];
    let mut right_children = vec![-1; n];

    for node in 0..n {
        let child_parts: Vec<&str> = lines[node + 1].split_whitespace().collect();
        if child_parts.len() != 2 {
            eprintln!("Invalid child pair at line {}", node + 2);
            process::exit(1);
        }

        let left: i32 = match child_parts[0].parse() {
            Ok(value) => value,
            Err(_) => {
                eprintln!("Invalid child pair at line {}", node + 2);
                process::exit(1);
            }
        };
        let right: i32 = match child_parts[1].parse() {
            Ok(value) => value,
            Err(_) => {
                eprintln!("Invalid child pair at line {}", node + 2);
                process::exit(1);
            }
        };

        if !is_valid_child(left, n) || !is_valid_child(right, n) {
            eprintln!("Invalid child pair at line {}", node + 2);
            process::exit(1);
        }

        left_children[node] = left;
        right_children[node] = right;
    }

    let traversal_start = std::time::Instant::now();
    let order = PostorderTraversal(&left_children, &right_children, root);
    let traversal_duration_ms = traversal_start.elapsed().as_secs_f64() * 1000.0;

    if time_postorder {
        println!("Visited nodes: {}", order.len());
        println!("PostorderTraversal call time (ms): {:.3}", traversal_duration_ms);
    } else {
        print!("Postorder traversal order:");
        for node in order {
            print!(" {}", node);
        }
        println!();
    }
}
