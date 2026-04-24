#[derive(Clone, Copy)]
pub struct Edge {
    pub source: usize,
    pub target: usize,
    pub weight: i64,
}

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum Status {
    Ok,
    Disconnected,
    Overflow,
}

pub struct Result {
    pub status: Status,
    pub total_weight: i64,
    pub chosen_edges: Vec<Edge>,
}

struct DisjointSetUnion {
    parent: Vec<usize>,
    size: Vec<usize>,
}

impl DisjointSetUnion {
    fn new(node_count: usize) -> Self {
        Self {
            parent: (0..node_count).collect(),
            size: vec![1; node_count],
        }
    }

    fn find(&mut self, node: usize) -> usize {
        if self.parent[node] == node {
            return node;
        }
        let root = self.find(self.parent[node]);
        self.parent[node] = root;
        root
    }

    fn unite(&mut self, left: usize, right: usize) -> bool {
        let mut left_root = self.find(left);
        let mut right_root = self.find(right);
        if left_root == right_root {
            return false;
        }
        if self.size[left_root] < self.size[right_root] {
            std::mem::swap(&mut left_root, &mut right_root);
        }
        self.parent[right_root] = left_root;
        self.size[left_root] += self.size[right_root];
        true
    }
}

fn normalize(edge: Edge) -> Edge {
    if edge.source <= edge.target {
        edge
    } else {
        Edge {
            source: edge.target,
            target: edge.source,
            weight: edge.weight,
        }
    }
}

pub fn kruskal_mst(node_count: usize, edges: &[Edge]) -> Result {
    let mut sorted_edges = edges.iter().copied().map(normalize).collect::<Vec<Edge>>();
    sorted_edges.sort_by_key(|edge| (edge.weight, edge.source, edge.target));

    let mut dsu = DisjointSetUnion::new(node_count);
    let mut total_weight = 0_i64;
    let mut chosen_edges = Vec::with_capacity(node_count.saturating_sub(1));

    for edge in sorted_edges {
        if !dsu.unite(edge.source, edge.target) {
            continue;
        }

        let Some(updated) = total_weight.checked_add(edge.weight) else {
            return Result {
                status: Status::Overflow,
                total_weight,
                chosen_edges,
            };
        };

        total_weight = updated;
        chosen_edges.push(edge);

        if chosen_edges.len() == node_count.saturating_sub(1) {
            return Result {
                status: Status::Ok,
                total_weight,
                chosen_edges,
            };
        }
    }

    Result {
        status: Status::Disconnected,
        total_weight,
        chosen_edges,
    }
}
