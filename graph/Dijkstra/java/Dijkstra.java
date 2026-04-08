import java.util.*;

public class Dijkstra {
    public static final long MAX_DISTANCE = Long.MAX_VALUE;

    public static final class Edge {
        public final int to;
        public final long weight;

        public Edge(int to, long weight) {
            this.to = to;
            this.weight = weight;
        }
    }

    private static final class NodeState {
        public final int node;
        public final long distance;

        private NodeState(int node, long distance) {
            this.node = node;
            this.distance = distance;
        }
    }

    public static final class Result {
        public final long[] distances;
        public final boolean[] reachable;

        public Result(long[] distances, boolean[] reachable) {
            this.distances = distances;
            this.reachable = reachable;
        }
    }

    public static Result Dijkstra(List<List<Edge>> graph, int start) {
        boolean[] graphReachable = new boolean[graph.size()];
        ArrayDeque<Integer> traversalQueue = new ArrayDeque<>();
        graphReachable[start] = true;
        traversalQueue.add(start);

        while (!traversalQueue.isEmpty()) {
            int node = traversalQueue.removeFirst();
            for (Edge edge : graph.get(node)) {
                if (!graphReachable[edge.to]) {
                    graphReachable[edge.to] = true;
                    traversalQueue.addLast(edge.to);
                }
            }
        }

        long[] distances = new long[graph.size()];
        boolean[] reachable = new boolean[graph.size()];

        PriorityQueue<NodeState> minHeap = new PriorityQueue<>(Comparator.comparingLong(state -> state.distance));
        reachable[start] = true;
        distances[start] = 0;
        minHeap.add(new NodeState(start, 0));

        while (!minHeap.isEmpty()) {
            NodeState state = minHeap.poll();

            if (!reachable[state.node] || state.distance != distances[state.node]) {
                continue;
            }

            for (Edge edge : graph.get(state.node)) {
                if (state.distance > MAX_DISTANCE - edge.weight) {
                    continue;
                }

                long candidate = state.distance + edge.weight;
                if (!reachable[edge.to] || candidate < distances[edge.to]) {
                    reachable[edge.to] = true;
                    distances[edge.to] = candidate;
                    minHeap.add(new NodeState(edge.to, candidate));
                }
            }
        }

        for (int i = 0; i < graph.size(); i++) {
            if (graphReachable[i] && !reachable[i]) {
                throw new ArithmeticException(
                    "Shortest-path overflow: a path distance exceeded the signed 64-bit integer range."
                );
            }
        }

        return new Result(distances, reachable);
    }
}
