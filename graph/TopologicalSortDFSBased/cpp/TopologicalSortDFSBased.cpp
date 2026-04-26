#include "TopologicalSortDFSBased.hpp"

#include <algorithm>
#include <utility>

using namespace std;

TopologicalSortResult topologicalSortDFSBased(int vertexCount, const vector<pair<int, int>>& edges) {
    if (vertexCount < 0) {
        throw invalid_argument("vertex count must be non-negative");
    }

    vector<vector<int>> graph(vertexCount);
    for (const auto& [from, to] : edges) {
        if (from < 0 || from >= vertexCount || to < 0 || to >= vertexCount) {
            throw invalid_argument("edge endpoint is outside the vertex range");
        }
        graph[from].push_back(to);
    }

    vector<int> color(vertexCount, 0); // 0 = unvisited, 1 = visiting, 2 = done
    vector<int> postorder;
    postorder.reserve(vertexCount);

    for (int start = 0; start < vertexCount; ++start) {
        if (color[start] != 0) {
            continue;
        }

        color[start] = 1;
        vector<pair<int, size_t>> stack;
        stack.emplace_back(start, 0);

        while (!stack.empty()) {
            int vertex = stack.back().first;
            size_t& nextIndex = stack.back().second;

            if (nextIndex < graph[vertex].size()) {
                int neighbor = graph[vertex][nextIndex++];
                if (color[neighbor] == 0) {
                    color[neighbor] = 1;
                    stack.emplace_back(neighbor, 0);
                } else if (color[neighbor] == 1) {
                    return {true, {}};
                }
            } else {
                color[vertex] = 2;
                postorder.push_back(vertex);
                stack.pop_back();
            }
        }
    }

    reverse(postorder.begin(), postorder.end());
    return {false, postorder};
}
