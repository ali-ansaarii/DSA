#pragma once

#include <cstdint>
#include <vector>

using namespace std;

bool canPartitionWithMaxGroupSum(const vector<long long>& values, int maxGroups, long long limit);
long long minimizeLargestGroupSum(const vector<long long>& values, int maxGroups);
