#pragma once

#include <vector>

struct Edge {
    int from;
    int to;
    long long weight;
};

enum class KruskalStatus {
    Ok,
    Disconnected,
    Overflow,
};

struct KruskalResult {
    KruskalStatus status;
    long long totalWeight;
    std::vector<Edge> chosenEdges;
};

KruskalResult KruskalMST(int nodeCount, const std::vector<Edge>& edges);
