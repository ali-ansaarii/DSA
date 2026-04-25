#include "MergeSort.hpp"

#include <algorithm>

using namespace std;

namespace {
void mergeRanges(vector<int64_t>& values, vector<int64_t>& buffer, size_t left, size_t mid, size_t right) {
    size_t i = left;
    size_t j = mid;
    size_t k = left;

    while (i < mid && j < right) {
        if (values[i] <= values[j]) {
            buffer[k++] = values[i++];
        } else {
            buffer[k++] = values[j++];
        }
    }

    while (i < mid) {
        buffer[k++] = values[i++];
    }

    while (j < right) {
        buffer[k++] = values[j++];
    }

    copy(buffer.begin() + static_cast<long long>(left), buffer.begin() + static_cast<long long>(right), values.begin() + static_cast<long long>(left));
}

void mergeSortRecursive(vector<int64_t>& values, vector<int64_t>& buffer, size_t left, size_t right) {
    if (right - left <= 1) {
        return;
    }

    const size_t mid = left + (right - left) / 2;
    mergeSortRecursive(values, buffer, left, mid);
    mergeSortRecursive(values, buffer, mid, right);
    mergeRanges(values, buffer, left, mid, right);
}
}  // namespace

vector<int64_t> mergeSort(const vector<int64_t>& values) {
    vector<int64_t> sorted = values;
    vector<int64_t> buffer(sorted.size());
    mergeSortRecursive(sorted, buffer, 0, sorted.size());
    return sorted;
}
