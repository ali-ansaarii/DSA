#[derive(Clone, Copy)]
pub enum Query {
    Add { index: usize, delta: i64 },
    Sum { left: usize, right: usize },
}

pub struct FenwickTree {
    tree: Vec<i64>,
}

impl FenwickTree {
    pub fn new(size: usize) -> Self {
        Self { tree: vec![0; size + 1] }
    }

    pub fn add(&mut self, index: usize, delta: i64) -> Result<(), String> {
        let mut i = index + 1;
        while i < self.tree.len() {
            self.tree[i] = self.tree[i]
                .checked_add(delta)
                .ok_or_else(|| String::from("Fenwick tree overflowed while applying an update."))?;
            i += i & (!i + 1);
        }
        Ok(())
    }

    pub fn prefix_sum(&self, index: usize) -> Result<i64, String> {
        let mut result = 0_i64;
        let mut i = index + 1;
        while i > 0 {
            result = result
                .checked_add(self.tree[i])
                .ok_or_else(|| String::from("Fenwick tree overflowed while evaluating a sum query."))?;
            i -= i & (!i + 1);
        }
        Ok(result)
    }

    pub fn range_sum(&self, left: usize, right: usize) -> Result<i64, String> {
        let right_prefix = self.prefix_sum(right)?;
        if left == 0 {
            return Ok(right_prefix);
        }
        let left_prefix = self.prefix_sum(left - 1)?;
        right_prefix
            .checked_sub(left_prefix)
            .ok_or_else(|| String::from("Fenwick tree overflowed while evaluating a sum query."))
    }
}

pub fn process_fenwick_queries(initial_values: &[i64], queries: &[Query]) -> Result<Vec<i64>, String> {
    let mut tree = FenwickTree::new(initial_values.len());
    for (index, value) in initial_values.iter().enumerate() {
        tree.add(index, *value)
            .map_err(|_| String::from("Fenwick tree overflowed while building the initial state."))?;
    }

    let mut results = Vec::new();
    for query in queries {
        match *query {
            Query::Add { index, delta } => tree.add(index, delta)?,
            Query::Sum { left, right } => results.push(tree.range_sum(left, right)?),
        }
    }

    Ok(results)
}
