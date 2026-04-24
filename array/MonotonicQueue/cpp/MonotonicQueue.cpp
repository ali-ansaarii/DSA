#include "MonotonicQueue.hpp"

#include <deque>

using namespace std;

vector<long long> SlidingWindowMaximum(const vector<long long>& values, int windowSize) {
    deque<int> candidateIndices;
    vector<long long> maxima;
    maxima.reserve(values.size() >= static_cast<size_t>(windowSize)
                       ? values.size() - static_cast<size_t>(windowSize) + 1
                       : 0);

    for (int i = 0; i < static_cast<int>(values.size()); ++i) {
        while (!candidateIndices.empty() &&
               candidateIndices.front() <= i - windowSize) {
            candidateIndices.pop_front();
        }

        while (!candidateIndices.empty() &&
               values[candidateIndices.back()] <= values[i]) {
            candidateIndices.pop_back();
        }

        candidateIndices.push_back(i);

        if (i + 1 >= windowSize) {
            maxima.push_back(values[candidateIndices.front()]);
        }
    }

    return maxima;
}
