import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Main {
    private record ParsedInput(int vertexCount, List<ShortestPathInDAG.Edge> edges, int source) {}

    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean time_flag_time_shortest_path_in_dag = false;

        for (String argument : args) {
            if (argument.equals("--time-shortest-path-in-dag")) {
                time_flag_time_shortest_path_in_dag = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        try {
            ParsedInput parsedInput = parseInput(inputPath);
            long[] distances;
            if (time_flag_time_shortest_path_in_dag) {
                long start = System.nanoTime();
                distances = ShortestPathInDAG.shortestPathInDAG(
                    parsedInput.vertexCount(),
                    parsedInput.edges(),
                    parsedInput.source()
                );
                long elapsed = System.nanoTime() - start;
                System.err.printf("algorithm_ms %.6f%n", elapsed / 1_000_000.0);
            } else {
                distances = ShortestPathInDAG.shortestPathInDAG(
                    parsedInput.vertexCount(),
                    parsedInput.edges(),
                    parsedInput.source()
                );
            }
            System.out.println(formatDistances(distances));
        } catch (IOException | IllegalArgumentException error) {
            System.err.println(error.getMessage());
            System.exit(1);
        }
    }

    private static ParsedInput parseInput(Path inputPath) throws IOException {
        String[] tokens = Files.readString(inputPath).trim().split("\\s+");
        if (tokens.length < 3) {
            throw new IllegalArgumentException("invalid input header");
        }

        int cursor = 0;
        int vertexCount = Integer.parseInt(tokens[cursor++]);
        int edgeCount = Integer.parseInt(tokens[cursor++]);
        int source = Integer.parseInt(tokens[cursor++]);
        if (vertexCount < 0 || edgeCount < 0) {
            throw new IllegalArgumentException("vertex and edge counts must be non-negative");
        }

        List<ShortestPathInDAG.Edge> edges = new ArrayList<>(edgeCount);
        for (int index = 0; index < edgeCount; index++) {
            if (cursor + 2 >= tokens.length) {
                throw new IllegalArgumentException("invalid edge line at index " + index);
            }
            int from = Integer.parseInt(tokens[cursor++]);
            int to = Integer.parseInt(tokens[cursor++]);
            long weight = Long.parseLong(tokens[cursor++]);
            edges.add(new ShortestPathInDAG.Edge(from, to, weight));
        }

        return new ParsedInput(vertexCount, edges, source);
    }

    private static String formatDistances(long[] distances) {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < distances.length; i++) {
            if (i > 0) {
                builder.append(' ');
            }
            if (distances[i] == ShortestPathInDAG.INF) {
                builder.append("INF");
            } else {
                builder.append(distances[i]);
            }
        }
        return builder.toString();
    }
}
