#include "BidirectionalBFS.hpp"

#include <algorithm>
#include <deque>

using namespace std;

namespace {
vector<int> buildPath(int meeting, const vector<int>& parentFromSource, const vector<int>& parentFromTarget) {
    vector<int> left;
    for (int vertex = meeting; vertex != -1;) {
        left.push_back(vertex);
        if (parentFromSource[vertex] == vertex) {
            break;
        }
        vertex = parentFromSource[vertex];
    }
    reverse(left.begin(), left.end());

    vector<int> path = left;
    for (int vertex = parentFromTarget[meeting]; vertex != -1 && vertex != meeting;) {
        path.push_back(vertex);
        if (parentFromTarget[vertex] == vertex) {
            break;
        }
        vertex = parentFromTarget[vertex];
    }
    return path;
}

int expandOneLevel(
    deque<int>& frontier,
    vector<int>& parentThisSide,
    const vector<int>& parentOtherSide,
    const vector<vector<int>>& graph
) {
    const size_t levelSize = frontier.size();
    for (size_t i = 0; i < levelSize; ++i) {
        const int current = frontier.front();
        frontier.pop_front();

        for (const int neighbor : graph[current]) {
            if (parentThisSide[neighbor] != -1) {
                continue;
            }

            parentThisSide[neighbor] = current;
            if (parentOtherSide[neighbor] != -1) {
                return neighbor;
            }
            frontier.push_back(neighbor);
        }
    }
    return -1;
}
}  // namespace

BidirectionalBFSResult shortestPathBidirectionalBFS(
    const vector<vector<int>>& graph,
    int source,
    int target
) {
    if (source == target) {
        return {0, {source}};
    }

    const int n = static_cast<int>(graph.size());
    vector<int> parentFromSource(n, -1);
    vector<int> parentFromTarget(n, -1);
    deque<int> sourceFrontier;
    deque<int> targetFrontier;

    parentFromSource[source] = source;
    parentFromTarget[target] = target;
    sourceFrontier.push_back(source);
    targetFrontier.push_back(target);

    while (!sourceFrontier.empty() && !targetFrontier.empty()) {
        int meeting = -1;
        if (sourceFrontier.size() <= targetFrontier.size()) {
            meeting = expandOneLevel(sourceFrontier, parentFromSource, parentFromTarget, graph);
        } else {
            meeting = expandOneLevel(targetFrontier, parentFromTarget, parentFromSource, graph);
        }

        if (meeting != -1) {
            vector<int> path = buildPath(meeting, parentFromSource, parentFromTarget);
            return {static_cast<int>(path.size()) - 1, path};
        }
    }

    return {-1, {}};
}
