mod prefix_sum_2d;

use prefix_sum_2d::{answer_rectangle_queries, RectQuery};
use std::env;
use std::fs;
use std::time::Instant;

fn parse_input(input_path: &str) -> (Vec<Vec<i64>>, Vec<RectQuery>) {
    let contents = fs::read_to_string(input_path)
        .unwrap_or_else(|error| panic!("failed to read input file {}: {}", input_path, error));
    let mut values = contents.split_whitespace();

    let rows: usize = values.next().expect("missing row count").parse().expect("invalid row count");
    let cols: usize = values.next().expect("missing column count").parse().expect("invalid column count");

    let mut matrix = vec![vec![0_i64; cols]; rows];
    for row in matrix.iter_mut() {
        for value in row.iter_mut() {
            *value = values
                .next()
                .expect("missing matrix value")
                .parse()
                .expect("invalid matrix value");
        }
    }

    let query_count: usize = values
        .next()
        .expect("missing query count")
        .parse()
        .expect("invalid query count");
    let mut queries = Vec::with_capacity(query_count);

    for _ in 0..query_count {
        let r1 = values.next().expect("missing r1").parse().expect("invalid r1");
        let c1 = values.next().expect("missing c1").parse().expect("invalid c1");
        let r2 = values.next().expect("missing r2").parse().expect("invalid r2");
        let c2 = values.next().expect("missing c2").parse().expect("invalid c2");
        queries.push(RectQuery { r1, c1, r2, c2 });
    }

    (matrix, queries)
}

fn main() {
    let mut input_path = String::from("inputs/input.txt");
    let mut time_flag_time_prefix_sum_2d = false;

    for argument in env::args().skip(1) {
        if argument == "--time-prefix-sum-2d" {
            time_flag_time_prefix_sum_2d = true;
        } else {
            input_path = argument;
        }
    }

    let (matrix, queries) = parse_input(&input_path);

    let start = Instant::now();
    let answers = answer_rectangle_queries(&matrix, &queries);
    let elapsed = start.elapsed();

    if time_flag_time_prefix_sum_2d {
        eprintln!("algorithm_time_ms {:.3}", elapsed.as_secs_f64() * 1000.0);
    }

    let mut output = String::new();
    for answer in answers {
        output.push_str(&format!("{}\n", answer));
    }
    print!("{}", output);
}
