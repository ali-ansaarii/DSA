#include "SlidingWindow.hpp"

using namespace std;

namespace {
bool CheckedAdd(long long a, long long b, long long& result) {
    if ((b > 0 && a > 9223372036854775807LL - b) ||
        (b < 0 && a < (-9223372036854775807LL - 1LL) - b)) {
        return false;
    }
    result = a + b;
    return true;
}

bool CheckedSub(long long a, long long b, long long& result) {
    if ((b < 0 && a > 9223372036854775807LL + b) ||
        (b > 0 && a < (-9223372036854775807LL - 1LL) + b)) {
        return false;
    }
    result = a - b;
    return true;
}
}  // namespace

bool MinWindowAtLeastTarget(const vector<long long>& values,
                            long long target,
                            int& bestLength,
                            int& bestLeft,
                            int& bestRight) {
    long long windowSum = 0;
    int left = 0;
    bestLength = -1;
    bestLeft = -1;
    bestRight = -1;

    for (int right = 0; right < static_cast<int>(values.size()); ++right) {
        if (!CheckedAdd(windowSum, values[right], windowSum)) {
            return false;
        }

        while (windowSum >= target) {
            const int currentLength = right - left + 1;
            if (bestLength == -1 || currentLength < bestLength) {
                bestLength = currentLength;
                bestLeft = left;
                bestRight = right;
            }

            if (!CheckedSub(windowSum, values[left], windowSum)) {
                return false;
            }
            ++left;
        }
    }

    return true;
}
