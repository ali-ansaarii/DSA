#include "TernarySearch.hpp"

#include <stdexcept>

using namespace std;

TernarySearchResult findUnimodalMaximum(const vector<long long>& values) {
    if (values.empty()) {
        throw invalid_argument("ternary search requires a non-empty array");
    }

    size_t left = 0;
    size_t right = values.size() - 1;

    while (right > left + 3) {
        const size_t third = (right - left) / 3;
        const size_t mid1 = left + third;
        const size_t mid2 = right - third;

        if (values[mid1] < values[mid2]) {
            left = mid1 + 1;
        } else if (values[mid1] > values[mid2]) {
            right = mid2 - 1;
        } else {
            left = mid1;
            right = mid2;
        }
    }

    size_t bestIndex = left;
    for (size_t i = left + 1; i <= right; ++i) {
        if (values[i] > values[bestIndex]) {
            bestIndex = i;
        }
    }

    return {bestIndex, values[bestIndex]};
}
