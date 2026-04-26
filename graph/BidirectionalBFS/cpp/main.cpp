#include "BidirectionalBFS.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <string>

using namespace std;

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool time_flag_time_bidirectional_bfs = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-bidirectional-bfs") {
            time_flag_time_bidirectional_bfs = true;
        } else {
            inputPath = argument;
        }
    }

    ifstream input(inputPath);
    if (!input) {
        cerr << "failed to open input file: " << inputPath << '\n';
        return 1;
    }

    int n = 0;
    int m = 0;
    input >> n >> m;
    if (!input || n < 0 || m < 0) {
        cerr << "invalid graph header\n";
        return 1;
    }

    vector<vector<int>> graph(n);
    for (int i = 0; i < m; ++i) {
        int u = 0;
        int v = 0;
        input >> u >> v;
        if (!input || u < 0 || v < 0 || u >= n || v >= n) {
            cerr << "invalid edge at index " << i << '\n';
            return 1;
        }
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    int source = 0;
    int target = 0;
    input >> source >> target;
    if (!input || source < 0 || target < 0 || source >= n || target >= n) {
        cerr << "invalid source/target query\n";
        return 1;
    }

    BidirectionalBFSResult result;
    if (time_flag_time_bidirectional_bfs) {
        const auto start = chrono::steady_clock::now();
        result = shortestPathBidirectionalBFS(graph, source, target);
        const auto end = chrono::steady_clock::now();
        cerr << "algorithm_time_ns: "
             << chrono::duration_cast<chrono::nanoseconds>(end - start).count()
             << '\n';
    } else {
        result = shortestPathBidirectionalBFS(graph, source, target);
    }

    cout << "distance: " << result.distance << '\n';
    cout << "path:";
    for (const int vertex : result.path) {
        cout << ' ' << vertex;
    }
    cout << '\n';

    return 0;
}
