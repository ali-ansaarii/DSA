import java.util.List;

enum QueryType {
    ADD,
    SUM
}

record Query(QueryType type, int left, int right, long delta) {}

final class FenwickTreeStructure {
    private final long[] tree;

    FenwickTreeStructure(int size) {
        tree = new long[size + 1];
    }

    void add(int index, long delta) {
        for (int i = index + 1; i < tree.length; i += i & -i) {
            tree[i] = Math.addExact(tree[i], delta);
        }
    }

    long prefixSum(int index) {
        long result = 0;
        for (int i = index + 1; i > 0; i -= i & -i) {
            result = Math.addExact(result, tree[i]);
        }
        return result;
    }

    long rangeSum(int left, int right) {
        long rightPrefix = prefixSum(right);
        if (left == 0) {
            return rightPrefix;
        }
        return Math.subtractExact(rightPrefix, prefixSum(left - 1));
    }
}

public final class FenwickTree {
    private FenwickTree() {}

    public static List<Long> processFenwickQueries(List<Long> initialValues, List<Query> queries) {
        FenwickTreeStructure tree = new FenwickTreeStructure(initialValues.size());
        for (int index = 0; index < initialValues.size(); ++index) {
            tree.add(index, initialValues.get(index));
        }

        List<Long> results = new java.util.ArrayList<>();
        for (Query query : queries) {
            if (query.type() == QueryType.ADD) {
                tree.add(query.left(), query.delta());
            } else {
                results.add(tree.rangeSum(query.left(), query.right()));
            }
        }

        return results;
    }
}
