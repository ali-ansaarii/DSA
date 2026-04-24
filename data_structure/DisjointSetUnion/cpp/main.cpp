#include "DisjointSetUnion.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static bool IsValidElement(int element, int n) {
    return element >= 0 && element < n;
}

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool timeDsu = false;

    for (int i = 1; i < argc; ++i) {
        const string arg = argv[i];
        if (arg == "--time-dsu") {
            timeDsu = true;
        } else {
            inputPath = arg;
        }
    }

    ifstream input(inputPath);
    if (!input) {
        cerr << "Failed to open input file: " << inputPath << '\n';
        return 1;
    }

    int n = 0;
    int q = 0;
    if (!(input >> n >> q) || n <= 0 || q < 0) {
        cerr << "Invalid DSU header. Expected: n q" << '\n';
        return 1;
    }

    vector<Operation> operations;
    operations.reserve(q);

    for (int line = 0; line < q; ++line) {
        string op;
        if (!(input >> op)) {
            cerr << "Input ended early. Expected " << q << " operations." << '\n';
            return 1;
        }

        if (op == "union" || op == "connected") {
            int a = -1;
            int b = -1;
            if (!(input >> a >> b) || !IsValidElement(a, n) || !IsValidElement(b, n)) {
                cerr << "Invalid operation at line " << (line + 2) << '\n';
                return 1;
            }

            operations.push_back({op == "union" ? OperationType::Union : OperationType::Connected, a, b});
        } else if (op == "find") {
            int a = -1;
            if (!(input >> a) || !IsValidElement(a, n)) {
                cerr << "Invalid operation at line " << (line + 2) << '\n';
                return 1;
            }

            operations.push_back({OperationType::Find, a, -1});
        } else {
            cerr << "Invalid operation at line " << (line + 2) << '\n';
            return 1;
        }
    }

    const auto dsuStart = chrono::steady_clock::now();
    const vector<string> queryResults = DisjointSetUnion(n, operations);
    const auto dsuEnd = chrono::steady_clock::now();
    const auto dsuDuration = chrono::duration_cast<chrono::microseconds>(dsuEnd - dsuStart);

    if (timeDsu) {
        cout << "Processed operations: " << operations.size() << '\n';
        cout << "DisjointSetUnion call time (ms): " << (dsuDuration.count() / 1000.0) << '\n';
    } else {
        cout << "Query results:" << '\n';
        for (const string& result : queryResults) {
            cout << result << '\n';
        }
    }

    return 0;
}
