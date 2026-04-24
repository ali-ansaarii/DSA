#include "DifferenceArray.hpp"

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

bool BuildDifferenceArray(const vector<long long>& values, vector<long long>& diff) {
    diff.assign(values.size(), 0);
    if (values.empty()) {
        return true;
    }

    diff[0] = values[0];
    for (size_t i = 1; i < values.size(); ++i) {
        if (!CheckedSub(values[i], values[i - 1], diff[i])) {
            return false;
        }
    }
    return true;
}

bool ApplyRangeAdd(vector<long long>& diff, int left, int right, long long delta) {
    long long updated = 0;
    if (!CheckedAdd(diff[left], delta, updated)) {
        return false;
    }
    diff[left] = updated;

    if (right + 1 < static_cast<int>(diff.size())) {
        if (!CheckedSub(diff[right + 1], delta, updated)) {
            return false;
        }
        diff[right + 1] = updated;
    }
    return true;
}

bool ReconstructValues(const vector<long long>& diff, vector<long long>& values) {
    values.assign(diff.size(), 0);
    if (diff.empty()) {
        return true;
    }

    values[0] = diff[0];
    for (size_t i = 1; i < diff.size(); ++i) {
        if (!CheckedAdd(values[i - 1], diff[i], values[i])) {
            return false;
        }
    }
    return true;
}
