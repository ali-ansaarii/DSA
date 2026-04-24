#include "SlidingWindow.hpp"

using namespace std;

namespace {
constexpr __int128 kMinI64 = static_cast<__int128>(-9223372036854775807LL - 1LL);
constexpr __int128 kMaxI64 = static_cast<__int128>(9223372036854775807LL);

bool TryConvertToI64(__int128 value, long long& result) {
    if (value < kMinI64 || value > kMaxI64) {
        return false;
    }
    result = static_cast<long long>(value);
    return true;
}
}  // namespace

bool BestFixedWindow(const vector<long long>& values, int k, long long& bestSum, int& bestLeft, int& bestRight) {
    __int128 windowSumWide = 0;
    for (int i = 0; i < k; ++i) {
        windowSumWide += static_cast<__int128>(values[i]);
    }
    if (!TryConvertToI64(windowSumWide, bestSum)) {
        return false;
    }

    bestLeft = 0;
    bestRight = k - 1;

    for (int right = k; right < static_cast<int>(values.size()); ++right) {
        windowSumWide = windowSumWide - static_cast<__int128>(values[right - k]) +
                        static_cast<__int128>(values[right]);

        long long windowSum = 0;
        if (!TryConvertToI64(windowSumWide, windowSum)) {
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
