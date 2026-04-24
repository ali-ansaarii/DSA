pub fn binary_search_exact(values: &[i64], target: i64) -> i32 {
    let mut left: i32 = 0;
    let mut right: i32 = values.len() as i32 - 1;

    while left <= right {
        let mid = left + (right - left) / 2;
        let value = values[mid as usize];

        if value == target {
            return mid;
        }

        if value < target {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    -1
}
