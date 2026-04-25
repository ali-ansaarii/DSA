#include "MergeSort.hpp"

#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>

using namespace std;

namespace {
vector<int64_t> readInput(const string& inputPath) {
    ifstream input(inputPath);
    if (!input) {
        throw runtime_error("failed to open input file: " + inputPath);
    }

    size_t n = 0;
    if (!(input >> n)) {
        throw runtime_error("input must start with the element count");
    }

    vector<int64_t> values;
    values.reserve(n);
    for (size_t i = 0; i < n; ++i) {
        int64_t value = 0;
        if (!(input >> value)) {
            throw runtime_error("input ended before reading all elements");
        }
        values.push_back(value);
    }

    string extra;
    if (input >> extra) {
        throw runtime_error("input contains extra tokens after the declared elements");
    }

    return values;
}

void printValues(const vector<int64_t>& values) {
    for (size_t i = 0; i < values.size(); ++i) {
        if (i > 0) {
            cout << ' ';
        }
        cout << values[i];
    }
    cout << '\n';
}
}  // namespace

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool time_flag_time_merge_sort = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-merge-sort") {
            time_flag_time_merge_sort = true;
        } else {
            inputPath = argument;
        }
    }

    try {
        const vector<int64_t> values = readInput(inputPath);

        vector<int64_t> sorted;
        if (time_flag_time_merge_sort) {
            const auto start = chrono::steady_clock::now();
            sorted = mergeSort(values);
            const auto end = chrono::steady_clock::now();
            const chrono::duration<double> elapsed = end - start;
            cerr << fixed << setprecision(9) << "merge_sort_seconds=" << elapsed.count() << '\n';
        } else {
            sorted = mergeSort(values);
        }

        printValues(sorted);
    } catch (const exception& error) {
        cerr << "Error: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
