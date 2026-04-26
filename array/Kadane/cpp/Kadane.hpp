#pragma once

#include <cstddef>
#include <vector>

using namespace std;

struct KadaneResult {
    long long maximum_sum;
    size_t start_index;
    size_t end_index;
};

KadaneResult maxSubarrayKadane(const vector<long long>& values);
