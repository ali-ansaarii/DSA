mod merge_sort;

use merge_sort::merge_sort;
use std::env;
use std::error::Error;
use std::fs;
use std::time::Instant;

fn read_input(input_path: &str) -> Result<Vec<i64>, Box<dyn Error>> {
    let content = fs::read_to_string(input_path)?;
    let mut tokens = content.split_whitespace();

    let n_token = tokens.next().ok_or("input must start with the element count")?;
    let n: usize = n_token.parse()?;

    let mut values = Vec::with_capacity(n);
    for _ in 0..n {
        let token = tokens.next().ok_or("input ended before reading all elements")?;
        values.push(token.parse()?);
    }

    if tokens.next().is_some() {
        return Err("input contains extra tokens after the declared elements".into());
    }

    Ok(values)
}

fn format_values(values: &[i64]) -> String {
    values
        .iter()
        .map(i64::to_string)
        .collect::<Vec<String>>()
        .join(" ")
}

fn run() -> Result<(), Box<dyn Error>> {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_flag_time_merge_sort = false;

    for argument in env::args().skip(1) {
        if argument == "--time-merge-sort" {
            time_flag_time_merge_sort = true;
        } else {
            input_path = argument;
        }
    }

    let values = read_input(&input_path)?;

    let sorted = if time_flag_time_merge_sort {
        let start = Instant::now();
        let sorted = merge_sort(&values);
        let elapsed = start.elapsed();
        eprintln!("merge_sort_seconds={:.9}", elapsed.as_secs_f64());
        sorted
    } else {
        merge_sort(&values)
    };

    println!("{}", format_values(&sorted));
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("Error: {error}");
        std::process::exit(1);
    }
}
