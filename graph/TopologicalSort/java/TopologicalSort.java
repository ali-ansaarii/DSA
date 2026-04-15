import java.util.*;

public class TopologicalSort {
    public static List<Integer> TopologicalSort(List<List<Integer>> graph) {
        int[] indegree = new int[graph.size()];
        for (List<Integer> neighbors : graph) {
            for (int neighbor : neighbors) {
                indegree[neighbor]++;
            }
        }

        Deque<Integer> ready = new ArrayDeque<>();
        for (int node = 0; node < graph.size(); node++) {
            if (indegree[node] == 0) {
                ready.add(node);
            }
        }

        List<Integer> order = new ArrayList<>();
        while (!ready.isEmpty()) {
            int node = ready.remove();
            order.add(node);

            for (int neighbor : graph.get(node)) {
                indegree[neighbor]--;
                if (indegree[neighbor] == 0) {
                    ready.add(neighbor);
                }
            }
        }

        return order;
    }
}
