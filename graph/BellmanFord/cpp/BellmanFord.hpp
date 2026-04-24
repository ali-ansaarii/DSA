#pragma once

#include <optional>
#include <vector>

struct Edge {
    int from;
    int to;
    long long weight;
};

enum class BellmanFordStatus {
    Ok,
    NegativeCycle,
    Overflow,
};

struct BellmanFordResult {
    BellmanFordStatus status;
    std::vector<std::optional<long long>> distances;
};

BellmanFordResult BellmanFord(int nodeCount, const std::vector<Edge>& edges, int start);
