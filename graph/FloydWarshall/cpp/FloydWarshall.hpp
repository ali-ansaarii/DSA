#pragma once

#include <optional>
#include <vector>

struct Edge {
    int from;
    int to;
    long long weight;
};

enum class FloydWarshallStatus {
    Ok,
    NegativeCycle,
    Overflow,
};

struct FloydWarshallResult {
    FloydWarshallStatus status;
    std::vector<std::vector<std::optional<long long>>> distances;
};

FloydWarshallResult FloydWarshall(int nodeCount, const std::vector<Edge>& edges);
