import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public final class ShortestPathInDAG {
    public static final long INF = Long.MAX_VALUE / 4;

    private ShortestPathInDAG() {}

    public record Edge(int from, int to, long weight) {}

    private record AdjacentEdge(int to, long weight) {}

    public static long[] shortestPathInDAG(int vertexCount, List<Edge> edges, int source) {
        if (vertexCount < 0) {
            throw new IllegalArgumentException("vertex count cannot be negative");
        }
        if (source < 0 || source >= vertexCount) {
            throw new IllegalArgumentException("source vertex is out of range");
        }

        List<List<AdjacentEdge>> adjacency = new ArrayList<>(vertexCount);
        for (int vertex = 0; vertex < vertexCount; vertex++) {
            adjacency.add(new ArrayList<>());
        }
        int[] indegree = new int[vertexCount];

        for (Edge edge : edges) {
            if (edge.from() < 0 || edge.from() >= vertexCount || edge.to() < 0 || edge.to() >= vertexCount) {
                throw new IllegalArgumentException("edge endpoint is out of range");
            }
            adjacency.get(edge.from()).add(new AdjacentEdge(edge.to(), edge.weight()));
            indegree[edge.to()]++;
        }

        ArrayDeque<Integer> ready = new ArrayDeque<>();
        for (int vertex = 0; vertex < vertexCount; vertex++) {
            if (indegree[vertex] == 0) {
                ready.add(vertex);
            }
        }

        int[] topologicalOrder = new int[vertexCount];
        int orderSize = 0;
        while (!ready.isEmpty()) {
            int vertex = ready.removeFirst();
            topologicalOrder[orderSize++] = vertex;

            for (AdjacentEdge edge : adjacency.get(vertex)) {
                indegree[edge.to()]--;
                if (indegree[edge.to()] == 0) {
                    ready.add(edge.to());
                }
            }
        }

        if (orderSize != vertexCount) {
            throw new IllegalArgumentException("input graph is not a DAG");
        }

        long[] distance = new long[vertexCount];
        Arrays.fill(distance, INF);
        distance[source] = 0;

        for (int i = 0; i < orderSize; i++) {
            int vertex = topologicalOrder[i];
            if (distance[vertex] == INF) {
                continue;
            }
            for (AdjacentEdge edge : adjacency.get(vertex)) {
                long candidate = distance[vertex] + edge.weight();
                if (candidate < distance[edge.to()]) {
                    distance[edge.to()] = candidate;
                }
            }
        }

        return distance;
    }
}
