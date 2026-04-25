pub type Matrix = Vec<Vec<i64>>;

pub fn multiply_matrices(left: &Matrix, right: &Matrix) -> Matrix {
    if left.is_empty() || right.is_empty() {
        panic!("matrices must be non-empty");
    }

    let rows = left.len();
    let shared = left[0].len();
    let right_rows = right.len();
    let cols = right[0].len();

    if shared == 0 || cols == 0 || shared != right_rows {
        panic!("matrix dimensions are incompatible");
    }
    if left.iter().any(|row| row.len() != shared) {
        panic!("left matrix rows have inconsistent lengths");
    }
    if right.iter().any(|row| row.len() != cols) {
        panic!("right matrix rows have inconsistent lengths");
    }

    let mut result = vec![vec![0_i64; cols]; rows];
    for i in 0..rows {
        for k in 0..shared {
            let value = left[i][k];
            for j in 0..cols {
                result[i][j] += value * right[k][j];
            }
        }
    }
    result
}
