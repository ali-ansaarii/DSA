mod ternary_search;

use std::env;
use std::error::Error;
use std::fs;
use std::time::Instant;

use ternary_search::find_unimodal_maximum;

fn read_input(input_path: &str) -> Result<Vec<i64>, Box<dyn Error>> {
    let content = fs::read_to_string(input_path)?;
    let mut tokens = content.split_whitespace();

    let n: usize = tokens
        .next()
        .ok_or("input must start with a positive element count")?
        .parse()?;
    if n == 0 {
        return Err("input must start with a positive element count".into());
    }

    let mut values = Vec::with_capacity(n);
    for _ in 0..n {
        let value: i64 = tokens
            .next()
            .ok_or("input ended before all array values were read")?
            .parse()?;
        values.push(value);
    }

    Ok(values)
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_ternary_search = false;

    for argument in env::args().skip(1) {
        if argument == "--time-ternary-search" {
            time_ternary_search = true;
        } else {
            input_path = argument;
        }
    }

    let values = read_input(&input_path)?;

    let mut elapsed_ns = 0u128;
    let result = if time_ternary_search {
        let start = Instant::now();
        let result = find_unimodal_maximum(&values)?;
        elapsed_ns = start.elapsed().as_nanos();
        result
    } else {
        find_unimodal_maximum(&values)?
    };

    println!("Maximum index: {}", result.index);
    println!("Maximum value: {}", result.value);
    if time_ternary_search {
        println!("Algorithm time (ns): {}", elapsed_ns);
    }

    Ok(())
}
