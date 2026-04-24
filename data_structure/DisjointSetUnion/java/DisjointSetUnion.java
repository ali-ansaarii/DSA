import java.util.*;

public class DisjointSetUnion {
    public enum OperationType {
        UNION,
        CONNECTED,
        FIND
    }

    public static final class Operation {
        public final OperationType type;
        public final int first;
        public final int second;

        public Operation(OperationType type, int first, int second) {
            this.type = type;
            this.first = first;
            this.second = second;
        }
    }

    public static List<String> DisjointSetUnion(int n, List<Operation> operations) {
        int[] parent = new int[n];
        int[] componentSize = new int[n];
        for (int node = 0; node < n; node++) {
            parent[node] = node;
            componentSize[node] = 1;
        }

        List<String> queryResults = new ArrayList<>();
        for (Operation operation : operations) {
            if (operation.type == OperationType.UNION) {
                int rootA = findRoot(parent, operation.first);
                int rootB = findRoot(parent, operation.second);

                if (rootA == rootB) {
                    continue;
                }

                if (componentSize[rootA] < componentSize[rootB] ||
                    (componentSize[rootA] == componentSize[rootB] && rootA > rootB)) {
                    int temp = rootA;
                    rootA = rootB;
                    rootB = temp;
                }

                parent[rootB] = rootA;
                componentSize[rootA] += componentSize[rootB];
            } else if (operation.type == OperationType.CONNECTED) {
                queryResults.add(findRoot(parent, operation.first) == findRoot(parent, operation.second) ? "true" : "false");
            } else {
                queryResults.add(Integer.toString(findRoot(parent, operation.first)));
            }
        }

        return queryResults;
    }

    private static int findRoot(int[] parent, int node) {
        if (parent[node] == node) {
            return node;
        }

        parent[node] = findRoot(parent, parent[node]);
        return parent[node];
    }
}
