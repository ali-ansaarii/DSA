pub fn selection_sort(values: &mut [i32]) {
    let n = values.len();

    for i in 0..n {
        let mut min_index = i;
        for j in (i + 1)..n {
            if values[j] < values[min_index] {
                min_index = j;
            }
        }

        if min_index != i {
            values.swap(i, min_index);
        }
    }
}
