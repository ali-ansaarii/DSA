#include "SlidingWindow.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

namespace {
bool ReadInput(const string& inputPath, vector<long long>& values, int& k) {
    ifstream input(inputPath);
    if (!input) {
        cerr << "Failed to open input file: " << inputPath << '\n';
        return false;
    }

    int n = 0;
    if (!(input >> n >> k) || n <= 0 || k <= 0 || k > n) {
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

    return true;
}
}  // namespace

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool timeFixedWindow = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-fixed-window") {
            timeFixedWindow = true;
        } else {
            inputPath = argument;
        }
    }

    vector<long long> values;
    int k = 0;
    if (!ReadInput(inputPath, values, k)) {
        return 1;
    }

    long long bestSum = 0;
    int bestLeft = 0;
    int bestRight = 0;

    const auto start = chrono::steady_clock::now();
    if (!BestFixedWindow(values, k, bestSum, bestLeft, bestRight)) {
        cerr << "Overflow while evaluating fixed-size windows.\n";
        return 1;
    }
    const auto end = chrono::steady_clock::now();

    if (timeFixedWindow) {
        const chrono::duration<double, milli> elapsed = end - start;
        cout << "Fixed-window time: " << elapsed.count() << " ms\n";
    } else {
        cout << "Best window sum: " << bestSum << '\n';
        cout << "Best window range: " << bestLeft << ' ' << bestRight << '\n';
    }

    return 0;
}
