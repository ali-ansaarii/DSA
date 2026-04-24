import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;

public final class PrimMST {
    private PrimMST() {}

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

    private static final class Candidate {
        final long weight;
        final int source;
        final int target;
        final int nextNode;

        Candidate(long weight, int source, int target, int nextNode) {
            this.weight = weight;
            this.source = source;
            this.target = target;
            this.nextNode = nextNode;
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

    public static Result primMST(int nodeCount, List<Edge> edges) {
        if (nodeCount <= 1) {
            return new Result(Status.OK, 0L, new ArrayList<>());
        }

        List<List<Edge>> adjacency = new ArrayList<>(nodeCount);
        for (int node = 0; node < nodeCount; ++node) {
            adjacency.add(new ArrayList<>());
        }

        for (Edge edge : edges) {
            Edge normalized = normalize(edge);
            adjacency.get(normalized.source).add(new Edge(normalized.source, normalized.target, normalized.weight));
            adjacency.get(normalized.target).add(new Edge(normalized.target, normalized.source, normalized.weight));
        }

        boolean[] visited = new boolean[nodeCount];
        PriorityQueue<Candidate> heap =
                new PriorityQueue<>(
                        Comparator.comparingLong((Candidate candidate) -> candidate.weight)
                                .thenComparingInt(candidate -> candidate.source)
                                .thenComparingInt(candidate -> candidate.target)
                                .thenComparingInt(candidate -> candidate.nextNode));
        List<Edge> chosenEdges = new ArrayList<>(nodeCount - 1);
        long totalWeight = 0L;

        java.util.function.IntConsumer pushCandidates =
                node -> {
                    for (Edge edge : adjacency.get(node)) {
                        if (visited[edge.target]) {
                            continue;
                        }
                        Edge normalized = normalize(new Edge(edge.source, edge.target, edge.weight));
                        heap.add(new Candidate(normalized.weight, normalized.source, normalized.target, edge.target));
                    }
                };

        visited[0] = true;
        int visitedCount = 1;
        pushCandidates.accept(0);

        while (!heap.isEmpty() && visitedCount < nodeCount) {
            Candidate candidate = heap.poll();
            if (visited[candidate.nextNode]) {
                continue;
            }

            Long updated = checkedAdd(totalWeight, candidate.weight);
            if (updated == null) {
                return new Result(Status.OVERFLOW, totalWeight, chosenEdges);
            }

            totalWeight = updated;
            chosenEdges.add(new Edge(candidate.source, candidate.target, candidate.weight));
            visited[candidate.nextNode] = true;
            visitedCount += 1;
            pushCandidates.accept(candidate.nextNode);
        }

        if (visitedCount != nodeCount) {
            return new Result(Status.DISCONNECTED, totalWeight, chosenEdges);
        }

        return new Result(Status.OK, totalWeight, chosenEdges);
    }
}
