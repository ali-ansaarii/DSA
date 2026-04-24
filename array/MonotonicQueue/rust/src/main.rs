mod monotonic_queue;

use monotonic_queue::sliding_window_maximum;
use std::env;
use std::fs;
use std::process;
use std::time::Instant;

fn read_input(input_path: &str) -> Result<(Vec<i64>, usize), String> {
    let content = fs::read_to_string(input_path)
        .map_err(|_| format!("Failed to open input file: {input_path}"))?;
    let tokens: Vec<&str> = content.split_whitespace().collect();

    if tokens.len() < 2 {
        return Err(String::from("Invalid input header."));
    }

    let n = tokens[0]
        .parse::<usize>()
        .map_err(|_| String::from("Invalid input header."))?;
    let window_size = tokens[1]
        .parse::<usize>()
        .map_err(|_| String::from("Invalid input header."))?;

    if n == 0 || window_size == 0 || window_size > n {
        return Err(String::from("Invalid input header."));
    }

    if tokens.len() != n + 2 {
        return Err(String::from("Input size does not match header."));
    }

    let mut values = Vec::with_capacity(n);
    for (index, token) in tokens[2..].iter().enumerate() {
        let value = token
            .parse::<i64>()
            .map_err(|_| format!("Failed to read array value at index {index}."))?;
        values.push(value);
    }

    Ok((values, window_size))
}

fn print_answer(maxima: &[i64]) {
    print!("Window maxima:");
    for value in maxima {
        print!(" {}", value);
    }
    println!();
}

fn main() {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_monotonic_queue = false;

    for argument in env::args().skip(1) {
        if argument == "--time-monotonic-queue" {
            time_monotonic_queue = true;
        } else {
            input_path = argument;
        }
    }

    let (values, window_size) = match read_input(&input_path) {
        Ok(data) => data,
        Err(message) => {
            eprintln!("{message}");
            process::exit(1);
        }
    };

    let start = Instant::now();
    let maxima = sliding_window_maximum(&values, window_size);
    let elapsed = start.elapsed();

    if time_monotonic_queue {
        println!("Monotonic-queue time: {:.6} ms", elapsed.as_secs_f64() * 1000.0);
    } else {
        print_answer(&maxima);
    }
}
