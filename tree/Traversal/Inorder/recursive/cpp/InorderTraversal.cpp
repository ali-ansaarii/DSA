#include "InorderTraversal.hpp"

#include <functional>
#include <vector>

using namespace std;

vector<int> InorderTraversal(const vector<int>& leftChildren, const vector<int>& rightChildren, int root) {
    vector<int> order;

    function<void(int)> traverse = [&](int node) {
        if (leftChildren[node] != -1) {
            traverse(leftChildren[node]);
        }

        order.push_back(node);

        if (rightChildren[node] != -1) {
            traverse(rightChildren[node]);
        }
    };

    traverse(root);
    return order;
}
