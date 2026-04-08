#pragma once

#include <cstdint>
#include <limits>
#include <stdexcept>
#include <utility>
#include <vector>

inline constexpr long long DIJKSTRA_MAX_DISTANCE = std::numeric_limits<long long>::max();

struct DijkstraResult {
    std::vector<long long> distances;
    std::vector<bool> reachable;
};

class DijkstraOverflowError : public std::runtime_error {
public:
    DijkstraOverflowError()
        : std::runtime_error("Shortest-path overflow: a path distance exceeded the signed 64-bit integer range.") {}
};

DijkstraResult Dijkstra(const std::vector<std::vector<std::pair<int, long long>>>& graph, int start);
