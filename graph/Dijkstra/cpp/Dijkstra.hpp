#pragma once

#include <limits>
#include <utility>
#include <vector>

inline constexpr long long DIJKSTRA_INF = std::numeric_limits<long long>::max() / 4;

std::vector<long long> Dijkstra(const std::vector<std::vector<std::pair<int, long long>>>& graph, int start);
