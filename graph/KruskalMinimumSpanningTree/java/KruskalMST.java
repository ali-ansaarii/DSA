import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public final class KruskalMST {
    private KruskalMST() {}

    public static final class Edge {
        public final int source;
        public final int target;
        public final long weight;

        public Edge(int source, int target, long weight) {
            this.source = source;
            this.target = target;
            this.weight = weight;
        }
    }

    public enum Status {
        OK,
        DISCONNECTED,
        OVERFLOW
    }

    public static final class Result {
        public final Status status;
        public final long totalWeight;
        public final List<Edge> chosenEdges;

        public Result(Status status, long totalWeight, List<Edge> chosenEdges) {
            this.status = status;
            this.totalWeight = totalWeight;
            this.chosenEdges = chosenEdges;
        }
    }

    private static final class DisjointSetUnion {
        private final int[] parent;
        private final int[] size;

        private DisjointSetUnion(int nodeCount) {
            this.parent = new int[nodeCount];
            this.size = new int[nodeCount];
            for (int node = 0; node < nodeCount; ++node) {
                this.parent[node] = node;
                this.size[node] = 1;
            }
        }

        private int find(int node) {
            if (parent[node] == node) {
                return node;
            }
            parent[node] = find(parent[node]);
            return parent[node];
        }

        private boolean unite(int left, int right) {
            left = find(left);
            right = find(right);
            if (left == right) {
                return false;
            }
            if (size[left] < size[right]) {
                int temporary = left;
                left = right;
                right = temporary;
            }
            parent[right] = left;
            size[left] += size[right];
            return true;
        }
    }

    private static Long checkedAdd(long left, long right) {
        if (right > 0 && left > Long.MAX_VALUE - right) {
            return null;
        }
        if (right < 0 && left < Long.MIN_VALUE - right) {
            return null;
        }
        return left + right;
    }

    private static Edge normalize(Edge edge) {
        if (edge.source <= edge.target) {
            return edge;
        }
        return new Edge(edge.target, edge.source, edge.weight);
    }

    public static Result kruskalMST(int nodeCount, List<Edge> edges) {
        List<Edge> sortedEdges = new ArrayList<>(edges.size());
        for (Edge edge : edges) {
            sortedEdges.add(normalize(edge));
        }
        sortedEdges.sort(
                Comparator.comparingLong((Edge edge) -> edge.weight)
                        .thenComparingInt(edge -> edge.source)
                        .thenComparingInt(edge -> edge.target));

        DisjointSetUnion dsu = new DisjointSetUnion(nodeCount);
        List<Edge> chosenEdges = new ArrayList<>(Math.max(0, nodeCount - 1));
        long totalWeight = 0;

        for (Edge edge : sortedEdges) {
            if (!dsu.unite(edge.source, edge.target)) {
                continue;
            }

            Long updated = checkedAdd(totalWeight, edge.weight);
            if (updated == null) {
                return new Result(Status.OVERFLOW, totalWeight, chosenEdges);
            }

            totalWeight = updated;
            chosenEdges.add(edge);

            if (chosenEdges.size() == nodeCount - 1) {
                return new Result(Status.OK, totalWeight, chosenEdges);
            }
        }

        return new Result(Status.DISCONNECTED, totalWeight, chosenEdges);
    }
}
