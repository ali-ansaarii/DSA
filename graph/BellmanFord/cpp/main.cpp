#include "BellmanFord.hpp"

#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

namespace {

struct ProgramOptions {
    string inputPath;
    bool benchmarkMode = false;
};

bool ParseArguments(int argc, char* argv[], ProgramOptions& options) {
    for (int index = 1; index < argc; ++index) {
        string argument = argv[index];
        if (argument == "--time-bellman-ford") {
            options.benchmarkMode = true;
        } else if (options.inputPath.empty()) {
            options.inputPath = argument;
        } else {
            return false;
        }
    }

    return !options.inputPath.empty();
}

void PrintDistances(const vector<optional<long long>>& distances, int start) {
    cout << "Shortest distances from " << start << ":";
    for (const auto& distance : distances) {
        cout << ' ';
        if (distance.has_value()) {
            cout << *distance;
        } else {
            cout << "INF";
        }
    }
    cout << '\n';
}

}  // namespace

int main(int argc, char* argv[]) {
    ProgramOptions options;
    if (!ParseArguments(argc, argv, options)) {
        cerr << "Usage: " << argv[0] << " <input-file> [--time-bellman-ford]\n";
        return 1;
    }

    ifstream input(options.inputPath);
    if (!input) {
        cerr << "Failed to open input file: " << options.inputPath << '\n';
        return 1;
    }

    int nodeCount = 0;
    int edgeCount = 0;
    if (!(input >> nodeCount >> edgeCount) || nodeCount <= 0 || edgeCount < 0) {
        cerr << "Invalid graph header\n";
        return 1;
    }

    vector<Edge> edges;
    edges.reserve(edgeCount);

    for (int index = 0; index < edgeCount; ++index) {
        Edge edge{};
        if (!(input >> edge.from >> edge.to >> edge.weight)) {
            cerr << "Invalid edge at index " << index << '\n';
            return 1;
        }

        if (edge.from < 0 || edge.from >= nodeCount || edge.to < 0 || edge.to >= nodeCount) {
            cerr << "Edge node out of range at index " << index << '\n';
            return 1;
        }

        edges.push_back(edge);
    }

    int start = 0;
    if (!(input >> start) || start < 0 || start >= nodeCount) {
        cerr << "Invalid start node\n";
        return 1;
    }

    const auto begin = chrono::steady_clock::now();
    const BellmanFordResult result = BellmanFord(nodeCount, edges, start);
    const auto end = chrono::steady_clock::now();
    const chrono::duration<double, milli> elapsed = end - begin;

    if (options.benchmarkMode) {
        cout << fixed << setprecision(3);
        cout << "Bellman-Ford time: " << elapsed.count() << " ms\n";
    }

    if (result.status == BellmanFordStatus::Overflow) {
        cerr << "Overflow detected while relaxing edges\n";
        return 1;
    }

    if (result.status == BellmanFordStatus::NegativeCycle) {
        cout << "Negative cycle reachable from " << start << '\n';
        return 0;
    }

    if (!options.benchmarkMode) {
        PrintDistances(result.distances, start);
    }

    return 0;
}
