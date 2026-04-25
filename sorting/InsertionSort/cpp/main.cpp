#include "InsertionSort.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using namespace std;

namespace {

vector<long long> readInput(const string& inputPath) {
    ifstream input(inputPath);
    if (!input) {
        throw runtime_error("failed to open input file: " + inputPath);
    }

    long long nValue = 0;
    if (!(input >> nValue)) {
        throw runtime_error("input must start with the number of elements");
    }
    if (nValue < 0) {
        throw runtime_error("number of elements must be nonnegative");
    }

    const size_t n = static_cast<size_t>(nValue);
    vector<long long> values;
    values.reserve(n);

    for (size_t i = 0; i < n; ++i) {
        long long value = 0;
        if (!(input >> value)) {
            throw runtime_error("input ended before all elements were read");
        }
        values.push_back(value);
    }

    return values;
}

void printValues(const vector<long long>& values) {
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
    bool time_flag_time_insertion_sort = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-insertion-sort") {
            time_flag_time_insertion_sort = true;
        } else {
            inputPath = argument;
        }
    }

    try {
        vector<long long> values = readInput(inputPath);

        if (time_flag_time_insertion_sort) {
            const auto start = chrono::steady_clock::now();
            insertionSort(values);
            const auto end = chrono::steady_clock::now();
            const auto elapsed = chrono::duration_cast<chrono::microseconds>(end - start).count();
            cerr << "algorithm_time_microseconds=" << elapsed << '\n';
        } else {
            insertionSort(values);
        }

        printValues(values);
    } catch (const exception& error) {
        cerr << "error: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
