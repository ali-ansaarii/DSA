#include "FloydWarshall.hpp"

#include <limits>

namespace {

bool CheckedAdd(long long left, long long right, long long& out) {
    if (right > 0 && left > std::numeric_limits<long long>::max() - right) {
        return false;
    }

    if (right < 0 && left < std::numeric_limits<long long>::min() - right) {
        return false;
    }

    out = left + right;
    return true;
}

}  // namespace

FloydWarshallResult FloydWarshall(int nodeCount, const std::vector<Edge>& edges) {
    std::vector<std::vector<std::optional<long long>>> distances(
        nodeCount, std::vector<std::optional<long long>>(nodeCount));

    for (int node = 0; node < nodeCount; ++node) {
        distances[node][node] = 0;
    }

    for (const Edge& edge : edges) {
        if (!distances[edge.from][edge.to].has_value() || edge.weight < *distances[edge.from][edge.to]) {
            distances[edge.from][edge.to] = edge.weight;
        }
    }

    for (int intermediate = 0; intermediate < nodeCount; ++intermediate) {
        for (int from = 0; from < nodeCount; ++from) {
            if (!distances[from][intermediate].has_value()) {
                continue;
            }

            for (int to = 0; to < nodeCount; ++to) {
                if (!distances[intermediate][to].has_value()) {
                    continue;
                }

                long long candidate = 0;
                if (!CheckedAdd(*distances[from][intermediate], *distances[intermediate][to], candidate)) {
                    return {FloydWarshallStatus::Overflow, std::move(distances)};
                }

                if (!distances[from][to].has_value() || candidate < *distances[from][to]) {
                    distances[from][to] = candidate;
                }
            }
        }
    }

    for (int node = 0; node < nodeCount; ++node) {
        if (distances[node][node].has_value() && *distances[node][node] < 0) {
            return {FloydWarshallStatus::NegativeCycle, std::move(distances)};
        }
    }

    return {FloydWarshallStatus::Ok, std::move(distances)};
}
