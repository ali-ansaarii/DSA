#include "FenwickTree.hpp"

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

bool CheckedSub(long long a, long long b, long long& result) {
    if (b == numeric_limits<long long>::min()) {
        return false;
    }
    return CheckedAdd(a, -b, result);
}

class FenwickTree {
public:
    explicit FenwickTree(int n) : tree_(n + 1, 0) {}

    bool Add(int index, long long delta) {
        for (int i = index + 1; i < static_cast<int>(tree_.size()); i += i & -i) {
            long long updated = 0;
            if (!CheckedAdd(tree_[i], delta, updated)) {
                return false;
            }
            tree_[i] = updated;
        }
        return true;
    }

    bool PrefixSum(int index, long long& result) const {
        result = 0;
        for (int i = index + 1; i > 0; i -= i & -i) {
            long long updated = 0;
            if (!CheckedAdd(result, tree_[i], updated)) {
                return false;
            }
            result = updated;
        }
        return true;
    }

    bool RangeSum(int left, int right, long long& result) const {
        long long rightPrefix = 0;
        if (!PrefixSum(right, rightPrefix)) {
            return false;
        }

        if (left == 0) {
            result = rightPrefix;
            return true;
        }

        long long leftPrefix = 0;
        if (!PrefixSum(left - 1, leftPrefix)) {
            return false;
        }

        return CheckedSub(rightPrefix, leftPrefix, result);
    }

private:
    vector<long long> tree_;
};
}  // namespace

vector<long long> ProcessFenwickQueries(
    const vector<long long>& initialValues,
    const vector<Query>& queries,
    string& errorMessage
) {
    FenwickTree tree(static_cast<int>(initialValues.size()));
    vector<long long> results;

    for (int index = 0; index < static_cast<int>(initialValues.size()); ++index) {
        if (!tree.Add(index, initialValues[index])) {
            errorMessage = "Fenwick tree overflowed while building the initial state.";
            return {};
        }
    }

    results.reserve(queries.size());
    for (const Query& query : queries) {
        if (query.type == QueryType::Add) {
            if (!tree.Add(query.left, query.delta)) {
                errorMessage = "Fenwick tree overflowed while applying an update.";
                return {};
            }
        } else {
            long long sum = 0;
            if (!tree.RangeSum(query.left, query.right, sum)) {
                errorMessage = "Fenwick tree overflowed while evaluating a sum query.";
                return {};
            }
            results.push_back(sum);
        }
    }

    return results;
}
