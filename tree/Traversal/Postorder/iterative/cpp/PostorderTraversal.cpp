#include "PostorderTraversal.hpp"

#include <utility>
#include <vector>

using namespace std;

vector<int> PostorderTraversal(const vector<int>& leftChildren, const vector<int>& rightChildren, int root) {
    vector<int> order;
    vector<pair<int, bool>> stack = {{root, false}};

    while (!stack.empty()) {
        const auto [node, expanded] = stack.back();
        stack.pop_back();

        if (expanded) {
            order.push_back(node);
            continue;
        }

        stack.push_back({node, true});

        if (rightChildren[node] != -1) {
            stack.push_back({rightChildren[node], false});
        }

        if (leftChildren[node] != -1) {
            stack.push_back({leftChildren[node], false});
        }
    }

    return order;
}
