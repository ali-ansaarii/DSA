#[derive(Clone, Copy)]
pub struct RectQuery {
    pub r1: usize,
    pub c1: usize,
    pub r2: usize,
    pub c2: usize,
}

pub struct PrefixSum2D {
    prefix: Vec<Vec<i64>>,
}

impl PrefixSum2D {
    pub fn new(matrix: &[Vec<i64>]) -> Self {
        let rows = matrix.len();
        let cols = if rows == 0 { 0 } else { matrix[0].len() };
        let mut prefix = vec![vec![0_i64; cols + 1]; rows + 1];

        for r in 0..rows {
            for c in 0..cols {
                prefix[r + 1][c + 1] = matrix[r][c]
                    + prefix[r][c + 1]
                    + prefix[r + 1][c]
                    - prefix[r][c];
            }
        }

        Self { prefix }
    }

    pub fn rectangle_sum(&self, r1: usize, c1: usize, r2: usize, c2: usize) -> i64 {
        self.prefix[r2 + 1][c2 + 1]
            - self.prefix[r1][c2 + 1]
            - self.prefix[r2 + 1][c1]
            + self.prefix[r1][c1]
    }
}

pub fn answer_rectangle_queries(matrix: &[Vec<i64>], queries: &[RectQuery]) -> Vec<i64> {
    let prefix_sum = PrefixSum2D::new(matrix);
    queries
        .iter()
        .map(|query| prefix_sum.rectangle_sum(query.r1, query.c1, query.r2, query.c2))
        .collect()
}
