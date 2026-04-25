mod matrix_multiplication;

use matrix_multiplication::{multiply_matrices, Matrix};
use std::env;
use std::error::Error;
use std::fs;
use std::time::Instant;

struct Parser {
    tokens: Vec<String>,
    index: usize,
}

impl Parser {
    fn from_file(input_path: &str) -> Result<Self, Box<dyn Error>> {
        let content = fs::read_to_string(input_path)?;
        Ok(Self {
            tokens: content.split_whitespace().map(str::to_owned).collect(),
            index: 0,
        })
    }

    fn next_usize(&mut self, description: &str) -> Result<usize, Box<dyn Error>> {
        if self.index >= self.tokens.len() {
            return Err(format!("failed to read {description}").into());
        }
        let value = self.tokens[self.index].parse::<usize>()?;
        self.index += 1;
        Ok(value)
    }

    fn next_i64(&mut self, description: &str) -> Result<i64, Box<dyn Error>> {
        if self.index >= self.tokens.len() {
            return Err(format!("failed to read {description}").into());
        }
        let value = self.tokens[self.index].parse::<i64>()?;
        self.index += 1;
        Ok(value)
    }
}

fn read_matrix(parser: &mut Parser, rows: usize, cols: usize) -> Result<Matrix, Box<dyn Error>> {
    let mut matrix = vec![vec![0_i64; cols]; rows];
    for row in matrix.iter_mut().take(rows) {
        for value in row.iter_mut().take(cols) {
            *value = parser.next_i64("matrix value")?;
        }
    }
    Ok(matrix)
}

fn print_matrix(matrix: &Matrix) {
    let rows = matrix.len();
    let cols = matrix.first().map_or(0, Vec::len);
    println!("{rows} {cols}");
    for row in matrix {
        for (index, value) in row.iter().enumerate() {
            if index > 0 {
                print!(" ");
            }
            print!("{value}");
        }
        println!();
    }
}

fn run() -> Result<(), Box<dyn Error>> {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_matrix_multiplication = false;

    for argument in env::args().skip(1) {
        if argument == "--time-matrix-multiplication" {
            time_matrix_multiplication = true;
        } else {
            input_path = argument;
        }
    }

    let mut parser = Parser::from_file(&input_path)?;
    let m = parser.next_usize("first matrix row count")?;
    let n = parser.next_usize("first matrix column count")?;
    let left = read_matrix(&mut parser, m, n)?;

    let n2 = parser.next_usize("second matrix row count")?;
    let p = parser.next_usize("second matrix column count")?;
    if n != n2 {
        return Err("matrix dimensions are incompatible".into());
    }
    let right = read_matrix(&mut parser, n2, p)?;

    let start = Instant::now();
    let result = multiply_matrices(&left, &right)?;
    let elapsed = start.elapsed();

    if time_matrix_multiplication {
        eprintln!("matrix_multiplication_ms={:.6}", elapsed.as_secs_f64() * 1000.0);
    }

    print_matrix(&result);
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("error: {error}");
        std::process::exit(1);
    }
}
