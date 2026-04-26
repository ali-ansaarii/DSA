#pragma once

#include <vector>

using namespace std;

struct RectQuery {
    int r1;
    int c1;
    int r2;
    int c2;
};

class PrefixSum2D {
public:
    explicit PrefixSum2D(const vector<vector<long long>>& matrix);

    long long rectangle_sum(int r1, int c1, int r2, int c2) const;

private:
    vector<vector<long long>> prefix_;
};

vector<long long> answer_rectangle_queries(
    const vector<vector<long long>>& matrix,
    const vector<RectQuery>& queries
);
