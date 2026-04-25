#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TernarySearchResult {
    pub index: usize,
    pub value: i64,
}

pub fn find_unimodal_maximum(values: &[i64]) -> Result<TernarySearchResult, String> {
    if values.is_empty() {
        return Err(String::from("ternary search requires a non-empty array"));
    }

    let mut left = 0usize;
    let mut right = values.len() - 1;

    while right > left + 3 {
        let third = (right - left) / 3;
        let mid1 = left + third;
        let mid2 = right - third;

        if values[mid1] < values[mid2] {
            left = mid1 + 1;
        } else if values[mid1] > values[mid2] {
            right = mid2 - 1;
        } else {
            left = mid1;
            right = mid2;
        }
    }

    let mut best_index = left;
    for index in (left + 1)..=right {
        if values[index] > values[best_index] {
            best_index = index;
        }
    }

    Ok(TernarySearchResult {
        index: best_index,
        value: values[best_index],
    })
}
