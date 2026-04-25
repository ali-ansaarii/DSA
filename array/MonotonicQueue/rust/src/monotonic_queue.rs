use std::collections::VecDeque;

pub fn sliding_window_maximum(values: &[i64], window_size: usize) -> Vec<i64> {
    let mut candidate_indices: VecDeque<usize> = VecDeque::new();
    let mut maxima: Vec<i64> = Vec::with_capacity(values.len().saturating_sub(window_size) + 1);

    for (index, &value) in values.iter().enumerate() {
        while let Some(&front) = candidate_indices.front() {
            if front + window_size <= index {
                candidate_indices.pop_front();
            } else {
                break;
            }
        }

        while let Some(&back) = candidate_indices.back() {
            if values[back] <= value {
                candidate_indices.pop_back();
            } else {
                break;
            }
        }

        candidate_indices.push_back(index);

        if index + 1 >= window_size {
            maxima.push(values[*candidate_indices.front().unwrap()]);
        }
    }

    maxima
}
