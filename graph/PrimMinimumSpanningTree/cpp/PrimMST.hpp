#pragma once

#include <vector>

struct Edge {
    int from;
    int to;
    long long weight;
};

enum class PrimStatus {
    Ok,
    Disconnected,
    Overflow,
};

struct PrimResult {
    PrimStatus status;
    long long totalWeight;
    std::vector<Edge> chosenEdges;
};

PrimResult PrimMST(int nodeCount, const std::vector<Edge>& edges);
