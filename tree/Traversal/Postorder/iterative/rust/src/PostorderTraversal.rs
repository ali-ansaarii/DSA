#[allow(non_snake_case)]
pub fn PostorderTraversal(left_children: &[i32], right_children: &[i32], root: usize) -> Vec<usize> {
    let mut order = Vec::new();
    let mut stack = vec![(root, false)];

    while let Some((node, expanded)) = stack.pop() {
        if expanded {
            order.push(node);
            continue;
        }

        stack.push((node, true));

        let right_child = right_children[node];
        if right_child != -1 {
            stack.push((right_child as usize, false));
        }

        let left_child = left_children[node];
        if left_child != -1 {
            stack.push((left_child as usize, false));
        }
    }

    order
}
