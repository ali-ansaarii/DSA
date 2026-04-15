#include "TopologicalSort.hpp"

#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool timeTopologicalSort = false;

    for (int i = 1; i < argc; ++i) {
        const string arg = argv[i];
        if (arg == "--time-toposort") {
            timeTopologicalSort = true;
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
    int m = 0;
    if (!(input >> n >> m) || n <= 0 || m < 0) {
        cerr << "Invalid graph header. Expected: n m" << '\n';
        return 1;
    }

    vector<vector<int>> graph(n);
    for (int i = 0; i < m; ++i) {
        int u = 0;
        int v = 0;
        if (!(input >> u >> v) || u < 0 || u >= n || v < 0 || v >= n) {
            cerr << "Invalid directed edge at line " << (i + 2) << '\n';
            return 1;
        }

        graph[u].push_back(v);
    }

    for (auto& neighbors : graph) {
        sort(neighbors.begin(), neighbors.end());
    }

    const auto topologicalSortStart = chrono::steady_clock::now();
    const vector<int> order = TopologicalSort(graph);
    const auto topologicalSortEnd = chrono::steady_clock::now();
    const auto topologicalSortDuration =
        chrono::duration_cast<chrono::microseconds>(topologicalSortEnd - topologicalSortStart);

    if (timeTopologicalSort) {
        cout << "Processed nodes: " << order.size() << '\n';
        cout << "TopologicalSort call time (ms): " << (topologicalSortDuration.count() / 1000.0) << '\n';
    }

    if (order.size() != graph.size()) {
        cerr << "Cycle detected. Topological sort requires a DAG." << '\n';
        return 1;
    }

    if (!timeTopologicalSort) {
        cout << "Topological order:";
        for (const int node : order) {
            cout << ' ' << node;
        }
        cout << '\n';
    }

    return 0;
}
