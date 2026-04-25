#include "BinarySearchOnAnswer.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using namespace std;

struct ProblemInput {
    int n;
    int k;
    vector<long long> values;
};

ProblemInput readInput(const string& inputPath) {
    ifstream input(inputPath);
    if (!input) {
        throw runtime_error("Unable to open input file: " + inputPath);
    }

    ProblemInput data{};
    if (!(input >> data.n >> data.k)) {
        throw runtime_error("Input must start with n and k");
    }
    if (data.n < 0) {
        throw runtime_error("n must be non-negative");
    }

    data.values.resize(static_cast<size_t>(data.n));
    for (int i = 0; i < data.n; ++i) {
        if (!(input >> data.values[static_cast<size_t>(i)])) {
            throw runtime_error("Input ended before reading all array values");
        }
    }

    return data;
}

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool time_flag_time_binary_search_on_answer = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-binary-search-on-answer") {
            time_flag_time_binary_search_on_answer = true;
        } else {
            inputPath = argument;
        }
    }

    try {
        ProblemInput data = readInput(inputPath);

        long long answer = 0;
        if (time_flag_time_binary_search_on_answer) {
            auto start = chrono::steady_clock::now();
            answer = minimizeLargestGroupSum(data.values, data.k);
            auto end = chrono::steady_clock::now();
            auto elapsedNs = chrono::duration_cast<chrono::nanoseconds>(end - start).count();
            cerr << "algorithm_time_ns " << elapsedNs << '\n';
        } else {
            answer = minimizeLargestGroupSum(data.values, data.k);
        }

        cout << answer << '\n';
    } catch (const exception& error) {
        cerr << "Error: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
