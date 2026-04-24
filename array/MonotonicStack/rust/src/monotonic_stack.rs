pub fn next_greater_elements(values: &[i64]) -> Vec<i64> {
    let mut answer = vec![-1_i64; values.len()];
    let mut stack: Vec<i64> = Vec::with_capacity(values.len());

    for index in (0..values.len()).rev() {
        while let Some(&top) = stack.last() {
            if top <= values[index] {
                stack.pop();
            } else {
                break;
            }
        }
        if let Some(&top) = stack.last() {
            answer[index] = top;
        }
        stack.push(values[index]);
    }

    answer
}
