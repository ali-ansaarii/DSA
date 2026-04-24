pub fn build_prefix_sums(values: &[i64]) -> Option<Vec<i64>> {
    let mut prefix = vec![0_i64; values.len() + 1];
    for (index, value) in values.iter().enumerate() {
        prefix[index + 1] = prefix[index].checked_add(*value)?;
    }
    Some(prefix)
}

pub fn range_sum(prefix: &[i64], left: usize, right: usize) -> Option<i64> {
    prefix[right + 1].checked_sub(prefix[left])
}
