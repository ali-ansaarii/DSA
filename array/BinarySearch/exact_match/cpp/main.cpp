#include "BinarySearchExact.hpp"

#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

namespace {

struct ProgramOptions {
    string inputPath;
    bool benchmarkMode = false;
};

bool ParseArguments(int argc, char* argv[], ProgramOptions& options) {
    for (int index = 1; index < argc; ++index) {
        const string argument = argv[index];
        if (argument == "--time-exact") {
            options.benchmarkMode = true;
        } else if (options.inputPath.empty()) {
            options.inputPath = argument;
        } else {
            return false;
        }
    }

    return !options.inputPath.empty();
}

}  // namespace

int main(int argc, char* argv[]) {
    ProgramOptions options;
    if (!ParseArguments(argc, argv, options)) {
        cerr << "Usage: " << argv[0] << " <input-file> [--time-exact]\n";
        return 1;
    }

    ifstream input(options.inputPath);
    if (!input) {
        cerr << "Failed to open input file: " << options.inputPath << '\n';
        return 1;
    }

    int valueCount = 0;
    int queryCount = 0;
    if (!(input >> valueCount >> queryCount) || valueCount < 0 || queryCount < 0) {
        cerr << "Invalid input header\n";
        return 1;
    }

    vector<long long> values(valueCount);
    for (int index = 0; index < valueCount; ++index) {
        if (!(input >> values[index])) {
            cerr << "Invalid array value at index " << index << '\n';
            return 1;
        }
    }

    vector<long long> queries(queryCount);
    for (int index = 0; index < queryCount; ++index) {
        if (!(input >> queries[index])) {
            cerr << "Invalid query at index " << index << '\n';
            return 1;
        }
    }

    vector<int> results;
    results.reserve(queryCount);

    const auto begin = chrono::steady_clock::now();
    for (const long long query : queries) {
        results.push_back(BinarySearchExact(values, query));
    }
    const auto end = chrono::steady_clock::now();

    if (options.benchmarkMode) {
        cout << fixed << setprecision(3);
        cout << "Exact binary search time: " << chrono::duration<double, milli>(end - begin).count() << " ms\n";
        return 0;
    }

    cout << "Exact-match results:";
    for (const int result : results) {
        cout << ' ' << result;
    }
    cout << '\n';

    return 0;
}
