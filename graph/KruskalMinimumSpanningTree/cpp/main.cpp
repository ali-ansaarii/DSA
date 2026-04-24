#include "KruskalMST.hpp"

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
        if (argument == "--time-kruskal") {
            options.benchmarkMode = true;
        } else if (options.inputPath.empty()) {
            options.inputPath = argument;
        } else {
            return false;
        }
    }

    return !options.inputPath.empty();
}

void PrintResult(const KruskalResult& result) {
    cout << "MST total weight: " << result.totalWeight << '\n';
    cout << "MST edges:\n";
    for (const Edge& edge : result.chosenEdges) {
        cout << edge.from << ' ' << edge.to << ' ' << edge.weight << '\n';
    }
}

}  // namespace

int main(int argc, char* argv[]) {
    ProgramOptions options;
    if (!ParseArguments(argc, argv, options)) {
        cerr << "Usage: " << argv[0] << " <input-file> [--time-kruskal]\n";
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

    const auto begin = chrono::steady_clock::now();
    const KruskalResult result = KruskalMST(nodeCount, edges);
    const auto end = chrono::steady_clock::now();
    const chrono::duration<double, milli> elapsed = end - begin;

    if (options.benchmarkMode) {
        cout << fixed << setprecision(3);
        cout << "Kruskal time: " << elapsed.count() << " ms\n";
    }

    if (result.status == KruskalStatus::Overflow) {
        cerr << "Overflow detected while summing MST edge weights\n";
        return 1;
    }

    if (result.status == KruskalStatus::Disconnected) {
        cout << "Graph is disconnected; MST does not exist\n";
        return 0;
    }

    if (!options.benchmarkMode) {
        PrintResult(result);
    }

    return 0;
}
