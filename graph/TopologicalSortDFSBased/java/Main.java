import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Main {
    private record ParsedInput(int vertexCount, List<TopologicalSortDFSBased.Edge> edges) {}

    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean time_flag_time_topological_sort_dfs_based = false;

        for (String argument : args) {
            if (argument.equals("--time-topological-sort-dfs-based")) {
                time_flag_time_topological_sort_dfs_based = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        ParsedInput parsed;
        try {
            parsed = parseInput(inputPath);
        } catch (IOException error) {
            System.err.println("Failed to read input file: " + error.getMessage());
            System.exit(1);
            return;
        } catch (IllegalArgumentException error) {
            System.err.println(error.getMessage());
            System.exit(1);
            return;
        }

        TopologicalSortDFSBased.Result result;
        try {
            long start = System.nanoTime();
            result = TopologicalSortDFSBased.sort(parsed.vertexCount(), parsed.edges());
            long elapsed = System.nanoTime() - start;

            if (time_flag_time_topological_sort_dfs_based) {
                System.err.println("algorithm_time_ns " + elapsed);
            }
        } catch (IllegalArgumentException error) {
            System.err.println(error.getMessage());
            System.exit(1);
            return;
        }

        if (result.hasCycle()) {
            System.out.println("CYCLE DETECTED");
            return;
        }

        System.out.println("Topological order:");
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < result.order().size(); i++) {
            if (i > 0) {
                builder.append(' ');
            }
            builder.append(result.order().get(i));
        }
        System.out.println(builder);
    }

    private static ParsedInput parseInput(Path inputPath) throws IOException {
        String[] tokens = Files.readString(inputPath).trim().split("\\s+");
        if (tokens.length < 2) {
            throw new IllegalArgumentException("input must start with: n m");
        }

        int vertexCount = Integer.parseInt(tokens[0]);
        int edgeCount = Integer.parseInt(tokens[1]);
        if (vertexCount < 0 || edgeCount < 0) {
            throw new IllegalArgumentException("n and m must be non-negative");
        }

        int expectedTokens = 2 + 2 * edgeCount;
        if (tokens.length != expectedTokens) {
            throw new IllegalArgumentException("expected " + edgeCount + " edges, found " + ((tokens.length - 2) / 2));
        }

        List<TopologicalSortDFSBased.Edge> edges = new ArrayList<>(edgeCount);
        for (int i = 0; i < edgeCount; i++) {
            int base = 2 + 2 * i;
            int from = Integer.parseInt(tokens[base]);
            int to = Integer.parseInt(tokens[base + 1]);
            edges.add(new TopologicalSortDFSBased.Edge(from, to));
        }

        return new ParsedInput(vertexCount, edges);
    }
}
