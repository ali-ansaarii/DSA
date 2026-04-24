#include "PrimMST.hpp"

#include <algorithm>
#include <functional>
#include <limits>
#include <queue>
#include <tuple>
#include <vector>

namespace {

struct Candidate {
    long long weight;
    int keyFrom;
    int keyTo;
    int nextNode;
};

struct CandidateGreater {
    bool operator()(const Candidate& left, const Candidate& right) const {
        if (left.weight != right.weight) {
            return left.weight > right.weight;
        }
        if (left.keyFrom != right.keyFrom) {
            return left.keyFrom > right.keyFrom;
        }
        if (left.keyTo != right.keyTo) {
            return left.keyTo > right.keyTo;
        }
        return left.nextNode > right.nextNode;
    }
};

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

Edge Normalize(const Edge& edge) {
    if (edge.from <= edge.to) {
        return edge;
    }
    return {edge.to, edge.from, edge.weight};
}

}  // namespace

PrimResult PrimMST(int nodeCount, const std::vector<Edge>& edges) {
    if (nodeCount <= 1) {
        return {PrimStatus::Ok, 0, {}};
    }

    std::vector<std::vector<Edge>> adjacency(nodeCount);
    for (const Edge& edge : edges) {
        Edge normalized = Normalize(edge);
        adjacency[normalized.from].push_back({normalized.from, normalized.to, normalized.weight});
        adjacency[normalized.to].push_back({normalized.to, normalized.from, normalized.weight});
    }

    std::vector<bool> visited(nodeCount, false);
    std::priority_queue<Candidate, std::vector<Candidate>, CandidateGreater> heap;
    PrimResult result{PrimStatus::Ok, 0, {}};
    result.chosenEdges.reserve(nodeCount - 1);

    auto pushCandidates = [&](int node) {
        for (const Edge& edge : adjacency[node]) {
            if (visited[edge.to]) {
                continue;
            }

            Edge normalized = Normalize({edge.from, edge.to, edge.weight});
            heap.push({normalized.weight, normalized.from, normalized.to, edge.to});
        }
    };

    visited[0] = true;
    int visitedCount = 1;
    pushCandidates(0);

    while (!heap.empty() && visitedCount < nodeCount) {
        Candidate candidate = heap.top();
        heap.pop();

        int nextNode = visited[candidate.nextNode] ? -1 : candidate.nextNode;
        if (nextNode == -1) {
            continue;
        }

        long long updatedWeight = 0;
        if (!CheckedAdd(result.totalWeight, candidate.weight, updatedWeight)) {
            result.status = PrimStatus::Overflow;
            return result;
        }

        result.totalWeight = updatedWeight;
        result.chosenEdges.push_back({candidate.keyFrom, candidate.keyTo, candidate.weight});
        visited[nextNode] = true;
        ++visitedCount;
        pushCandidates(nextNode);
    }

    if (visitedCount != nodeCount) {
        result.status = PrimStatus::Disconnected;
    }

    return result;
}
