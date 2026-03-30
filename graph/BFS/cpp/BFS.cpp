#include "BFS.hpp"

#include <queue>
#include <vector>

using namespace std;

vector<int> BFS(const vector<vector<int>>& graph, int start) {
    vector<int> order;
    vector<bool> visited(graph.size(), false);
    queue<int> q;

    visited[start] = true;
    q.push(start);

    while (!q.empty()) {
        const int node = q.front();
        q.pop();
        order.push_back(node);

        for (const int neighbor : graph[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push(neighbor);
            }
        }
    }

    return order;
}
