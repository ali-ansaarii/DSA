mod fenwick_tree;

use fenwick_tree::{process_fenwick_queries, Query};
use std::env;
use std::fs;
use std::process;
use std::time::Instant;

fn read_input(input_path: &str) -> Result<(Vec<i64>, Vec<Query>), String> {
    let content = fs::read_to_string(input_path)
        .map_err(|_| format!("Failed to open input file: {input_path}"))?;
    let mut tokens = content.split_whitespace();

    let n = tokens
        .next()
        .ok_or_else(|| String::from("Invalid input header."))?
        .parse::<usize>()
        .map_err(|_| String::from("Invalid input header."))?;
    let q = tokens
        .next()
        .ok_or_else(|| String::from("Invalid input header."))?
        .parse::<usize>()
        .map_err(|_| String::from("Invalid input header."))?;

    if n == 0 {
        return Err(String::from("Invalid input header."));
    }

    let mut initial_values = Vec::with_capacity(n);
    for index in 0..n {
        let value = tokens
            .next()
            .ok_or_else(|| format!("Failed to read initial value at index {index}."))?
            .parse::<i64>()
            .map_err(|_| format!("Failed to read initial value at index {index}."))?;
        initial_values.push(value);
    }

    let mut queries = Vec::with_capacity(q);
    for line_index in 0..q {
        let operation_line = n + line_index + 2;
        let operation = tokens
            .next()
            .ok_or_else(|| format!("Input ended early. Expected {q} operations."))?;

        match operation {
            "add" => {
                let index = tokens
                    .next()
                    .ok_or_else(|| format!("Invalid operation at line {}.", operation_line))?
                    .parse::<usize>()
                    .map_err(|_| format!("Invalid operation at line {}.", operation_line))?;
                let delta = tokens
                    .next()
                    .ok_or_else(|| format!("Invalid operation at line {}.", operation_line))?
                    .parse::<i64>()
                    .map_err(|_| format!("Invalid operation at line {}.", operation_line))?;

                if index >= n {
                    return Err(format!("Invalid operation at line {}.", operation_line));
                }

                queries.push(Query::Add { index, delta });
            }
            "sum" => {
                let left = tokens
                    .next()
                    .ok_or_else(|| format!("Invalid operation at line {}.", operation_line))?
                    .parse::<usize>()
                    .map_err(|_| format!("Invalid operation at line {}.", operation_line))?;
                let right = tokens
                    .next()
                    .ok_or_else(|| format!("Invalid operation at line {}.", operation_line))?
                    .parse::<usize>()
                    .map_err(|_| format!("Invalid operation at line {}.", operation_line))?;

                if left > right || right >= n {
                    return Err(format!("Invalid operation at line {}.", operation_line));
                }

                queries.push(Query::Sum { left, right });
            }
            _ => {
                return Err(format!("Invalid operation at line {}.", operation_line));
            }
        }
    }

    if tokens.next().is_some() {
        return Err(String::from("Input size does not match header."));
    }

    Ok((initial_values, queries))
}

fn print_answer(results: &[i64]) {
    println!("Query sums:");
    for value in results {
        println!("{value}");
    }
}

fn main() {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_fenwick_tree = false;

    for argument in env::args().skip(1) {
        if argument == "--time-fenwick-tree" {
            time_fenwick_tree = true;
        } else {
            input_path = argument;
        }
    }

    let (initial_values, queries) = match read_input(&input_path) {
        Ok(data) => data,
        Err(message) => {
            eprintln!("{message}");
            process::exit(1);
        }
    };

    let start = Instant::now();
    let results = match process_fenwick_queries(&initial_values, &queries) {
        Ok(results) => results,
        Err(message) => {
            eprintln!("{message}");
            process::exit(1);
        }
    };
    let elapsed = start.elapsed();

    if time_fenwick_tree {
        println!("Fenwick-tree time: {:.6} ms", elapsed.as_secs_f64() * 1000.0);
    } else {
        print_answer(&results);
    }
}
