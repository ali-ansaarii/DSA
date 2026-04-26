#include "ShortestPathInDAG.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

using namespace std;

static void printDistances(const vector<long long>& distances) {
    for (size_t i = 0; i < distances.size(); ++i) {
        if (i > 0) {
            cout << ' ';
        }
        if (distances[i] == DAG_INF) {
            cout << "INF";
        } else {
            cout << distances[i];
        }
    }
    cout << '\n';
}

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool time_flag_time_shortest_path_in_dag = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-shortest-path-in-dag") {
            time_flag_time_shortest_path_in_dag = true;
        } else {
            inputPath = argument;
        }
    }

    ifstream input(inputPath);
    if (!input) {
        cerr << "failed to open input file: " << inputPath << '\n';
        return 1;
    }

    int vertexCount = 0;
    int edgeCount = 0;
    int source = 0;
    input >> vertexCount >> edgeCount >> source;
    if (!input || vertexCount < 0 || edgeCount < 0) {
        cerr << "invalid input header\n";
        return 1;
    }

    vector<Edge> edges;
    edges.reserve(edgeCount);
    for (int i = 0; i < edgeCount; ++i) {
        Edge edge{};
        input >> edge.from >> edge.to >> edge.weight;
        if (!input) {
            cerr << "invalid edge line at index " << i << '\n';
            return 1;
        }
        edges.push_back(edge);
    }

    try {
        vector<long long> distances;
        if (time_flag_time_shortest_path_in_dag) {
            const auto start = chrono::steady_clock::now();
            distances = shortestPathInDAG(vertexCount, edges, source);
            const auto end = chrono::steady_clock::now();
            const chrono::duration<double, milli> elapsed = end - start;
            cerr << "algorithm_ms " << elapsed.count() << '\n';
        } else {
            distances = shortestPathInDAG(vertexCount, edges, source);
        }
        printDistances(distances);
    } catch (const exception& error) {
        cerr << error.what() << '\n';
        return 1;
    }

    return 0;
}
