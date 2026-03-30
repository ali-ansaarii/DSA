#include "DFS.hpp"

#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main(int argc, char* argv[]) {
    string inputPath = "../inputs/input.txt";
    bool timeDfs = false;

    for (int i = 1; i < argc; ++i) {
        const string arg = argv[i];
        if (arg == "--time-dfs") {
            timeDfs = true;
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
            cerr << "Invalid edge at line " << (i + 2) << '\n';
            return 1;
        }

        // Undirected graph: add both directions.
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    int start = 0;
    if (!(input >> start) || start < 0 || start >= n) {
        cerr << "Invalid start node. Expected a node in [0, n)." << '\n';
        return 1;
    }

    for (auto& neighbors : graph) {
        ranges::sort(neighbors);
    }

    const auto dfsStart = chrono::steady_clock::now();
    const vector<int> traversalOrder = DFS(graph, start);
    const auto dfsEnd = chrono::steady_clock::now();
    const auto dfsDuration = chrono::duration_cast<chrono::microseconds>(dfsEnd - dfsStart);

    if (timeDfs) {
        cout << "DFS visited nodes: " << traversalOrder.size() << '\n';
        cout << "DFS call time (ms): " << (dfsDuration.count() / 1000.0) << '\n';
    } else {
        cout << "DFS traversal order:";
        for (const int node : traversalOrder) {
            cout << ' ' << node;
        }
        cout << '\n';
    }

    return 0;
}
