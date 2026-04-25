#[derive(Clone, Copy)]
pub enum Query {
    Add { index: usize, delta: i64 },
    Sum { left: usize, right: usize },
}

pub struct SegmentTree {
    n: usize,
    tree: Vec<i64>,
}

impl SegmentTree {
    pub fn new(initial_values: &[i64]) -> Result<Self, String> {
        let n = initial_values.len();
        let mut tree = vec![0_i64; 2 * n];
        for (index, value) in initial_values.iter().enumerate() {
            tree[n + index] = *value;
        }
        for node in (1..n).rev() {
            tree[node] = tree[2 * node]
                .checked_add(tree[2 * node + 1])
                .ok_or_else(|| String::from("Segment tree overflowed while building the initial state."))?;
        }
        Ok(Self { n, tree })
    }

    pub fn add(&mut self, index: usize, delta: i64) -> Result<(), String> {
        let mut node = index + self.n;
        self.tree[node] = self.tree[node]
            .checked_add(delta)
            .ok_or_else(|| String::from("Segment tree overflowed while applying an update."))?;

        node /= 2;
        while node > 0 {
            self.tree[node] = self.tree[2 * node]
                .checked_add(self.tree[2 * node + 1])
                .ok_or_else(|| String::from("Segment tree overflowed while applying an update."))?;
            node /= 2;
        }

        Ok(())
    }

    pub fn range_sum(&self, left: usize, right: usize) -> Result<i64, String> {
        let mut result = 0_i64;
        let mut l = left + self.n;
        let mut r = right + self.n + 1;

        while l < r {
            if l & 1 == 1 {
                result = result
                    .checked_add(self.tree[l])
                    .ok_or_else(|| String::from("Segment tree overflowed while evaluating a sum query."))?;
                l += 1;
            }
            if r & 1 == 1 {
                r -= 1;
                result = result
                    .checked_add(self.tree[r])
                    .ok_or_else(|| String::from("Segment tree overflowed while evaluating a sum query."))?;
            }
            l /= 2;
            r /= 2;
        }

        Ok(result)
    }
}

pub fn process_segment_tree_queries(initial_values: &[i64], queries: &[Query]) -> Result<Vec<i64>, String> {
    let mut tree = SegmentTree::new(initial_values)?;
    let mut results = Vec::new();

    for query in queries {
        match *query {
            Query::Add { index, delta } => tree.add(index, delta)?,
            Query::Sum { left, right } => results.push(tree.range_sum(left, right)?),
        }
    }

    Ok(results)
}
