#include "DifferenceArray.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <string>
#include <tuple>
#include <vector>

using namespace std;

namespace {
bool ReadInput(const string& inputPath, vector<long long>& values, vector<tuple<int, int, long long>>& updates) {
    ifstream input(inputPath);
    if (!input) {
        cerr << "Failed to open input file: " << inputPath << '\n';
        return false;
    }

    int n = 0;
    int q = 0;
    if (!(input >> n >> q) || n < 0 || q < 0) {
        cerr << "Invalid input header.\n";
        return false;
    }

    values.assign(n, 0);
    for (int i = 0; i < n; ++i) {
        if (!(input >> values[i])) {
            cerr << "Failed to read array value at index " << i << ".\n";
            return false;
        }
    }

    updates.clear();
    updates.reserve(q);
    for (int i = 0; i < q; ++i) {
        int left = 0;
        int right = 0;
        long long delta = 0;
        if (!(input >> left >> right >> delta)) {
            cerr << "Failed to read update " << i << ".\n";
            return false;
        }
        if (left < 0 || right < left || right >= n) {
            cerr << "Invalid update range at update " << i << ".\n";
            return false;
        }
        updates.emplace_back(left, right, delta);
    }

    return true;
}

bool RunDifferenceArray(const vector<long long>& inputValues,
                        const vector<tuple<int, int, long long>>& updates,
                        vector<long long>& finalValues) {
    vector<long long> diff;
    if (!BuildDifferenceArray(inputValues, diff)) {
        cerr << "Overflow while building the difference array.\n";
        return false;
    }

    for (const auto& [left, right, delta] : updates) {
        if (!ApplyRangeAdd(diff, left, right, delta)) {
            cerr << "Overflow while applying a range update.\n";
            return false;
        }
    }

    if (!ReconstructValues(diff, finalValues)) {
        cerr << "Overflow while reconstructing the final array.\n";
        return false;
    }
    return true;
}

void PrintValues(const vector<long long>& values) {
    cout << "Final array:";
    for (long long value : values) {
        cout << ' ' << value;
    }
    cout << '\n';
}
}  // namespace

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool timeDifferenceArray = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-difference-array") {
            timeDifferenceArray = true;
        } else {
            inputPath = argument;
        }
    }

    vector<long long> values;
    vector<tuple<int, int, long long>> updates;
    if (!ReadInput(inputPath, values, updates)) {
        return 1;
    }

    vector<long long> finalValues;
    const auto start = chrono::steady_clock::now();
    if (!RunDifferenceArray(values, updates, finalValues)) {
        return 1;
    }
    const auto end = chrono::steady_clock::now();

    if (timeDifferenceArray) {
        const chrono::duration<double, milli> elapsed = end - start;
        cout << "Difference-array time: " << elapsed.count() << " ms\n";
    } else {
        PrintValues(finalValues);
    }

    return 0;
}
