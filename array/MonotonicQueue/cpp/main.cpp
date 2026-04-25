#include "MonotonicQueue.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

namespace {
bool ReadInput(const string& inputPath, vector<long long>& values, int& windowSize) {
    ifstream input(inputPath);
    if (!input) {
        cerr << "Failed to open input file: " << inputPath << '\n';
        return false;
    }

    int n = 0;
    if (!(input >> n >> windowSize) || n <= 0 || windowSize <= 0 || windowSize > n) {
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

    string extraToken;
    if (input >> extraToken) {
        cerr << "Input size does not match header.\n";
        return false;
    }

    return true;
}

void PrintAnswer(const vector<long long>& maxima) {
    cout << "Window maxima:";
    for (long long value : maxima) {
        cout << ' ' << value;
    }
    cout << '\n';
}
}  // namespace

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool timeMonotonicQueue = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-monotonic-queue") {
            timeMonotonicQueue = true;
        } else {
            inputPath = argument;
        }
    }

    vector<long long> values;
    int windowSize = 0;
    if (!ReadInput(inputPath, values, windowSize)) {
        return 1;
    }

    const auto start = chrono::steady_clock::now();
    const vector<long long> maxima = SlidingWindowMaximum(values, windowSize);
    const auto end = chrono::steady_clock::now();

    if (timeMonotonicQueue) {
        const chrono::duration<double, milli> elapsed = end - start;
        cout << "Monotonic-queue time: " << elapsed.count() << " ms\n";
    } else {
        PrintAnswer(maxima);
    }

    return 0;
}
