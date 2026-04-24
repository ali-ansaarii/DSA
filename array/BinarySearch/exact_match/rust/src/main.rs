mod binary_search_exact;

use binary_search_exact::binary_search_exact;
use std::env;
use std::fs;
use std::time::Instant;

struct ProgramOptions {
    input_path: String,
    benchmark_mode: bool,
}

fn parse_arguments(args: &[String]) -> Result<ProgramOptions, String> {
    let mut input_path: Option<String> = None;
    let mut benchmark_mode = false;

    for argument in args.iter().skip(1) {
        if argument == "--time-exact" {
            benchmark_mode = true;
        } else if input_path.is_none() {
            input_path = Some(argument.clone());
        } else {
            return Err("Usage: binary_search_exact <input-file> [--time-exact]".to_string());
        }
    }

    let Some(input_path) = input_path else {
        return Err("Usage: binary_search_exact <input-file> [--time-exact]".to_string());
    };

    Ok(ProgramOptions {
        input_path,
        benchmark_mode,
    })
}

fn read_input(path: &str) -> Result<(Vec<i64>, Vec<i64>), String> {
    let contents = fs::read_to_string(path).map_err(|error| format!("Failed to open input file: {error}"))?;
    let tokens = contents.split_whitespace().collect::<Vec<&str>>();

    if tokens.len() < 2 {
        return Err("Invalid input header".to_string());
    }

    let mut position = 0usize;
    let value_count: usize = tokens[position]
        .parse()
        .map_err(|_| "Invalid value count".to_string())?;
    position += 1;
    let query_count: usize = tokens[position]
        .parse()
        .map_err(|_| "Invalid query count".to_string())?;
    position += 1;

    if position + value_count + query_count != tokens.len() {
        return Err("Input length does not match n and q".to_string());
    }

    let mut values = Vec::with_capacity(value_count);
    for _ in 0..value_count {
        values.push(
            tokens[position]
                .parse::<i64>()
                .map_err(|_| "Invalid array value".to_string())?,
        );
        position += 1;
    }

    let mut queries = Vec::with_capacity(query_count);
    for _ in 0..query_count {
        queries.push(
            tokens[position]
                .parse::<i64>()
                .map_err(|_| "Invalid query value".to_string())?,
        );
        position += 1;
    }

    Ok((values, queries))
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let options = match parse_arguments(&args) {
        Ok(options) => options,
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(1);
        }
    };

    let (values, queries) = match read_input(&options.input_path) {
        Ok(parsed) => parsed,
        Err(error) => {
            eprintln!("{error}");
            std::process::exit(1);
        }
    };

    let mut results = Vec::with_capacity(queries.len());
    let begin = Instant::now();
    for query in queries {
        results.push(binary_search_exact(&values, query));
    }
    let elapsed_ms = begin.elapsed().as_secs_f64() * 1000.0;

    if options.benchmark_mode {
        println!("Exact binary search time: {:.3} ms", elapsed_ms);
        return;
    }

    print!("Exact-match results:");
    for result in results {
        print!(" {}", result);
    }
    println!();
}
