pub fn lower_bound_range_halving(values: &[i64], target: i64) -> i32 {
    let mut left: i32 = 0;
    let mut right: i32 = values.len() as i32;

    while left < right {
        let mid = left + (right - left) / 2;
        if values[mid as usize] < target {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    left
}

pub fn lower_bound_powers_of_two(values: &[i64], target: i64) -> i32 {
    let mut position: i32 = -1;
    let mut step: i32 = 1;
    while step < values.len() as i32 {
        step <<= 1;
    }

    while step > 0 {
        let next = position + step;
        if next < values.len() as i32 && values[next as usize] < target {
            position = next;
        }
        step >>= 1;
    }

    position + 1
}
