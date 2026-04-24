pub fn min_window_at_least_target(values: &[i64], target: i64) -> Option<(i32, i32, i32)> {
    let mut window_sum = 0_i64;
    let mut left = 0_usize;
    let mut best_length = -1_i32;
    let mut best_left = -1_i32;
    let mut best_right = -1_i32;

    for (right, &value) in values.iter().enumerate() {
        window_sum = window_sum.checked_add(value)?;

        while window_sum >= target {
            let current_length = (right - left + 1) as i32;
            if best_length == -1 || current_length < best_length {
                best_length = current_length;
                best_left = left as i32;
                best_right = right as i32;
            }
            window_sum = window_sum.checked_sub(values[left])?;
            left += 1;
        }
    }

    Some((best_length, best_left, best_right))
}
