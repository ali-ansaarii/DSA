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

bool BestFixedWindow(const vector<long long>& values, int k, long long& bestSum, int& bestLeft, int& bestRight) {
    long long windowSum = 0;
    for (int i = 0; i < k; ++i) {
        if (!CheckedAdd(windowSum, values[i], windowSum)) {
            return false;
        }
    }

    bestSum = windowSum;
    bestLeft = 0;
    bestRight = k - 1;

    for (int right = k; right < static_cast<int>(values.size()); ++right) {
        if (!CheckedSub(windowSum, values[right - k], windowSum)) {
            return false;
        }
        if (!CheckedAdd(windowSum, values[right], windowSum)) {
            return false;
        }
        const int left = right - k + 1;
        if (windowSum > bestSum) {
            bestSum = windowSum;
            bestLeft = left;
            bestRight = right;
        }
    }

    return true;
}
