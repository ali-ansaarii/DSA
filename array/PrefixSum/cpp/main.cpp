#include "PrefixSum.hpp"

#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

namespace {

struct Query {
    int left;
    int right;
};

struct ProgramOptions {
    string inputPath;
    bool benchmarkMode = false;
};

bool ParseArguments(int argc, char* argv[], ProgramOptions& options) {
    for (int index = 1; index < argc; ++index) {
        const string argument = argv[index];
        if (argument == "--time-prefix-sum") {
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
        cerr << "Usage: " << argv[0] << " <input-file> [--time-prefix-sum]\n";
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

    vector<Query> queries(queryCount);
    for (int index = 0; index < queryCount; ++index) {
        if (!(input >> queries[index].left >> queries[index].right)) {
            cerr << "Invalid query at index " << index << '\n';
            return 1;
        }
        if (queries[index].left < 0 || queries[index].right < queries[index].left || queries[index].right >= valueCount) {
            cerr << "Query indices out of range at index " << index << '\n';
            return 1;
        }
    }

    vector<long long> prefix;
    vector<long long> results;
    results.reserve(queryCount);

    const auto begin = chrono::steady_clock::now();
    if (!BuildPrefixSums(values, prefix)) {
        cerr << "Overflow detected while building prefix sums\n";
        return 1;
    }
    for (const Query& query : queries) {
        long long sum = 0;
        if (!RangeSum(prefix, query.left, query.right, sum)) {
            cerr << "Overflow detected while answering a range query\n";
            return 1;
        }
        results.push_back(sum);
    }
    const auto end = chrono::steady_clock::now();

    if (options.benchmarkMode) {
        cout << fixed << setprecision(3);
        cout << "Prefix-sum time: " << chrono::duration<double, milli>(end - begin).count() << " ms\n";
        return 0;
    }

    cout << "Range-sum results:";
    for (const long long result : results) {
        cout << ' ' << result;
    }
    cout << '\n';

    return 0;
}
