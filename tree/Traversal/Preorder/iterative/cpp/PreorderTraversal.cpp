#include "PreorderTraversal.hpp"

#include <vector>

using namespace std;

vector<int> PreorderTraversal(const vector<int>& leftChildren, const vector<int>& rightChildren, int root) {
    vector<int> order;
    vector<int> stack = {root};

    while (!stack.empty()) {
        const int node = stack.back();
        stack.pop_back();
        order.push_back(node);

        if (rightChildren[node] != -1) {
            stack.push_back(rightChildren[node]);
        }

        if (leftChildren[node] != -1) {
            stack.push_back(leftChildren[node]);
        }
    }

    return order;
}
