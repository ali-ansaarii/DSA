#include "PreorderTraversal.hpp"

#include <functional>
#include <vector>

using namespace std;

vector<int> PreorderTraversal(const vector<int>& leftChildren, const vector<int>& rightChildren, int root) {
    vector<int> order;

    function<void(int)> dfs = [&](int node) {
        order.push_back(node);

        if (leftChildren[node] != -1) {
            dfs(leftChildren[node]);
        }

        if (rightChildren[node] != -1) {
            dfs(rightChildren[node]);
        }
    };

    dfs(root);
    return order;
}
