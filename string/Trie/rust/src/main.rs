mod trie;

use std::env;
use std::fs;
use std::process;
use std::time::Instant;

use trie::{execute_trie_commands, Operation};

fn read_operations(input_path: &str) -> Result<Vec<Operation>, String> {
    let contents = fs::read_to_string(input_path)
        .map_err(|error| format!("Unable to read input file {input_path}: {error}"))?;
    let mut tokens = contents.split_whitespace();

    let operation_count: usize = tokens
        .next()
        .ok_or_else(|| String::from("Input file is empty"))?
        .parse()
        .map_err(|error| format!("Invalid command count: {error}"))?;

    let mut operations = Vec::with_capacity(operation_count);
    for _ in 0..operation_count {
        let command = tokens
            .next()
            .ok_or_else(|| String::from("Input file ended before a command was read"))?
            .to_string();
        let value = tokens
            .next()
            .ok_or_else(|| String::from("Input file ended before a command value was read"))?
            .to_string();
        operations.push(Operation { command, value });
    }

    Ok(operations)
}

fn main() {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_flag_time_trie = false;

    for argument in env::args().skip(1) {
        if argument == "--time-trie" {
            time_flag_time_trie = true;
        } else {
            input_path = argument;
        }
    }

    let operations = match read_operations(&input_path) {
        Ok(operations) => operations,
        Err(error) => {
            eprintln!("Error: {error}");
            process::exit(1);
        }
    };

    let start = Instant::now();
    let output = match execute_trie_commands(&operations) {
        Ok(output) => output,
        Err(error) => {
            eprintln!("Error: {error}");
            process::exit(1);
        }
    };
    let elapsed = start.elapsed();

    for line in output {
        println!("{line}");
    }

    if time_flag_time_trie {
        eprintln!("trie_processing_ms={:.6}", elapsed.as_secs_f64() * 1000.0);
    }
}
