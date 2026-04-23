#[allow(non_snake_case)]
pub fn InorderTraversal(left_children: &[i32], right_children: &[i32], root: usize) -> Vec<usize> {
    let mut order = Vec::new();
    let mut stack = Vec::new();
    let mut current = Some(root);

    while current.is_some() || !stack.is_empty() {
        while let Some(node) = current {
            stack.push(node);
            let left_child = left_children[node];
            current = if left_child == -1 {
                None
            } else {
                Some(left_child as usize)
            };
        }

        let node = stack.pop().unwrap();
        order.push(node);
        let right_child = right_children[node];
        current = if right_child == -1 {
            None
        } else {
            Some(right_child as usize)
        };
    }

    order
}
