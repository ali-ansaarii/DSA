#include "Dijkstra.hpp"

#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main(int argc, char* argv[]) {
    string inputPath = "input.txt";
    bool timeDijkstra = false;

    for (int i = 1; i < argc; ++i) {
        const string arg = argv[i];
        if (arg == "--time-dijkstra") {
            timeDijkstra = true;
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

    vector<vector<pair<int, long long>>> graph(n);
    for (int i = 0; i < m; ++i) {
        int u = 0;
        int v = 0;
        long long w = 0;
        if (!(input >> u >> v >> w) || u < 0 || u >= n || v < 0 || v >= n || w < 0) {
            cerr << "Invalid weighted edge at line " << (i + 2) << '\n';
            return 1;
        }

        graph[u].push_back({v, w});
        graph[v].push_back({u, w});
    }

    int start = 0;
    if (!(input >> start) || start < 0 || start >= n) {
        cerr << "Invalid start node. Expected a node in [0, n)." << '\n';
        return 1;
    }

    for (auto& neighbors : graph) {
        ranges::sort(neighbors);
    }

    DijkstraResult result;
    const auto dijkstraStart = chrono::steady_clock::now();
    try {
        result = Dijkstra(graph, start);
    } catch (const DijkstraOverflowError& error) {
        cerr << error.what() << '\n';
        return 1;
    }
    const auto dijkstraEnd = chrono::steady_clock::now();
    const auto dijkstraDuration = chrono::duration_cast<chrono::microseconds>(dijkstraEnd - dijkstraStart);

    size_t reachableNodes = 0;
    for (const bool isReachable : result.reachable) {
        if (isReachable) {
            ++reachableNodes;
        }
    }

    if (timeDijkstra) {
        cout << "Reachable nodes: " << reachableNodes << '\n';
        cout << "Dijkstra call time (ms): " << (dijkstraDuration.count() / 1000.0) << '\n';
    } else {
        cout << "Shortest distances from " << start << ':';
        for (size_t i = 0; i < result.distances.size(); ++i) {
            if (!result.reachable[i]) {
                cout << " INF";
            } else {
                cout << ' ' << result.distances[i];
            }
        }
        cout << '\n';
    }

    return 0;
}
