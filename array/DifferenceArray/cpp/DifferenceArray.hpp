#pragma once

#include <vector>

bool BuildDifferenceArray(const std::vector<long long>& values, std::vector<long long>& diff);
bool ApplyRangeAdd(std::vector<long long>& diff, int left, int right, long long delta);
bool ReconstructValues(const std::vector<long long>& diff, std::vector<long long>& values);
