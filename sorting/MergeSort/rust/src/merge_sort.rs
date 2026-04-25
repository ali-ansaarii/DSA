pub fn merge_sort(values: &[i64]) -> Vec<i64> {
    let mut sorted = values.to_vec();
    let mut buffer = vec![0_i64; sorted.len()];
    merge_sort_recursive(&mut sorted, &mut buffer, 0, values.len());
    sorted
}

fn merge_sort_recursive(values: &mut [i64], buffer: &mut [i64], left: usize, right: usize) {
    if right - left <= 1 {
        return;
    }

    let mid = left + (right - left) / 2;
    merge_sort_recursive(values, buffer, left, mid);
    merge_sort_recursive(values, buffer, mid, right);
    merge_ranges(values, buffer, left, mid, right);
}

fn merge_ranges(values: &mut [i64], buffer: &mut [i64], left: usize, mid: usize, right: usize) {
    let mut i = left;
    let mut j = mid;
    let mut k = left;

    while i < mid && j < right {
        if values[i] <= values[j] {
            buffer[k] = values[i];
            i += 1;
        } else {
            buffer[k] = values[j];
            j += 1;
        }
        k += 1;
    }

    while i < mid {
        buffer[k] = values[i];
        i += 1;
        k += 1;
    }

    while j < right {
        buffer[k] = values[j];
        j += 1;
        k += 1;
    }

    values[left..right].copy_from_slice(&buffer[left..right]);
}
