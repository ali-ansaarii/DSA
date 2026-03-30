#include "DFS.hpp"

#include <functional>
#include <vector>

using namespace std;

vector<int> DFS(const vector<vector<int>>& graph, int start) {
    vector<int> order;
    vector<bool> visited(graph.size(), false);

    function<void(int)> dfs = [&](int node) {
        visited[node] = true;
        order.push_back(node);

        for (const int neighbor : graph[node]) {
            if (!visited[neighbor]) {
                dfs(neighbor);
            }
        }
    };

    dfs(start);
    return order;
}
