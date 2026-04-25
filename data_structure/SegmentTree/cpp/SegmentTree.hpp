#pragma once

#include <string>
#include <vector>

using namespace std;

enum class QueryType {
    Add,
    Sum,
};

struct Query {
    QueryType type;
    int left;
    int right;
    long long delta;
};

vector<long long> ProcessSegmentTreeQueries(
    const vector<long long>& initialValues,
    const vector<Query>& queries,
    string& errorMessage
);
