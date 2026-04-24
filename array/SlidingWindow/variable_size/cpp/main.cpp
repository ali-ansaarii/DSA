#include "SlidingWindow.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

namespace {
bool ReadInput(const string& inputPath, vector<long long>& values, long long& target) {
    ifstream input(inputPath);
    if (!input) {
        cerr << "Failed to open input file: " << inputPath << '\n';
        return false;
    }

    int n = 0;
    if (!(input >> n >> target) || n <= 0 || target <= 0) {
        cerr << "Invalid input header.\n";
        return false;
    }

    values.assign(n, 0);
    for (int i = 0; i < n; ++i) {
        if (!(input >> values[i])) {
            cerr << "Failed to read array value at index " << i << ".\n";
            return false;
        }
        if (values[i] <= 0) {
            cerr << "Variable-size sliding window requires positive values.\n";
            return false;
        }
    }

    return true;
}
}  // namespace

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool timeVariableWindow = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-variable-window") {
            timeVariableWindow = true;
        } else {
            inputPath = argument;
        }
    }

    vector<long long> values;
    long long target = 0;
    if (!ReadInput(inputPath, values, target)) {
        return 1;
    }

    int bestLength = -1;
    int bestLeft = -1;
    int bestRight = -1;

    const auto start = chrono::steady_clock::now();
    if (!MinWindowAtLeastTarget(values, target, bestLength, bestLeft, bestRight)) {
        cerr << "Overflow while evaluating variable-size windows.\n";
        return 1;
    }
    const auto end = chrono::steady_clock::now();

    if (timeVariableWindow) {
        const chrono::duration<double, milli> elapsed = end - start;
        cout << "Variable-window time: " << elapsed.count() << " ms\n";
    } else if (bestLength == -1) {
        cout << "No valid window\n";
    } else {
        cout << "Minimum window length: " << bestLength << '\n';
        cout << "Minimum window range: " << bestLeft << ' ' << bestRight << '\n';
    }

    return 0;
}
