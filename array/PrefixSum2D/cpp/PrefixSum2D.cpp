#include "PrefixSum2D.hpp"

using namespace std;

PrefixSum2D::PrefixSum2D(const vector<vector<long long>>& matrix) {
    const int rows = static_cast<int>(matrix.size());
    const int cols = rows == 0 ? 0 : static_cast<int>(matrix[0].size());
    prefix_.assign(rows + 1, vector<long long>(cols + 1, 0));

    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < cols; ++c) {
            prefix_[r + 1][c + 1] = matrix[r][c]
                                  + prefix_[r][c + 1]
                                  + prefix_[r + 1][c]
                                  - prefix_[r][c];
        }
    }
}

long long PrefixSum2D::rectangle_sum(int r1, int c1, int r2, int c2) const {
    return prefix_[r2 + 1][c2 + 1]
         - prefix_[r1][c2 + 1]
         - prefix_[r2 + 1][c1]
         + prefix_[r1][c1];
}

vector<long long> answer_rectangle_queries(
    const vector<vector<long long>>& matrix,
    const vector<RectQuery>& queries
) {
    PrefixSum2D prefix_sum(matrix);
    vector<long long> answers;
    answers.reserve(queries.size());

    for (const RectQuery& query : queries) {
        answers.push_back(prefix_sum.rectangle_sum(query.r1, query.c1, query.r2, query.c2));
    }

    return answers;
}
