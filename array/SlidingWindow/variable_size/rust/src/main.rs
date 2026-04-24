mod sliding_window;

use sliding_window::min_window_at_least_target;
use std::env;
use std::fs;
use std::time::Instant;

fn read_input(input_path: &str) -> Result<(Vec<i64>, i64), String> {
    let content = fs::read_to_string(input_path)
        .map_err(|_| format!("Failed to open input file: {input_path}"))?;
    let tokens: Vec<&str> = content.split_whitespace().collect();
    if tokens.len() < 2 {
        return Err("Invalid input header.".to_string());
    }

    let n = tokens[0]
        .parse::<usize>()
        .map_err(|_| "Invalid input header.".to_string())?;
    let target = tokens[1]
        .parse::<i64>()
        .map_err(|_| "Invalid input header.".to_string())?;
    if n == 0 || target <= 0 {
        return Err("Invalid input header.".to_string());
    }
    if tokens.len() != 2 + n {
        return Err("Input size does not match header.".to_string());
    }

    let mut values = Vec::with_capacity(n);
    for token in &tokens[2..] {
        let value = token
            .parse::<i64>()
            .map_err(|_| "Invalid array value.".to_string())?;
        if value <= 0 {
            return Err("Variable-size sliding window requires positive values.".to_string());
        }
        values.push(value);
    }

    Ok((values, target))
}

fn main() {
    let mut input_path = "inputs/input.txt".to_string();
    let mut time_variable_window = false;

    for argument in env::args().skip(1) {
        if argument == "--time-variable-window" {
            time_variable_window = true;
        } else {
            input_path = argument;
        }
    }

    let (values, target) = match read_input(&input_path) {
        Ok(parsed) => parsed,
        Err(message) => {
            eprintln!("{message}");
            std::process::exit(1);
        }
    };

    let start = Instant::now();
    let result = match min_window_at_least_target(&values, target) {
        Some(result) => result,
        None => {
            eprintln!("Overflow while evaluating variable-size windows.");
            std::process::exit(1);
        }
    };
    let elapsed_ms = start.elapsed().as_secs_f64() * 1000.0;

    if time_variable_window {
        println!("Variable-window time: {:.3} ms", elapsed_ms);
    } else if result.0 == -1 {
        println!("No valid window");
    } else {
        println!("Minimum window length: {}", result.0);
        println!("Minimum window range: {} {}", result.1, result.2);
    }
}
