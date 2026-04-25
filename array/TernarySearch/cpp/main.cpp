#include "TernarySearch.hpp"

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

    size_t n = 0;
    input >> n;
    if (!input || n == 0) {
        throw runtime_error("input must start with a positive element count");
    }

    vector<long long> values(n);
    for (size_t i = 0; i < n; ++i) {
        if (!(input >> values[i])) {
            throw runtime_error("input ended before all array values were read");
        }
    }

    return values;
}
}  // namespace

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool timeTernarySearch = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-ternary-search") {
            timeTernarySearch = true;
        } else {
            inputPath = argument;
        }
    }

    try {
        const vector<long long> values = readInput(inputPath);

        TernarySearchResult result{};
        long long elapsedNanoseconds = 0;
        if (timeTernarySearch) {
            const auto start = chrono::steady_clock::now();
            result = findUnimodalMaximum(values);
            const auto stop = chrono::steady_clock::now();
            elapsedNanoseconds = chrono::duration_cast<chrono::nanoseconds>(stop - start).count();
        } else {
            result = findUnimodalMaximum(values);
        }

        cout << "Maximum index: " << result.index << '\n';
        cout << "Maximum value: " << result.value << '\n';
        if (timeTernarySearch) {
            cout << "Algorithm time (ns): " << elapsedNanoseconds << '\n';
        }
    } catch (const exception& error) {
        cerr << "Error: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
