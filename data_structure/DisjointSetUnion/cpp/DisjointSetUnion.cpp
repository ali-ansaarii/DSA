#include "DisjointSetUnion.hpp"

#include <functional>
#include <string>
#include <vector>

using namespace std;

vector<string> DisjointSetUnion(int n, const vector<Operation>& operations) {
    vector<int> parent(n);
    vector<int> componentSize(n, 1);
    for (int node = 0; node < n; ++node) {
        parent[node] = node;
    }

    function<int(int)> findRoot = [&](int node) -> int {
        if (parent[node] == node) {
            return node;
        }

        parent[node] = findRoot(parent[node]);
        return parent[node];
    };

    vector<string> queryResults;
    for (const Operation& operation : operations) {
        if (operation.type == OperationType::Union) {
            int rootA = findRoot(operation.first);
            int rootB = findRoot(operation.second);

            if (rootA == rootB) {
                continue;
            }

            if (componentSize[rootA] < componentSize[rootB] ||
                (componentSize[rootA] == componentSize[rootB] && rootA > rootB)) {
                swap(rootA, rootB);
            }

            parent[rootB] = rootA;
            componentSize[rootA] += componentSize[rootB];
        } else if (operation.type == OperationType::Connected) {
            queryResults.push_back(findRoot(operation.first) == findRoot(operation.second) ? "true" : "false");
        } else {
            queryResults.push_back(to_string(findRoot(operation.first)));
        }
    }

    return queryResults;
}
