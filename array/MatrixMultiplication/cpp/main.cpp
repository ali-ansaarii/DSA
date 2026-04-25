#include "MatrixMultiplication.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

using namespace std;

static Matrix readMatrix(istream& input, size_t rows, size_t cols) {
    Matrix matrix(rows, vector<long long>(cols));
    for (size_t i = 0; i < rows; ++i) {
        for (size_t j = 0; j < cols; ++j) {
            if (!(input >> matrix[i][j])) {
                throw runtime_error("failed to read matrix value");
            }
        }
    }
    return matrix;
}

static void printMatrix(const Matrix& matrix) {
    const size_t rows = matrix.size();
    const size_t cols = rows == 0 ? 0 : matrix.front().size();

    cout << rows << ' ' << cols << '\n';
    for (size_t i = 0; i < rows; ++i) {
        for (size_t j = 0; j < cols; ++j) {
            if (j > 0) {
                cout << ' ';
            }
            cout << matrix[i][j];
        }
        cout << '\n';
    }
}

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool timeMatrixMultiplication = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-matrix-multiplication") {
            timeMatrixMultiplication = true;
        } else {
            inputPath = argument;
        }
    }

    try {
        ifstream input(inputPath);
        if (!input) {
            throw runtime_error("failed to open input file: " + inputPath);
        }

        size_t m = 0;
        size_t n = 0;
        size_t n2 = 0;
        size_t p = 0;

        if (!(input >> m >> n)) {
            throw runtime_error("failed to read first matrix dimensions");
        }
        Matrix left = readMatrix(input, m, n);

        if (!(input >> n2 >> p)) {
            throw runtime_error("failed to read second matrix dimensions");
        }
        if (n != n2) {
            throw runtime_error("matrix dimensions are incompatible");
        }
        Matrix right = readMatrix(input, n2, p);

        const auto start = chrono::steady_clock::now();
        Matrix result = multiplyMatrices(left, right);
        const auto finish = chrono::steady_clock::now();

        if (timeMatrixMultiplication) {
            const chrono::duration<double, milli> elapsed = finish - start;
            cerr << "matrix_multiplication_ms=" << elapsed.count() << '\n';
        }

        printMatrix(result);
    } catch (const exception& error) {
        cerr << "error: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
