import java.util.*;

public class DFS {
    public static List<Integer> DFS(List<List<Integer>> graph, int start) {
        List<Integer> order = new ArrayList<>();
        boolean[] visited = new boolean[graph.size()];

        dfs(start, graph, visited, order);
        return order;
    }

    private static void dfs(int node, List<List<Integer>> graph, boolean[] visited, List<Integer> order) {
        visited[node] = true;
        order.add(node);

        for (int neighbor : graph.get(node)) {
            if (!visited[neighbor]) {
                dfs(neighbor, graph, visited, order);
            }
        }
    }
}
