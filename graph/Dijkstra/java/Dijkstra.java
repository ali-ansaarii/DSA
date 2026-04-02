import java.util.*;

public class Dijkstra {
    public static final long INF = Long.MAX_VALUE / 4;

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

    public static long[] Dijkstra(List<List<Edge>> graph, int start) {
        long[] distances = new long[graph.size()];
        Arrays.fill(distances, INF);

        PriorityQueue<NodeState> minHeap = new PriorityQueue<>(Comparator.comparingLong(state -> state.distance));
        distances[start] = 0;
        minHeap.add(new NodeState(start, 0));

        while (!minHeap.isEmpty()) {
            NodeState state = minHeap.poll();

            if (state.distance != distances[state.node]) {
                continue;
            }

            for (Edge edge : graph.get(state.node)) {
                long candidate = state.distance + edge.weight;
                if (candidate < distances[edge.to]) {
                    distances[edge.to] = candidate;
                    minHeap.add(new NodeState(edge.to, candidate));
                }
            }
        }

        return distances;
    }
}
