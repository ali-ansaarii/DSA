#include "TopologicalSortDFSBased.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

using namespace std;

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool time_flag_time_topological_sort_dfs_based = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-topological-sort-dfs-based") {
            time_flag_time_topological_sort_dfs_based = true;
        } else {
            inputPath = argument;
        }
    }

    ifstream input(inputPath);
    if (!input) {
        cerr << "Failed to open input file: " << inputPath << '\n';
        return 1;
    }

    int vertexCount = 0;
    int edgeCount = 0;
    input >> vertexCount >> edgeCount;
    if (!input || vertexCount < 0 || edgeCount < 0) {
        cerr << "Invalid input header\n";
        return 1;
    }

    vector<pair<int, int>> edges;
    edges.reserve(edgeCount);
    for (int i = 0; i < edgeCount; ++i) {
        int from = 0;
        int to = 0;
        input >> from >> to;
        if (!input) {
            cerr << "Invalid edge at index " << i << '\n';
            return 1;
        }
        edges.emplace_back(from, to);
    }

    TopologicalSortResult result;
    try {
        auto start = chrono::steady_clock::now();
        result = topologicalSortDFSBased(vertexCount, edges);
        auto stop = chrono::steady_clock::now();

        if (time_flag_time_topological_sort_dfs_based) {
            auto elapsed = chrono::duration_cast<chrono::nanoseconds>(stop - start).count();
            cerr << "algorithm_time_ns " << elapsed << '\n';
        }
    } catch (const exception& error) {
        cerr << error.what() << '\n';
        return 1;
    }

    if (result.hasCycle) {
        cout << "CYCLE DETECTED\n";
        return 0;
    }

    cout << "Topological order:\n";
    for (size_t i = 0; i < result.order.size(); ++i) {
        if (i > 0) {
            cout << ' ';
        }
        cout << result.order[i];
    }
    cout << '\n';

    return 0;
}
