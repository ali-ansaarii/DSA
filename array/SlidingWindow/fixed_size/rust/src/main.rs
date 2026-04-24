mod sliding_window;

use sliding_window::best_fixed_window;
use std::env;
use std::fs;
use std::time::Instant;

fn read_input(input_path: &str) -> Result<(Vec<i64>, usize), String> {
    let content = fs::read_to_string(input_path)
        .map_err(|_| format!("Failed to open input file: {input_path}"))?;
    let tokens: Vec<&str> = content.split_whitespace().collect();
    if tokens.len() < 2 {
        return Err("Invalid input header.".to_string());
    }

    let n = tokens[0]
        .parse::<usize>()
        .map_err(|_| "Invalid input header.".to_string())?;
    let k = tokens[1]
        .parse::<usize>()
        .map_err(|_| "Invalid input header.".to_string())?;
    if n == 0 || k == 0 || k > n {
        return Err("Invalid input header.".to_string());
    }
    if tokens.len() != 2 + n {
        return Err("Input size does not match header.".to_string());
    }

    let mut values = Vec::with_capacity(n);
    for token in &tokens[2..] {
        values.push(
            token
                .parse::<i64>()
                .map_err(|_| "Invalid array value.".to_string())?,
        );
    }

    Ok((values, k))
}

fn main() {
    let mut input_path = "inputs/input.txt".to_string();
    let mut time_fixed_window = false;

    for argument in env::args().skip(1) {
        if argument == "--time-fixed-window" {
            time_fixed_window = true;
        } else {
            input_path = argument;
        }
    }

    let (values, k) = match read_input(&input_path) {
        Ok(parsed) => parsed,
        Err(message) => {
            eprintln!("{message}");
            std::process::exit(1);
        }
    };

    let start = Instant::now();
    let result = match best_fixed_window(&values, k) {
        Some(result) => result,
        None => {
            eprintln!("Overflow while evaluating fixed-size windows.");
            std::process::exit(1);
        }
    };
    let elapsed_ms = start.elapsed().as_secs_f64() * 1000.0;

    if time_fixed_window {
        println!("Fixed-window time: {:.3} ms", elapsed_ms);
    } else {
        println!("Best window sum: {}", result.0);
        println!("Best window range: {} {}", result.1, result.2);
    }
}
