#include "MonotonicStack.hpp"

using namespace std;

vector<long long> NextGreaterElements(const vector<long long>& values) {
    vector<long long> answer(values.size(), -1);
    vector<long long> stack;
    stack.reserve(values.size());

    for (int index = static_cast<int>(values.size()) - 1; index >= 0; --index) {
        while (!stack.empty() && stack.back() <= values[index]) {
            stack.pop_back();
        }
        if (!stack.empty()) {
            answer[index] = stack.back();
        }
        stack.push_back(values[index]);
    }

    return answer;
}
