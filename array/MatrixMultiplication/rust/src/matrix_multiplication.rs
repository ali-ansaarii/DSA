pub type Matrix = Vec<Vec<i64>>;

pub fn multiply_matrices(left: &Matrix, right: &Matrix) -> Result<Matrix, String> {
    if left.is_empty() || right.is_empty() {
        return Err("matrices must be non-empty".to_string());
    }

    let rows = left.len();
    let shared = left[0].len();
    let right_rows = right.len();
    let cols = right[0].len();

    if shared == 0 || cols == 0 || shared != right_rows {
        return Err("matrix dimensions are incompatible".to_string());
    }
    if left.iter().any(|row| row.len() != shared) {
        return Err("left matrix rows have inconsistent lengths".to_string());
    }
    if right.iter().any(|row| row.len() != cols) {
        return Err("right matrix rows have inconsistent lengths".to_string());
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
    Ok(result)
}
