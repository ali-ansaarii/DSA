#include "TopologicalSort.hpp"

#include <queue>
#include <vector>

using namespace std;

vector<int> TopologicalSort(const vector<vector<int>>& graph) {
    vector<int> indegree(graph.size(), 0);
    for (const auto& neighbors : graph) {
        for (const int neighbor : neighbors) {
            ++indegree[neighbor];
        }
    }

    queue<int> ready;
    for (int node = 0; node < static_cast<int>(graph.size()); ++node) {
        if (indegree[node] == 0) {
            ready.push(node);
        }
    }

    vector<int> order;
    while (!ready.empty()) {
        const int node = ready.front();
        ready.pop();
        order.push_back(node);

        for (const int neighbor : graph[node]) {
            --indegree[neighbor];
            if (indegree[neighbor] == 0) {
                ready.push(neighbor);
            }
        }
    }

    return order;
}
