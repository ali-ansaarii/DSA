#pragma once

#include <vector>

bool MinWindowAtLeastTarget(const std::vector<long long>& values,
                            long long target,
                            int& bestLength,
                            int& bestLeft,
                            int& bestRight);
