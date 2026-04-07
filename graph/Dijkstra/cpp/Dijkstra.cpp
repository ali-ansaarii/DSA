#include "Dijkstra.hpp"

#include <functional>
#include <queue>
#include <vector>

using namespace std;

DijkstraResult Dijkstra(const vector<vector<pair<int, long long>>>& graph, int start) {
    vector<bool> graphReachable(graph.size(), false);
    queue<int> traversalQueue;
    graphReachable[start] = true;
    traversalQueue.push(start);

    while (!traversalQueue.empty()) {
        const int node = traversalQueue.front();
        traversalQueue.pop();

        for (const auto& [neighbor, weight] : graph[node]) {
            (void)weight;
            if (!graphReachable[neighbor]) {
                graphReachable[neighbor] = true;
                traversalQueue.push(neighbor);
            }
        }
    }

    vector<long long> distances(graph.size(), 0);
    vector<bool> reachable(graph.size(), false);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> minHeap;

    reachable[start] = true;
    distances[start] = 0;
    minHeap.push({0, start});

    while (!minHeap.empty()) {
        const auto [distance, node] = minHeap.top();
        minHeap.pop();

        if (!reachable[node] || distance != distances[node]) {
            continue;
        }

        for (const auto& [neighbor, weight] : graph[node]) {
            if (distance > DIJKSTRA_MAX_DISTANCE - weight) {
                continue;
            }

            const long long candidate = distance + weight;
            if (!reachable[neighbor] || candidate < distances[neighbor]) {
                reachable[neighbor] = true;
                distances[neighbor] = candidate;
                minHeap.push({candidate, neighbor});
            }
        }
    }

    for (size_t i = 0; i < graph.size(); ++i) {
        if (graphReachable[i] && !reachable[i]) {
            throw DijkstraOverflowError();
        }
    }

    return {move(distances), move(reachable)};
}
