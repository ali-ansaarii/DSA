pub fn best_fixed_window(values: &[i64], k: usize) -> Option<(i64, usize, usize)> {
    let mut window_sum = 0_i64;
    for &value in &values[..k] {
        window_sum = window_sum.checked_add(value)?;
    }

    let mut best_sum = window_sum;
    let mut best_left = 0_usize;
    let mut best_right = k - 1;

    for right in k..values.len() {
        window_sum = window_sum.checked_sub(values[right - k])?;
        window_sum = window_sum.checked_add(values[right])?;
        let left = right - k + 1;
        if window_sum > best_sum {
            best_sum = window_sum;
            best_left = left;
            best_right = right;
        }
    }

    Some((best_sum, best_left, best_right))
}
