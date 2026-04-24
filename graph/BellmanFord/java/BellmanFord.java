import java.util.ArrayList;
import java.util.List;

public final class BellmanFord {
    private BellmanFord() {}

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
        public final List<Long> distances;

        public Result(Status status, List<Long> distances) {
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

    public static Result bellmanFord(int nodeCount, List<Edge> edges, int start) {
        List<Long> distances = new ArrayList<>(nodeCount);
        for (int i = 0; i < nodeCount; ++i) {
            distances.add(null);
        }
        distances.set(start, 0L);

        for (int pass = 0; pass < nodeCount - 1; ++pass) {
            boolean updated = false;

            for (Edge edge : edges) {
                Long sourceDistance = distances.get(edge.source);
                if (sourceDistance == null) {
                    continue;
                }

                Long candidate = checkedAdd(sourceDistance, edge.weight);
                if (candidate == null) {
                    return new Result(Status.OVERFLOW, distances);
                }

                Long targetDistance = distances.get(edge.target);
                if (targetDistance == null || candidate < targetDistance) {
                    distances.set(edge.target, candidate);
                    updated = true;
                }
            }

            if (!updated) {
                break;
            }
        }

        for (Edge edge : edges) {
            Long sourceDistance = distances.get(edge.source);
            if (sourceDistance == null) {
                continue;
            }

            Long candidate = checkedAdd(sourceDistance, edge.weight);
            if (candidate == null) {
                return new Result(Status.OVERFLOW, distances);
            }

            Long targetDistance = distances.get(edge.target);
            if (targetDistance == null || candidate < targetDistance) {
                return new Result(Status.NEGATIVE_CYCLE, distances);
            }
        }

        return new Result(Status.OK, distances);
    }
}
