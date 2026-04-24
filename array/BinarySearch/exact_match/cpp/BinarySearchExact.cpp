#include "BinarySearchExact.hpp"

int BinarySearchExact(const std::vector<long long>& values, long long target) {
    int left = 0;
    int right = static_cast<int>(values.size()) - 1;

    while (left <= right) {
        const int mid = left + (right - left) / 2;

        if (values[mid] == target) {
            return mid;
        }

        if (values[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    return -1;
}
