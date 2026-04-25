#include "SegmentTree.hpp"

#include <limits>

using namespace std;

namespace {
bool CheckedAdd(long long a, long long b, long long& result) {
    if ((b > 0 && a > numeric_limits<long long>::max() - b) ||
        (b < 0 && a < numeric_limits<long long>::min() - b)) {
        return false;
    }
    result = a + b;
    return true;
}

class SegmentTree {
public:
    explicit SegmentTree(const vector<long long>& initialValues)
        : n_(static_cast<int>(initialValues.size())), tree_(2 * n_, 0) {}

    bool Build(const vector<long long>& initialValues) {
        for (int index = 0; index < n_; ++index) {
            tree_[n_ + index] = initialValues[index];
        }

        for (int node = n_ - 1; node > 0; --node) {
            long long sum = 0;
            if (!CheckedAdd(tree_[2 * node], tree_[2 * node + 1], sum)) {
                return false;
            }
            tree_[node] = sum;
        }

        return true;
    }

    bool Add(int index, long long delta) {
        int node = index + n_;
        long long updatedLeaf = 0;
        if (!CheckedAdd(tree_[node], delta, updatedLeaf)) {
            return false;
        }
        tree_[node] = updatedLeaf;

        for (node /= 2; node > 0; node /= 2) {
            long long sum = 0;
            if (!CheckedAdd(tree_[2 * node], tree_[2 * node + 1], sum)) {
                return false;
            }
            tree_[node] = sum;
        }

        return true;
    }

    bool RangeSum(int left, int right, long long& result) const {
        result = 0;
        int l = left + n_;
        int r = right + n_ + 1;

        while (l < r) {
            if (l & 1) {
                long long updated = 0;
                if (!CheckedAdd(result, tree_[l], updated)) {
                    return false;
                }
                result = updated;
                ++l;
            }
            if (r & 1) {
                --r;
                long long updated = 0;
                if (!CheckedAdd(result, tree_[r], updated)) {
                    return false;
                }
                result = updated;
            }
            l /= 2;
            r /= 2;
        }

        return true;
    }

private:
    int n_;
    vector<long long> tree_;
};
}  // namespace

vector<long long> ProcessSegmentTreeQueries(
    const vector<long long>& initialValues,
    const vector<Query>& queries,
    string& errorMessage
) {
    SegmentTree tree(initialValues);
    if (!tree.Build(initialValues)) {
        errorMessage = "Segment tree overflowed while building the initial state.";
        return {};
    }

    vector<long long> results;
    results.reserve(queries.size());

    for (const Query& query : queries) {
        if (query.type == QueryType::Add) {
            if (!tree.Add(query.left, query.delta)) {
                errorMessage = "Segment tree overflowed while applying an update.";
                return {};
            }
        } else {
            long long sum = 0;
            if (!tree.RangeSum(query.left, query.right, sum)) {
                errorMessage = "Segment tree overflowed while evaluating a sum query.";
                return {};
            }
            results.push_back(sum);
        }
    }

    return results;
}
