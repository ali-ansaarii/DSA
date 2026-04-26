#pragma once

#include <vector>

using namespace std;

struct BidirectionalBFSResult {
    int distance;
    vector<int> path;
};

BidirectionalBFSResult shortestPathBidirectionalBFS(
    const vector<vector<int>>& graph,
    int source,
    int target
);
