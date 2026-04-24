#include "BoundarySearch.hpp"

#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

namespace {

enum class BenchmarkMethod {
    None,
    RangeHalving,
    PowersOfTwo,
};

struct ProgramOptions {
    string inputPath;
    BenchmarkMethod method = BenchmarkMethod::None;
};

bool ParseArguments(int argc, char* argv[], ProgramOptions& options) {
    for (int index = 1; index < argc; ++index) {
        const string argument = argv[index];
        if (argument == "--time-range-halving") {
            options.method = BenchmarkMethod::RangeHalving;
        } else if (argument == "--time-powers-of-two") {
            options.method = BenchmarkMethod::PowersOfTwo;
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
        cerr << "Usage: " << argv[0] << " <input-file> [--time-range-halving|--time-powers-of-two]\n";
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

    if (options.method != BenchmarkMethod::None) {
        vector<int> results;
        results.reserve(queryCount);

        const auto begin = chrono::steady_clock::now();
        if (options.method == BenchmarkMethod::RangeHalving) {
            for (const long long query : queries) {
                results.push_back(LowerBoundRangeHalving(values, query));
            }
        } else {
            for (const long long query : queries) {
                results.push_back(LowerBoundPowersOfTwo(values, query));
            }
        }
        const auto end = chrono::steady_clock::now();

        cout << fixed << setprecision(3);
        if (options.method == BenchmarkMethod::RangeHalving) {
            cout << "Boundary search time (range-halving): " << chrono::duration<double, milli>(end - begin).count() << " ms\n";
        } else {
            cout << "Boundary search time (powers-of-two): " << chrono::duration<double, milli>(end - begin).count() << " ms\n";
        }

        return 0;
    }

    vector<int> rangeResults;
    vector<int> powersResults;
    rangeResults.reserve(queryCount);
    powersResults.reserve(queryCount);

    for (const long long query : queries) {
        rangeResults.push_back(LowerBoundRangeHalving(values, query));
        powersResults.push_back(LowerBoundPowersOfTwo(values, query));
    }

    if (rangeResults != powersResults) {
        cerr << "Boundary-search implementations disagree\n";
        return 1;
    }

    cout << "Boundary results (range-halving):";
    for (const int result : rangeResults) {
        cout << ' ' << result;
    }
    cout << '\n';

    cout << "Boundary results (powers-of-two):";
    for (const int result : powersResults) {
        cout << ' ' << result;
    }
    cout << '\n';

    return 0;
}
