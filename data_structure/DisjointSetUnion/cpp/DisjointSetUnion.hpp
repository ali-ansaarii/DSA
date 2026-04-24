#pragma once

#include <string>
#include <vector>

enum class OperationType {
    Union,
    Connected,
    Find,
};

struct Operation {
    OperationType type;
    int first;
    int second;
};

std::vector<std::string> DisjointSetUnion(int n, const std::vector<Operation>& operations);
