#include "Kadane.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using namespace std;

vector<long long> readInput(const string& inputPath) {
    ifstream input(inputPath);
    if (!input) {
        throw runtime_error("failed to open input file: " + inputPath);
    }

    long long n_value = 0;
    if (!(input >> n_value) || n_value <= 0) {
        throw runtime_error("input must start with a positive element count");
    }

    vector<long long> values;
    values.reserve(static_cast<size_t>(n_value));

    for (long long i = 0; i < n_value; ++i) {
        long long value = 0;
        if (!(input >> value)) {
            throw runtime_error("input ended before all array values were read");
        }
        values.push_back(value);
    }

    string extra;
    if (input >> extra) {
        throw runtime_error("input contains more values than declared by n");
    }

    return values;
}

void printResult(const KadaneResult& result, const vector<long long>& values) {
    cout << "maximum_sum: " << result.maximum_sum << '\n';
    cout << "start_index: " << result.start_index << '\n';
    cout << "end_index: " << result.end_index << '\n';
    cout << "subarray:";
    for (size_t i = result.start_index; i <= result.end_index; ++i) {
        cout << ' ' << values[i];
    }
    cout << '\n';
}

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool time_kadane = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-kadane") {
            time_kadane = true;
        } else {
            inputPath = argument;
        }
    }

    try {
        const vector<long long> values = readInput(inputPath);

        KadaneResult result{};
        long long elapsed_ns = 0;
        if (time_kadane) {
            const auto start = chrono::steady_clock::now();
            result = maxSubarrayKadane(values);
            const auto end = chrono::steady_clock::now();
            elapsed_ns = chrono::duration_cast<chrono::nanoseconds>(end - start).count();
        } else {
            result = maxSubarrayKadane(values);
        }

        printResult(result, values);
        if (time_kadane) {
            cout << "algorithm_time_ns: " << elapsed_ns << '\n';
        }
    } catch (const exception& error) {
        cerr << "error: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
