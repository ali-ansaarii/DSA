#pragma once

#include <cstddef>
#include <vector>

using namespace std;

struct TernarySearchResult {
    size_t index;
    long long value;
};

TernarySearchResult findUnimodalMaximum(const vector<long long>& values);
