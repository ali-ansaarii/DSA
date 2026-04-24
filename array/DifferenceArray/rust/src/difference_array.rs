pub fn build_difference_array(values: &[i64]) -> Option<Vec<i64>> {
    if values.is_empty() {
        return Some(Vec::new());
    }

    let mut diff = vec![0_i64; values.len()];
    diff[0] = values[0];
    for index in 1..values.len() {
        diff[index] = values[index].checked_sub(values[index - 1])?;
    }
    Some(diff)
}

pub fn apply_range_add(diff: &mut [i64], left: usize, right: usize, delta: i64) -> Option<()> {
    diff[left] = diff[left].checked_add(delta)?;
    if right + 1 < diff.len() {
        diff[right + 1] = diff[right + 1].checked_sub(delta)?;
    }
    Some(())
}

pub fn reconstruct_values(diff: &[i64]) -> Option<Vec<i64>> {
    if diff.is_empty() {
        return Some(Vec::new());
    }

    let mut values = vec![0_i64; diff.len()];
    values[0] = diff[0];
    for index in 1..diff.len() {
        values[index] = values[index - 1].checked_add(diff[index])?;
    }
    Some(values)
}
