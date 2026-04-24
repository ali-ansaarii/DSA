#include "PrefixSum.hpp"

#include <limits>

namespace {

bool CheckedAdd(long long left, long long right, long long& out) {
    if (right > 0 && left > std::numeric_limits<long long>::max() - right) {
        return false;
    }
    if (right < 0 && left < std::numeric_limits<long long>::min() - right) {
        return false;
    }
    out = left + right;
    return true;
}

bool CheckedSub(long long left, long long right, long long& out) {
    if (right == std::numeric_limits<long long>::min()) {
        if (left >= 0) {
            return false;
        }
        out = left - right;
        return true;
    }
    return CheckedAdd(left, -right, out);
}

}  // namespace

bool BuildPrefixSums(const std::vector<long long>& values, std::vector<long long>& prefix) {
    prefix.assign(values.size() + 1, 0);

    for (size_t index = 0; index < values.size(); ++index) {
        if (!CheckedAdd(prefix[index], values[index], prefix[index + 1])) {
            return false;
        }
    }

    return true;
}

bool RangeSum(const std::vector<long long>& prefix, int left, int right, long long& sum) {
    return CheckedSub(prefix[static_cast<size_t>(right) + 1], prefix[left], sum);
}
