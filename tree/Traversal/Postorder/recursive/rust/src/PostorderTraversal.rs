#[allow(non_snake_case)]
pub fn PostorderTraversal(left_children: &[i32], right_children: &[i32], root: usize) -> Vec<usize> {
    let mut order = Vec::new();

    fn traverse(node: usize, left_children: &[i32], right_children: &[i32], order: &mut Vec<usize>) {
        let left_child = left_children[node];
        if left_child != -1 {
            traverse(left_child as usize, left_children, right_children, order);
        }

        let right_child = right_children[node];
        if right_child != -1 {
            traverse(right_child as usize, left_children, right_children, order);
        }

        order.push(node);
    }

    traverse(root, left_children, right_children, &mut order);
    order
}
