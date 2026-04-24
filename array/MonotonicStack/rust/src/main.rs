mod monotonic_stack;

use monotonic_stack::next_greater_elements;
use std::env;
use std::fs;
use std::time::Instant;

fn read_input(input_path: &str) -> Result<Vec<i64>, String> {
    let content = fs::read_to_string(input_path)
        .map_err(|_| format!("Failed to open input file: {input_path}"))?;
    let tokens: Vec<&str> = content.split_whitespace().collect();
    if tokens.is_empty() {
        return Err("Invalid input header.".to_string());
    }

    let n = tokens[0]
        .parse::<usize>()
        .map_err(|_| "Invalid input header.".to_string())?;
    if n == 0 {
        return Err("Invalid input header.".to_string());
    }
    if tokens.len() != 1 + n {
        return Err("Input size does not match header.".to_string());
    }

    let mut values = Vec::with_capacity(n);
    for token in &tokens[1..] {
        values.push(
            token
                .parse::<i64>()
                .map_err(|_| "Invalid array value.".to_string())?,
        );
    }

    Ok(values)
}

fn main() {
    let mut input_path = "inputs/input.txt".to_string();
    let mut time_monotonic_stack = false;

    for argument in env::args().skip(1) {
        if argument == "--time-monotonic-stack" {
            time_monotonic_stack = true;
        } else {
            input_path = argument;
        }
    }

    let values = match read_input(&input_path) {
        Ok(parsed) => parsed,
        Err(message) => {
            eprintln!("{message}");
            std::process::exit(1);
        }
    };

    let start = Instant::now();
    let answer = next_greater_elements(&values);
    let elapsed_ms = start.elapsed().as_secs_f64() * 1000.0;

    if time_monotonic_stack {
        println!("Monotonic-stack time: {:.3} ms", elapsed_ms);
    } else {
        print!("Next greater elements:");
        for value in answer {
            print!(" {}", value);
        }
        println!();
    }
}
