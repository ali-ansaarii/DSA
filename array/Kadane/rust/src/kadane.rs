#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct KadaneResult {
    pub maximum_sum: i64,
    pub start_index: usize,
    pub end_index: usize,
}

pub fn max_subarray_kadane(values: &[i64]) -> Result<KadaneResult, &'static str> {
    if values.is_empty() {
        return Err("Kadane's Algorithm requires a non-empty array");
    }

    let mut current_sum = values[0];
    let mut best_sum = values[0];
    let mut current_start = 0usize;
    let mut best_start = 0usize;
    let mut best_end = 0usize;

    for (index, &value) in values.iter().enumerate().skip(1) {
        let extended_sum = current_sum + value;

        if extended_sum < value {
            current_sum = value;
            current_start = index;
        } else {
            current_sum = extended_sum;
        }

        if current_sum > best_sum {
            best_sum = current_sum;
            best_start = current_start;
            best_end = index;
        }
    }

    Ok(KadaneResult {
        maximum_sum: best_sum,
        start_index: best_start,
        end_index: best_end,
    })
}
