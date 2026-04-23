#include "PostorderTraversal.hpp"

#include <functional>
#include <vector>

using namespace std;

vector<int> PostorderTraversal(const vector<int>& leftChildren, const vector<int>& rightChildren, int root) {
    vector<int> order;

    function<void(int)> traverse = [&](int node) {
        if (leftChildren[node] != -1) {
            traverse(leftChildren[node]);
        }

        if (rightChildren[node] != -1) {
            traverse(rightChildren[node]);
        }

        order.push_back(node);
    };

    traverse(root);
    return order;
}
