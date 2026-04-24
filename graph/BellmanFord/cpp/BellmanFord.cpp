#include "BellmanFord.hpp"

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

BellmanFordResult BellmanFord(int nodeCount, const std::vector<Edge>& edges, int start) {
    BellmanFordResult result{BellmanFordStatus::Ok, std::vector<std::optional<long long>>(nodeCount)};
    result.distances[start] = 0;

    for (int pass = 0; pass < nodeCount - 1; ++pass) {
        bool updated = false;

        for (const Edge& edge : edges) {
            if (!result.distances[edge.from].has_value()) {
                continue;
            }

            long long candidate = 0;
            if (!CheckedAdd(*result.distances[edge.from], edge.weight, candidate)) {
                result.status = BellmanFordStatus::Overflow;
                return result;
            }

            if (!result.distances[edge.to].has_value() || candidate < *result.distances[edge.to]) {
                result.distances[edge.to] = candidate;
                updated = true;
            }
        }

        if (!updated) {
            break;
        }
    }

    for (const Edge& edge : edges) {
        if (!result.distances[edge.from].has_value()) {
            continue;
        }

        long long candidate = 0;
        if (!CheckedAdd(*result.distances[edge.from], edge.weight, candidate)) {
            result.status = BellmanFordStatus::Overflow;
            return result;
        }

        if (!result.distances[edge.to].has_value() || candidate < *result.distances[edge.to]) {
            result.status = BellmanFordStatus::NegativeCycle;
            return result;
        }
    }

    return result;
}
