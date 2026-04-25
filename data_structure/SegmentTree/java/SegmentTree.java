import java.util.ArrayList;
import java.util.List;

enum QueryType {
    ADD,
    SUM
}

record Query(QueryType type, int left, int right, long delta) {}

final class SegmentTreeStructure {
    private final int n;
    private final long[] tree;

    SegmentTreeStructure(List<Long> initialValues) {
        n = initialValues.size();
        tree = new long[2 * n];

        for (int index = 0; index < n; ++index) {
            tree[n + index] = initialValues.get(index);
        }

        for (int node = n - 1; node > 0; --node) {
            tree[node] = Math.addExact(tree[2 * node], tree[2 * node + 1]);
        }
    }

    void add(int index, long delta) {
        int node = index + n;
        tree[node] = Math.addExact(tree[node], delta);
        node /= 2;
        while (node > 0) {
            tree[node] = Math.addExact(tree[2 * node], tree[2 * node + 1]);
            node /= 2;
        }
    }

    long rangeSum(int left, int right) {
        long result = 0;
        int l = left + n;
        int r = right + n + 1;

        while (l < r) {
            if ((l & 1) == 1) {
                result = Math.addExact(result, tree[l]);
                ++l;
            }
            if ((r & 1) == 1) {
                --r;
                result = Math.addExact(result, tree[r]);
            }
            l /= 2;
            r /= 2;
        }

        return result;
    }
}

public final class SegmentTree {
    private SegmentTree() {}

    public static List<Long> processSegmentTreeQueries(List<Long> initialValues, List<Query> queries) {
        SegmentTreeStructure tree = new SegmentTreeStructure(initialValues);
        List<Long> results = new ArrayList<>();
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
