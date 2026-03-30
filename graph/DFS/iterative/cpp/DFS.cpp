#include "DFS.hpp"

#include <vector>

using namespace std;

vector<int> DFS(const vector<vector<int>>& graph, int start) {
    vector<int> order;
    vector<bool> visited(graph.size(), false);
    vector<int> stack = {start};

    while (!stack.empty()) {
        const int node = stack.back();
        stack.pop_back();

        if (visited[node]) {
            continue;
        }

        visited[node] = true;
        order.push_back(node);

        for (auto it = graph[node].rbegin(); it != graph[node].rend(); ++it) {
            if (!visited[*it]) {
                stack.push_back(*it);
            }
        }
    }

    return order;
}
