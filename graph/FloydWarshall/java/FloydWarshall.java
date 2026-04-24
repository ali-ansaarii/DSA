import java.util.List;

public final class FloydWarshall {
    private FloydWarshall() {}

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
        NEGATIVE_CYCLE,
        OVERFLOW
    }

    public static final class Result {
        public final Status status;
        public final Long[][] distances;

        public Result(Status status, Long[][] distances) {
            this.status = status;
            this.distances = distances;
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

    public static Result floydWarshall(int nodeCount, List<Edge> edges) {
        Long[][] distances = new Long[nodeCount][nodeCount];

        for (int node = 0; node < nodeCount; ++node) {
            distances[node][node] = 0L;
        }

        for (Edge edge : edges) {
            Long current = distances[edge.source][edge.target];
            if (current == null || edge.weight < current) {
                distances[edge.source][edge.target] = edge.weight;
            }
        }

        for (int intermediate = 0; intermediate < nodeCount; ++intermediate) {
            for (int source = 0; source < nodeCount; ++source) {
                Long left = distances[source][intermediate];
                if (left == null) {
                    continue;
                }

                for (int target = 0; target < nodeCount; ++target) {
                    Long right = distances[intermediate][target];
                    if (right == null) {
                        continue;
                    }

                    Long candidate = checkedAdd(left, right);
                    if (candidate == null) {
                        return new Result(Status.OVERFLOW, distances);
                    }

                    Long current = distances[source][target];
                    if (current == null || candidate < current) {
                        distances[source][target] = candidate;
                    }
                }
            }
        }

        for (int node = 0; node < nodeCount; ++node) {
            Long diagonal = distances[node][node];
            if (diagonal != null && diagonal < 0) {
                return new Result(Status.NEGATIVE_CYCLE, distances);
            }
        }

        return new Result(Status.OK, distances);
    }
}
