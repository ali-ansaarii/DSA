pub fn can_partition_with_max_group_sum(
    values: &[i64],
    max_groups: usize,
    limit: i64,
) -> Result<bool, String> {
    if max_groups == 0 {
        return Ok(false);
    }

    let mut groups_used = 1usize;
    let mut current_sum = 0i64;

    for &value in values {
        if value < 0 {
            return Err(String::from(
                "Binary Search on Answer partition baseline requires non-negative values",
            ));
        }
        if value > limit {
            return Ok(false);
        }
        if current_sum + value > limit {
            groups_used += 1;
            current_sum = value;
            if groups_used > max_groups {
                return Ok(false);
            }
        } else {
            current_sum += value;
        }
    }

    Ok(true)
}

pub fn minimize_largest_group_sum(values: &[i64], max_groups: usize) -> Result<i64, String> {
    if values.is_empty() {
        return Ok(0);
    }
    if max_groups == 0 {
        return Err(String::from("max_groups must be positive"));
    }

    let mut low = *values.iter().max().expect("values is not empty");
    let mut high: i64 = values.iter().sum();

    while low < high {
        let mid = low + (high - low) / 2;
        if can_partition_with_max_group_sum(values, max_groups, mid)? {
            high = mid;
        } else {
            low = mid + 1;
        }
    }

    Ok(low)
}
