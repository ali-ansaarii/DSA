#include "Dijkstra.hpp"

#include <functional>
#include <queue>
#include <vector>

using namespace std;

vector<long long> Dijkstra(const vector<vector<pair<int, long long>>>& graph, int start) {
    vector<long long> distances(graph.size(), DIJKSTRA_INF);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> minHeap;

    distances[start] = 0;
    minHeap.push({0, start});

    while (!minHeap.empty()) {
        const auto [distance, node] = minHeap.top();
        minHeap.pop();

        if (distance != distances[node]) {
            continue;
        }

        for (const auto& [neighbor, weight] : graph[node]) {
            const long long candidate = distance + weight;
            if (candidate < distances[neighbor]) {
                distances[neighbor] = candidate;
                minHeap.push({candidate, neighbor});
            }
        }
    }

    return distances;
}
