#include "KruskalMST.hpp"

#include <algorithm>
#include <limits>
#include <numeric>

namespace {

struct DisjointSetUnion {
    std::vector<int> parent;
    std::vector<int> size;

    explicit DisjointSetUnion(int nodeCount) : parent(nodeCount), size(nodeCount, 1) {
        std::iota(parent.begin(), parent.end(), 0);
    }

    int Find(int node) {
        if (parent[node] == node) {
            return node;
        }
        parent[node] = Find(parent[node]);
        return parent[node];
    }

    bool Unite(int left, int right) {
        left = Find(left);
        right = Find(right);
        if (left == right) {
            return false;
        }
        if (size[left] < size[right]) {
            std::swap(left, right);
        }
        parent[right] = left;
        size[left] += size[right];
        return true;
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

bool EdgeLess(const Edge& left, const Edge& right) {
    if (left.weight != right.weight) {
        return left.weight < right.weight;
    }
    if (left.from != right.from) {
        return left.from < right.from;
    }
    return left.to < right.to;
}

}  // namespace

KruskalResult KruskalMST(int nodeCount, const std::vector<Edge>& edges) {
    std::vector<Edge> sortedEdges;
    sortedEdges.reserve(edges.size());
    for (const Edge& edge : edges) {
        sortedEdges.push_back(Normalize(edge));
    }
    std::sort(sortedEdges.begin(), sortedEdges.end(), EdgeLess);

    DisjointSetUnion dsu(nodeCount);
    KruskalResult result{KruskalStatus::Ok, 0, {}};
    result.chosenEdges.reserve(nodeCount > 0 ? nodeCount - 1 : 0);

    for (const Edge& edge : sortedEdges) {
        if (!dsu.Unite(edge.from, edge.to)) {
            continue;
        }

        long long updatedWeight = 0;
        if (!CheckedAdd(result.totalWeight, edge.weight, updatedWeight)) {
            result.status = KruskalStatus::Overflow;
            return result;
        }

        result.totalWeight = updatedWeight;
        result.chosenEdges.push_back(edge);

        if (static_cast<int>(result.chosenEdges.size()) == nodeCount - 1) {
            return result;
        }
    }

    result.status = KruskalStatus::Disconnected;
    return result;
}
