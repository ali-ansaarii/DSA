use std::convert::TryFrom;

pub fn best_fixed_window(values: &[i64], k: usize) -> Option<(i64, usize, usize)> {
    let mut window_sum_wide = 0_i128;
    for &value in &values[..k] {
        window_sum_wide += value as i128;
    }
    let mut window_sum = i64::try_from(window_sum_wide).ok()?;

    let mut best_sum = window_sum;
    let mut best_left = 0_usize;
    let mut best_right = k - 1;

    for right in k..values.len() {
        window_sum_wide = window_sum_wide - values[right - k] as i128 + values[right] as i128;
        window_sum = i64::try_from(window_sum_wide).ok()?;
        let left = right - k + 1;
        if window_sum > best_sum {
            best_sum = window_sum;
            best_left = left;
            best_right = right;
        }
    }

    Some((best_sum, best_left, best_right))
}
