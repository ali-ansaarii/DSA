import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public final class BidirectionalBFS {
    private BidirectionalBFS() {}

    public static final class Result {
        public final int distance;
        public final List<Integer> path;

        public Result(int distance, List<Integer> path) {
            this.distance = distance;
            this.path = path;
        }
    }

    public static Result shortestPath(List<List<Integer>> graph, int source, int target) {
        if (source == target) {
            return new Result(0, List.of(source));
        }

        int n = graph.size();
        int[] parentFromSource = new int[n];
        int[] parentFromTarget = new int[n];
        for (int i = 0; i < n; i++) {
            parentFromSource[i] = -1;
            parentFromTarget[i] = -1;
        }

        ArrayDeque<Integer> sourceFrontier = new ArrayDeque<>();
        ArrayDeque<Integer> targetFrontier = new ArrayDeque<>();
        parentFromSource[source] = source;
        parentFromTarget[target] = target;
        sourceFrontier.addLast(source);
        targetFrontier.addLast(target);

        while (!sourceFrontier.isEmpty() && !targetFrontier.isEmpty()) {
            int meeting;
            if (sourceFrontier.size() <= targetFrontier.size()) {
                meeting = expandOneLevel(sourceFrontier, parentFromSource, parentFromTarget, graph);
            } else {
                meeting = expandOneLevel(targetFrontier, parentFromTarget, parentFromSource, graph);
            }

            if (meeting != -1) {
                List<Integer> path = buildPath(meeting, parentFromSource, parentFromTarget);
                return new Result(path.size() - 1, path);
            }
        }

        return new Result(-1, List.of());
    }

    private static int expandOneLevel(
        ArrayDeque<Integer> frontier,
        int[] parentThisSide,
        int[] parentOtherSide,
        List<List<Integer>> graph
    ) {
        int levelSize = frontier.size();
        for (int i = 0; i < levelSize; i++) {
            int current = frontier.removeFirst();
            for (int neighbor : graph.get(current)) {
                if (parentThisSide[neighbor] != -1) {
                    continue;
                }

                parentThisSide[neighbor] = current;
                if (parentOtherSide[neighbor] != -1) {
                    return neighbor;
                }
                frontier.addLast(neighbor);
            }
        }
        return -1;
    }

    private static List<Integer> buildPath(int meeting, int[] parentFromSource, int[] parentFromTarget) {
        ArrayList<Integer> left = new ArrayList<>();
        for (int vertex = meeting; vertex != -1; ) {
            left.add(vertex);
            if (parentFromSource[vertex] == vertex) {
                break;
            }
            vertex = parentFromSource[vertex];
        }
        Collections.reverse(left);

        ArrayList<Integer> path = new ArrayList<>(left);
        for (int vertex = parentFromTarget[meeting]; vertex != -1; ) {
            path.add(vertex);
            if (parentFromTarget[vertex] == vertex) {
                break;
            }
            vertex = parentFromTarget[vertex];
        }
        return path;
    }
}
