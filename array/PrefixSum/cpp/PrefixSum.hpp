#pragma once

#include <vector>

bool BuildPrefixSums(const std::vector<long long>& values, std::vector<long long>& prefix);
bool RangeSum(const std::vector<long long>& prefix, int left, int right, long long& sum);
