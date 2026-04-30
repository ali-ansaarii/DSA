#include "ShortestPathInDAG.hpp"

#include <queue>
#include <stdexcept>
#include <utility>

using namespace std;

vector<long long> shortestPathInDAG(int vertexCount, const vector<Edge>& edges, int source) {
    if (vertexCount < 0) {
        throw invalid_argument("vertex count cannot be negative");
    }
    if (source < 0 || source >= vertexCount) {
        throw invalid_argument("source vertex is out of range");
    }

    vector<vector<pair<int, long long>>> adjacency(vertexCount);
    vector<int> indegree(vertexCount, 0);

    for (const Edge& edge : edges) {
        if (edge.from < 0 || edge.from >= vertexCount || edge.to < 0 || edge.to >= vertexCount) {
            throw invalid_argument("edge endpoint is out of range");
        }
        adjacency[edge.from].push_back({edge.to, edge.weight});
        ++indegree[edge.to];
    }

    queue<int> ready;
    for (int vertex = 0; vertex < vertexCount; ++vertex) {
        if (indegree[vertex] == 0) {
            ready.push(vertex);
        }
    }

    vector<int> topologicalOrder;
    topologicalOrder.reserve(vertexCount);
    while (!ready.empty()) {
        int vertex = ready.front();
        ready.pop();
        topologicalOrder.push_back(vertex);

        for (const auto& [neighbor, weight] : adjacency[vertex]) {
            (void)weight;
            --indegree[neighbor];
            if (indegree[neighbor] == 0) {
                ready.push(neighbor);
            }
        }
    }

    if (static_cast<int>(topologicalOrder.size()) != vertexCount) {
        throw invalid_argument("input graph is not a DAG");
    }

    vector<long long> distance(vertexCount, DAG_INF);
    distance[source] = 0;

    for (int vertex : topologicalOrder) {
        if (distance[vertex] == DAG_INF) {
            continue;
        }
        for (const auto& [neighbor, weight] : adjacency[vertex]) {
            long long candidate = distance[vertex] + weight;
            if (candidate < distance[neighbor]) {
                distance[neighbor] = candidate;
            }
        }
    }

    return distance;
}
