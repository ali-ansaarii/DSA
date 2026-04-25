mod binary_search_on_answer;

use binary_search_on_answer::minimize_largest_group_sum;
use std::env;
use std::fs;
use std::time::Instant;

struct ProblemInput {
    k: usize,
    values: Vec<i64>,
}

fn read_input(input_path: &str) -> Result<ProblemInput, String> {
    let contents = fs::read_to_string(input_path)
        .map_err(|error| format!("Unable to read input file {input_path}: {error}"))?;
    let tokens: Vec<&str> = contents.split_whitespace().collect();

    if tokens.len() < 2 {
        return Err(String::from("Input must start with n and k"));
    }

    let n: usize = tokens[0]
        .parse()
        .map_err(|error| format!("Invalid n value: {error}"))?;
    let k: usize = tokens[1]
        .parse()
        .map_err(|error| format!("Invalid k value: {error}"))?;

    if tokens.len() < 2 + n {
        return Err(String::from("Input ended before reading all array values"));
    }

    let mut values = Vec::with_capacity(n);
    for index in 0..n {
        let value = tokens[2 + index]
            .parse::<i64>()
            .map_err(|error| format!("Invalid array value at index {index}: {error}"))?;
        values.push(value);
    }

    Ok(ProblemInput { k, values })
}

fn main() {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_flag_time_binary_search_on_answer = false;

    for argument in env::args().skip(1) {
        if argument == "--time-binary-search-on-answer" {
            time_flag_time_binary_search_on_answer = true;
        } else {
            input_path = argument;
        }
    }

    let input = match read_input(&input_path) {
        Ok(input) => input,
        Err(error) => {
            eprintln!("Error: {error}");
            std::process::exit(1);
        }
    };

    let answer = if time_flag_time_binary_search_on_answer {
        let start = Instant::now();
        let result = minimize_largest_group_sum(&input.values, input.k);
        let elapsed = start.elapsed();
        eprintln!("algorithm_time_ns {}", elapsed.as_nanos());
        result
    } else {
        minimize_largest_group_sum(&input.values, input.k)
    };

    match answer {
        Ok(value) => println!("{value}"),
        Err(error) => {
            eprintln!("Error: {error}");
            std::process::exit(1);
        }
    }
}
