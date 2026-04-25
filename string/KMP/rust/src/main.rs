mod kmp;

use std::env;
use std::error::Error;
use std::fs;
use std::time::Instant;

fn read_input(input_path: &str) -> Result<(String, String), Box<dyn Error>> {
    let content = fs::read_to_string(input_path)?;
    let mut lines = content.lines();
    let text = lines
        .next()
        .ok_or("input file must contain a text line")?
        .to_string();
    let pattern = lines
        .next()
        .ok_or("input file must contain a pattern line")?
        .to_string();

    Ok((text, pattern))
}

fn print_matches(matches: &[usize]) {
    let output = matches
        .iter()
        .map(|index| index.to_string())
        .collect::<Vec<_>>()
        .join(" ");
    println!("{}", output);
}

fn run() -> Result<(), Box<dyn Error>> {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_flag_time_kmp = false;

    for argument in env::args().skip(1) {
        if argument == "--time-kmp" {
            time_flag_time_kmp = true;
        } else {
            input_path = argument;
        }
    }

    let (text, pattern) = read_input(&input_path)?;

    let matches = if time_flag_time_kmp {
        let start = Instant::now();
        let result = kmp::kmp(&text, &pattern);
        let elapsed_ms = start.elapsed().as_secs_f64() * 1000.0;
        eprintln!("algorithm_time_ms: {:.6}", elapsed_ms);
        result
    } else {
        kmp::kmp(&text, &pattern)
    };

    print_matches(&matches);
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("Error: {}", error);
        std::process::exit(1);
    }
}
