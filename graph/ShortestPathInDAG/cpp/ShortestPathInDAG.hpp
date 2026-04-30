#pragma once

#include <limits>
#include <vector>

using namespace std;

struct Edge {
    int from;
    int to;
    long long weight;
};

constexpr long long DAG_INF = numeric_limits<long long>::max() / 4;

vector<long long> shortestPathInDAG(int vertexCount, const vector<Edge>& edges, int source);
