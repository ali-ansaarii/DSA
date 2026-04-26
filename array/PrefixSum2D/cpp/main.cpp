#include "PrefixSum2D.hpp"

#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool time_flag_time_prefix_sum_2d = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-prefix-sum-2d") {
            time_flag_time_prefix_sum_2d = true;
        } else {
            inputPath = argument;
        }
    }

    ifstream input(inputPath);
    if (!input) {
        cerr << "Failed to open input file: " << inputPath << '\n';
        return 1;
    }

    int rows = 0;
    int cols = 0;
    input >> rows >> cols;

    vector<vector<long long>> matrix(rows, vector<long long>(cols));
    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < cols; ++c) {
            input >> matrix[r][c];
        }
    }

    int query_count = 0;
    input >> query_count;
    vector<RectQuery> queries(query_count);
    for (int i = 0; i < query_count; ++i) {
        input >> queries[i].r1 >> queries[i].c1 >> queries[i].r2 >> queries[i].c2;
    }

    const auto start = chrono::steady_clock::now();
    vector<long long> answers = answer_rectangle_queries(matrix, queries);
    const auto stop = chrono::steady_clock::now();

    if (time_flag_time_prefix_sum_2d) {
        const chrono::duration<double, milli> elapsed = stop - start;
        cerr << fixed << setprecision(3)
             << "algorithm_time_ms " << elapsed.count() << '\n';
    }

    for (long long answer : answers) {
        cout << answer << '\n';
    }

    return 0;
}
