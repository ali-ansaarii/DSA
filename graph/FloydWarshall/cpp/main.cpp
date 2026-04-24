#include "FloydWarshall.hpp"

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
        if (argument == "--time-floyd-warshall") {
            options.benchmarkMode = true;
        } else if (options.inputPath.empty()) {
            options.inputPath = argument;
        } else {
            return false;
        }
    }

    return !options.inputPath.empty();
}

void PrintMatrix(const vector<vector<optional<long long>>>& distances) {
    cout << "All-pairs shortest distances:\n";
    for (const auto& row : distances) {
        for (size_t column = 0; column < row.size(); ++column) {
            if (column > 0) {
                cout << ' ';
            }

            if (row[column].has_value()) {
                cout << *row[column];
            } else {
                cout << "INF";
            }
        }
        cout << '\n';
    }
}

}  // namespace

int main(int argc, char* argv[]) {
    ProgramOptions options;
    if (!ParseArguments(argc, argv, options)) {
        cerr << "Usage: " << argv[0] << " <input-file> [--time-floyd-warshall]\n";
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
    const FloydWarshallResult result = FloydWarshall(nodeCount, edges);
    const auto end = chrono::steady_clock::now();
    const chrono::duration<double, milli> elapsed = end - begin;

    if (options.benchmarkMode) {
        cout << fixed << setprecision(3);
        cout << "Floyd-Warshall time: " << elapsed.count() << " ms\n";
    }

    if (result.status == FloydWarshallStatus::Overflow) {
        cerr << "Overflow detected while updating the distance matrix\n";
        return 1;
    }

    if (result.status == FloydWarshallStatus::NegativeCycle) {
        cout << "Negative cycle detected\n";
        return 0;
    }

    if (!options.benchmarkMode) {
        PrintMatrix(result.distances);
    }

    return 0;
}
