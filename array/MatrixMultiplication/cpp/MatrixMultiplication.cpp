#include "MatrixMultiplication.hpp"

#include <stdexcept>

using namespace std;

Matrix multiplyMatrices(const Matrix& left, const Matrix& right) {
    if (left.empty() || right.empty()) {
        throw invalid_argument("matrices must be non-empty");
    }

    const size_t rows = left.size();
    const size_t shared = left.front().size();
    const size_t rightRows = right.size();
    const size_t cols = right.front().size();

    if (shared == 0 || cols == 0 || shared != rightRows) {
        throw invalid_argument("matrix dimensions are incompatible");
    }

    for (const auto& row : left) {
        if (row.size() != shared) {
            throw invalid_argument("left matrix rows have inconsistent lengths");
        }
    }
    for (const auto& row : right) {
        if (row.size() != cols) {
            throw invalid_argument("right matrix rows have inconsistent lengths");
        }
    }

    Matrix result(rows, vector<long long>(cols, 0));
    for (size_t i = 0; i < rows; ++i) {
        for (size_t k = 0; k < shared; ++k) {
            const long long value = left[i][k];
            for (size_t j = 0; j < cols; ++j) {
                result[i][j] += value * right[k][j];
            }
        }
    }
    return result;
}
