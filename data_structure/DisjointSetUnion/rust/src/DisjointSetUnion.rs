#[derive(Clone, Copy)]
pub enum OperationType {
    Union,
    Connected,
    Find,
}

#[derive(Clone, Copy)]
pub struct Operation {
    pub kind: OperationType,
    pub first: usize,
    pub second: usize,
}

#[allow(non_snake_case)]
pub fn DisjointSetUnion(n: usize, operations: &[Operation]) -> Vec<String> {
    let mut parent: Vec<usize> = (0..n).collect();
    let mut component_size = vec![1usize; n];

    fn find_root(parent: &mut [usize], node: usize) -> usize {
        if parent[node] == node {
            return node;
        }

        parent[node] = find_root(parent, parent[node]);
        parent[node]
    }

    let mut query_results = Vec::new();
    for operation in operations {
        match operation.kind {
            OperationType::Union => {
                let mut root_a = find_root(&mut parent, operation.first);
                let mut root_b = find_root(&mut parent, operation.second);

                if root_a == root_b {
                    continue;
                }

                if component_size[root_a] < component_size[root_b]
                    || (component_size[root_a] == component_size[root_b] && root_a > root_b)
                {
                    std::mem::swap(&mut root_a, &mut root_b);
                }

                parent[root_b] = root_a;
                component_size[root_a] += component_size[root_b];
            }
            OperationType::Connected => {
                query_results.push(if find_root(&mut parent, operation.first) == find_root(&mut parent, operation.second) {
                    "true".to_string()
                } else {
                    "false".to_string()
                });
            }
            OperationType::Find => {
                query_results.push(find_root(&mut parent, operation.first).to_string());
            }
        }
    }

    query_results
}
