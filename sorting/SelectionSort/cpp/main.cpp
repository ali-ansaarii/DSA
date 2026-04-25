#include "SelectionSort.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using namespace std;

namespace {
vector<int> readInput(const string& inputPath) {
    ifstream input(inputPath);
    if (!input) {
        throw runtime_error("failed to open input file: " + inputPath);
    }

    int n = 0;
    if (!(input >> n)) {
        throw runtime_error("input must start with the array length");
    }
    if (n < 0) {
        throw runtime_error("array length must be non-negative");
    }

    vector<int> values;
    values.reserve(static_cast<size_t>(n));
    for (int i = 0; i < n; ++i) {
        int value = 0;
        if (!(input >> value)) {
            throw runtime_error("input ended before reading all array values");
        }
        values.push_back(value);
    }

    return values;
}

void printValues(const vector<int>& values) {
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
    bool time_flag_time_selection_sort = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-selection-sort") {
            time_flag_time_selection_sort = true;
        } else {
            inputPath = argument;
        }
    }

    try {
        vector<int> values = readInput(inputPath);

        if (time_flag_time_selection_sort) {
            const auto start = chrono::steady_clock::now();
            selectionSort(values);
            const auto end = chrono::steady_clock::now();
            const chrono::duration<double, milli> elapsed = end - start;
            cerr << "algorithm_time_ms=" << elapsed.count() << '\n';
        } else {
            selectionSort(values);
        }

        printValues(values);
    } catch (const exception& error) {
        cerr << "Error: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
