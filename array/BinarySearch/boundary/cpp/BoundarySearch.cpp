#include "BoundarySearch.hpp"

#include <cstddef>

int LowerBoundRangeHalving(const std::vector<long long>& values, long long target) {
    int left = 0;
    int right = static_cast<int>(values.size());

    while (left < right) {
        const int mid = left + (right - left) / 2;
        if (values[mid] < target) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }

    return left;
}

int LowerBoundPowersOfTwo(const std::vector<long long>& values, long long target) {
    int position = -1;
    int step = 1;
    while (step < static_cast<int>(values.size())) {
        step <<= 1;
    }

    for (; step > 0; step >>= 1) {
        const int next = position + step;
        if (next < static_cast<int>(values.size()) && values[next] < target) {
            position = next;
        }
    }

    return position + 1;
}
