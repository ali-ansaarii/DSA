import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class TopologicalSortDFSBased {
    private TopologicalSortDFSBased() {}

    public record Edge(int from, int to) {}

    public record Result(boolean hasCycle, List<Integer> order) {}

    private static final class Frame {
        private final int vertex;
        private int nextIndex;

        private Frame(int vertex, int nextIndex) {
            this.vertex = vertex;
            this.nextIndex = nextIndex;
        }
    }

    public static Result sort(int vertexCount, List<Edge> edges) {
        if (vertexCount < 0) {
            throw new IllegalArgumentException("vertex count must be non-negative");
        }

        List<List<Integer>> graph = new ArrayList<>(vertexCount);
        for (int i = 0; i < vertexCount; i++) {
            graph.add(new ArrayList<>());
        }

        for (Edge edge : edges) {
            if (edge.from() < 0 || edge.from() >= vertexCount || edge.to() < 0 || edge.to() >= vertexCount) {
                throw new IllegalArgumentException("edge endpoint is outside the vertex range");
            }
            graph.get(edge.from()).add(edge.to());
        }

        int[] color = new int[vertexCount]; // 0 = unvisited, 1 = visiting, 2 = done
        List<Integer> postorder = new ArrayList<>(vertexCount);

        for (int start = 0; start < vertexCount; start++) {
            if (color[start] != 0) {
                continue;
            }

            color[start] = 1;
            List<Frame> stack = new ArrayList<>();
            stack.add(new Frame(start, 0));

            while (!stack.isEmpty()) {
                Frame frame = stack.get(stack.size() - 1);
                List<Integer> neighbors = graph.get(frame.vertex);

                if (frame.nextIndex < neighbors.size()) {
                    int neighbor = neighbors.get(frame.nextIndex);
                    frame.nextIndex++;

                    if (color[neighbor] == 0) {
                        color[neighbor] = 1;
                        stack.add(new Frame(neighbor, 0));
                    } else if (color[neighbor] == 1) {
                        return new Result(true, List.of());
                    }
                } else {
                    color[frame.vertex] = 2;
                    postorder.add(frame.vertex);
                    stack.remove(stack.size() - 1);
                }
            }
        }

        Collections.reverse(postorder);
        return new Result(false, postorder);
    }
}
