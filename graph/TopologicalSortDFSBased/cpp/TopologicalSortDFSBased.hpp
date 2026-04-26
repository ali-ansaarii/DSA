#pragma once

#include <stdexcept>
#include <vector>

using namespace std;

struct TopologicalSortResult {
    bool hasCycle;
    vector<int> order;
};

TopologicalSortResult topologicalSortDFSBased(int vertexCount, const vector<pair<int, int>>& edges);
