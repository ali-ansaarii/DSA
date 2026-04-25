#include "FenwickTree.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

namespace {
bool ReadInput(
    const string& inputPath,
    vector<long long>& initialValues,
    vector<Query>& queries
) {
    ifstream input(inputPath);
    if (!input) {
        cerr << "Failed to open input file: " << inputPath << '\n';
        return false;
    }

    int n = 0;
    int q = 0;
    if (!(input >> n >> q) || n <= 0 || q < 0) {
        cerr << "Invalid input header.\n";
        return false;
    }

    initialValues.assign(n, 0);
    for (int index = 0; index < n; ++index) {
        if (!(input >> initialValues[index])) {
            cerr << "Failed to read initial value at index " << index << ".\n";
            return false;
        }
    }

    queries.clear();
    queries.reserve(q);
    for (int lineIndex = 0; lineIndex < q; ++lineIndex) {
        const int operationLine = n + lineIndex + 2;
        string operation;
        if (!(input >> operation)) {
            cerr << "Input ended early. Expected " << q << " operations.\n";
            return false;
        }

        if (operation == "add") {
            int index = -1;
            long long delta = 0;
            if (!(input >> index >> delta) || index < 0 || index >= n) {
                cerr << "Invalid operation at line " << operationLine << ".\n";
                return false;
            }
            queries.push_back(Query{QueryType::Add, index, -1, delta});
        } else if (operation == "sum") {
            int left = -1;
            int right = -1;
            if (!(input >> left >> right) || left < 0 || right < left || right >= n) {
                cerr << "Invalid operation at line " << operationLine << ".\n";
                return false;
            }
            queries.push_back(Query{QueryType::Sum, left, right, 0});
        } else {
            cerr << "Invalid operation at line " << operationLine << ".\n";
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

void PrintAnswer(const vector<long long>& results) {
    cout << "Query sums:\n";
    for (long long value : results) {
        cout << value << '\n';
    }
}
}  // namespace

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool timeFenwickTree = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-fenwick-tree") {
            timeFenwickTree = true;
        } else {
            inputPath = argument;
        }
    }

    vector<long long> initialValues;
    vector<Query> queries;
    if (!ReadInput(inputPath, initialValues, queries)) {
        return 1;
    }

    string errorMessage;
    const auto start = chrono::steady_clock::now();
    const vector<long long> results = ProcessFenwickQueries(initialValues, queries, errorMessage);
    const auto end = chrono::steady_clock::now();

    if (!errorMessage.empty()) {
        cerr << errorMessage << '\n';
        return 1;
    }

    if (timeFenwickTree) {
        const chrono::duration<double, milli> elapsed = end - start;
        cout << "Fenwick-tree time: " << elapsed.count() << " ms\n";
    } else {
        PrintAnswer(results);
    }

    return 0;
}
