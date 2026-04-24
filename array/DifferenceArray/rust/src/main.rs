mod difference_array;

use difference_array::{apply_range_add, build_difference_array, reconstruct_values};
use std::env;
use std::fs;
use std::time::Instant;

type Update = (usize, usize, i64);

fn read_input(input_path: &str) -> Result<(Vec<i64>, Vec<Update>), String> {
    let content = fs::read_to_string(input_path)
        .map_err(|_| format!("Failed to open input file: {input_path}"))?;
    let tokens: Vec<&str> = content.split_whitespace().collect();
    if tokens.len() < 2 {
        return Err("Invalid input header.".to_string());
    }

    let n = tokens[0]
        .parse::<usize>()
        .map_err(|_| "Invalid input header.".to_string())?;
    let q = tokens[1]
        .parse::<usize>()
        .map_err(|_| "Invalid input header.".to_string())?;

    let expected = 2 + n + 3 * q;
    if tokens.len() != expected {
        return Err("Input size does not match header.".to_string());
    }

    let mut values = Vec::with_capacity(n);
    for token in &tokens[2..2 + n] {
        values.push(
            token
                .parse::<i64>()
                .map_err(|_| "Invalid array value.".to_string())?,
        );
    }

    let mut updates = Vec::with_capacity(q);
    let mut cursor = 2 + n;
    for _ in 0..q {
        let left = tokens[cursor]
            .parse::<usize>()
            .map_err(|_| "Invalid update range.".to_string())?;
        let right = tokens[cursor + 1]
            .parse::<usize>()
            .map_err(|_| "Invalid update range.".to_string())?;
        let delta = tokens[cursor + 2]
            .parse::<i64>()
            .map_err(|_| "Invalid update delta.".to_string())?;
        cursor += 3;

        if left > right || right >= n {
            return Err("Invalid update range.".to_string());
        }

        updates.push((left, right, delta));
    }

    Ok((values, updates))
}

fn run_difference_array(values: &[i64], updates: &[Update]) -> Result<Vec<i64>, String> {
    let mut diff =
        build_difference_array(values).ok_or_else(|| "Overflow while building the difference array.".to_string())?;

    for &(left, right, delta) in updates {
        apply_range_add(&mut diff, left, right, delta)
            .ok_or_else(|| "Overflow while applying a range update.".to_string())?;
    }

    reconstruct_values(&diff)
        .ok_or_else(|| "Overflow while reconstructing the final array.".to_string())
}

fn print_values(values: &[i64]) {
    print!("Final array:");
    for value in values {
        print!(" {}", value);
    }
    println!();
}

fn main() {
    let mut input_path = "inputs/input.txt".to_string();
    let mut time_difference_array = false;

    for argument in env::args().skip(1) {
        if argument == "--time-difference-array" {
            time_difference_array = true;
        } else {
            input_path = argument;
        }
    }

    let (values, updates) = match read_input(&input_path) {
        Ok(parsed) => parsed,
        Err(message) => {
            eprintln!("{message}");
            std::process::exit(1);
        }
    };

    let start = Instant::now();
    let final_values = match run_difference_array(&values, &updates) {
        Ok(result) => result,
        Err(message) => {
            eprintln!("{message}");
            std::process::exit(1);
        }
    };
    let elapsed_ms = start.elapsed().as_secs_f64() * 1000.0;

    if time_difference_array {
        println!("Difference-array time: {:.3} ms", elapsed_ms);
    } else {
        print_values(&final_values);
    }
}
