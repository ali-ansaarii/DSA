#include "BinarySearchOnAnswer.hpp"

#include <algorithm>
#include <numeric>
#include <stdexcept>

using namespace std;

bool canPartitionWithMaxGroupSum(const vector<long long>& values, int maxGroups, long long limit) {
    if (maxGroups <= 0) {
        return false;
    }

    int groupsUsed = 1;
    long long currentSum = 0;

    for (long long value : values) {
        if (value < 0) {
            throw invalid_argument("Binary Search on Answer partition baseline requires non-negative values");
        }
        if (value > limit) {
            return false;
        }
        if (currentSum + value > limit) {
            ++groupsUsed;
            currentSum = value;
            if (groupsUsed > maxGroups) {
                return false;
            }
        } else {
            currentSum += value;
        }
    }

    return true;
}

long long minimizeLargestGroupSum(const vector<long long>& values, int maxGroups) {
    if (values.empty()) {
        return 0;
    }
    if (maxGroups <= 0) {
        throw invalid_argument("maxGroups must be positive");
    }

    long long low = 0;
    long long high = 0;
    for (long long value : values) {
        if (value < 0) {
            throw invalid_argument("Binary Search on Answer partition baseline requires non-negative values");
        }
        low = max(low, value);
        high += value;
    }

    while (low < high) {
        long long mid = low + (high - low) / 2;
        if (canPartitionWithMaxGroupSum(values, maxGroups, mid)) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }

    return low;
}
