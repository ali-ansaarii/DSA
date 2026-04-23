#include "InorderTraversal.hpp"

#include <vector>

using namespace std;

vector<int> InorderTraversal(const vector<int>& leftChildren, const vector<int>& rightChildren, int root) {
    vector<int> order;
    vector<int> stack;
    int current = root;

    while (current != -1 || !stack.empty()) {
        while (current != -1) {
            stack.push_back(current);
            current = leftChildren[current];
        }

        current = stack.back();
        stack.pop_back();
        order.push_back(current);
        current = rightChildren[current];
    }

    return order;
}
