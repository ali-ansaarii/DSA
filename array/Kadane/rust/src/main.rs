mod kadane;

use kadane::{max_subarray_kadane, KadaneResult};
use std::env;
use std::fs;
use std::process;
use std::time::Instant;

fn read_input(input_path: &str) -> Result<Vec<i64>, String> {
    let content = fs::read_to_string(input_path)
        .map_err(|error| format!("failed to read input file {input_path}: {error}"))?;
    let mut tokens = content.split_whitespace();

    let n: usize = tokens
        .next()
        .ok_or_else(|| String::from("input must start with a positive element count"))?
        .parse()
        .map_err(|error| format!("invalid element count: {error}"))?;

    if n == 0 {
        return Err(String::from("input must start with a positive element count"));
    }

    let mut values = Vec::with_capacity(n);
    for index in 0..n {
        let value = tokens
            .next()
            .ok_or_else(|| format!("missing array value at index {index}"))?
            .parse::<i64>()
            .map_err(|error| format!("invalid array value at index {index}: {error}"))?;
        values.push(value);
    }

    if tokens.next().is_some() {
        return Err(String::from("input contains more values than declared by n"));
    }

    Ok(values)
}

fn print_result(result: KadaneResult, values: &[i64]) {
    println!("maximum_sum: {}", result.maximum_sum);
    println!("start_index: {}", result.start_index);
    println!("end_index: {}", result.end_index);

    let subarray = values[result.start_index..=result.end_index]
        .iter()
        .map(i64::to_string)
        .collect::<Vec<_>>()
        .join(" ");
    println!("subarray: {subarray}");
}

fn run() -> Result<(), String> {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_kadane = false;

    for argument in env::args().skip(1) {
        if argument == "--time-kadane" {
            time_kadane = true;
        } else {
            input_path = argument;
        }
    }

    let values = read_input(&input_path)?;

    let (result, elapsed_ns) = if time_kadane {
        let start = Instant::now();
        let result = max_subarray_kadane(&values).map_err(String::from)?;
        (result, Some(start.elapsed().as_nanos()))
    } else {
        (max_subarray_kadane(&values).map_err(String::from)?, None)
    };

    print_result(result, &values);
    if let Some(ns) = elapsed_ns {
        println!("algorithm_time_ns: {ns}");
    }

    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("error: {error}");
        process::exit(1);
    }
}
