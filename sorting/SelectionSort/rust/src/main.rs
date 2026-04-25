mod selection_sort;

use selection_sort::selection_sort;
use std::env;
use std::error::Error;
use std::fs;
use std::time::Instant;

fn read_input(input_path: &str) -> Result<Vec<i32>, Box<dyn Error>> {
    let content = fs::read_to_string(input_path)?;
    let mut tokens = content.split_whitespace();

    let n_text = tokens
        .next()
        .ok_or_else(|| String::from("input must start with the array length"))?;
    let n: usize = n_text.parse()?;

    let mut values = Vec::with_capacity(n);
    for _ in 0..n {
        let value_text = tokens
            .next()
            .ok_or_else(|| String::from("input ended before reading all array values"))?;
        values.push(value_text.parse()?);
    }

    Ok(values)
}

fn format_values(values: &[i32]) -> String {
    values
        .iter()
        .map(i32::to_string)
        .collect::<Vec<String>>()
        .join(" ")
}

fn run() -> Result<(), Box<dyn Error>> {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_flag_time_selection_sort = false;

    for argument in env::args().skip(1) {
        if argument == "--time-selection-sort" {
            time_flag_time_selection_sort = true;
        } else {
            input_path = argument;
        }
    }

    let mut values = read_input(&input_path)?;

    if time_flag_time_selection_sort {
        let start = Instant::now();
        selection_sort(&mut values);
        let elapsed = start.elapsed();
        eprintln!("algorithm_time_ms={:.6}", elapsed.as_secs_f64() * 1000.0);
    } else {
        selection_sort(&mut values);
    }

    println!("{}", format_values(&values));
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("Error: {error}");
        std::process::exit(1);
    }
}
