#include "MonotonicStack.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

namespace {
bool ReadInput(const string& inputPath, vector<long long>& values) {
    ifstream input(inputPath);
    if (!input) {
        cerr << "Failed to open input file: " << inputPath << '\n';
        return false;
    }

    int n = 0;
    if (!(input >> n) || n <= 0) {
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

void PrintAnswer(const vector<long long>& answer) {
    cout << "Next greater elements:";
    for (long long value : answer) {
        cout << ' ' << value;
    }
    cout << '\n';
}
}  // namespace

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool timeMonotonicStack = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-monotonic-stack") {
            timeMonotonicStack = true;
        } else {
            inputPath = argument;
        }
    }

    vector<long long> values;
    if (!ReadInput(inputPath, values)) {
        return 1;
    }

    const auto start = chrono::steady_clock::now();
    const vector<long long> answer = NextGreaterElements(values);
    const auto end = chrono::steady_clock::now();

    if (timeMonotonicStack) {
        const chrono::duration<double, milli> elapsed = end - start;
        cout << "Monotonic-stack time: " << elapsed.count() << " ms\n";
    } else {
        PrintAnswer(answer);
    }

    return 0;
}
