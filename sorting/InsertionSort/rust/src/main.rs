mod insertion_sort;

use insertion_sort::insertion_sort;
use std::env;
use std::error::Error;
use std::fs;
use std::time::Instant;

fn read_input(input_path: &str) -> Result<Vec<i64>, Box<dyn Error>> {
    let content = fs::read_to_string(input_path)?;
    let mut tokens = content.split_whitespace();

    let n_token = tokens
        .next()
        .ok_or("input must start with the number of elements")?;
    let n: usize = n_token.parse()?;

    let mut values = Vec::with_capacity(n);
    for _ in 0..n {
        let token = tokens
            .next()
            .ok_or("input ended before all elements were read")?;
        values.push(token.parse()?);
    }

    Ok(values)
}

fn print_values(values: &[i64]) {
    let output = values
        .iter()
        .map(i64::to_string)
        .collect::<Vec<_>>()
        .join(" ");
    println!("{output}");
}

fn run() -> Result<(), Box<dyn Error>> {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_flag_time_insertion_sort = false;

    for argument in env::args().skip(1) {
        if argument == "--time-insertion-sort" {
            time_flag_time_insertion_sort = true;
        } else {
            input_path = argument;
        }
    }

    let mut values = read_input(&input_path)?;

    if time_flag_time_insertion_sort {
        let start = Instant::now();
        insertion_sort(&mut values);
        let elapsed = start.elapsed().as_micros();
        eprintln!("algorithm_time_microseconds={elapsed}");
    } else {
        insertion_sort(&mut values);
    }

    print_values(&values);
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("error: {error}");
        std::process::exit(1);
    }
}
