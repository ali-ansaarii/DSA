import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public final class Main {
    private static final class ProgramOptions {
        String inputPath;
        boolean benchmarkMode;
    }

    private static final class ParsedInput {
        final int nodeCount;
        final List<BellmanFord.Edge> edges;
        final int start;

        ParsedInput(int nodeCount, List<BellmanFord.Edge> edges, int start) {
            this.nodeCount = nodeCount;
            this.edges = edges;
            this.start = start;
        }
    }

    private Main() {}

    private static ProgramOptions parseArguments(String[] args) {
        ProgramOptions options = new ProgramOptions();
        for (String argument : args) {
            if ("--time-bellman-ford".equals(argument)) {
                options.benchmarkMode = true;
            } else if (options.inputPath == null) {
                options.inputPath = argument;
            } else {
                throw new IllegalArgumentException("Usage: Main <input-file> [--time-bellman-ford]");
            }
        }

        if (options.inputPath == null) {
            throw new IllegalArgumentException("Usage: Main <input-file> [--time-bellman-ford]");
        }

        return options;
    }

    private static ParsedInput readInput(String path) throws IOException {
        String[] tokens = Files.readString(Path.of(path)).trim().split("\\s+");
        int position = 0;

        if (tokens.length < 3) {
            throw new IllegalArgumentException("Invalid graph input");
        }

        int nodeCount = Integer.parseInt(tokens[position++]);
        int edgeCount = Integer.parseInt(tokens[position++]);

        if (nodeCount <= 0 || edgeCount < 0) {
            throw new IllegalArgumentException("Invalid graph header");
        }

        List<BellmanFord.Edge> edges = new ArrayList<>(edgeCount);
        for (int index = 0; index < edgeCount; ++index) {
            if (position + 3 > tokens.length) {
                throw new IllegalArgumentException("Invalid edge at index " + index);
            }

            int source = Integer.parseInt(tokens[position++]);
            int target = Integer.parseInt(tokens[position++]);
            long weight = Long.parseLong(tokens[position++]);

            if (source < 0 || source >= nodeCount || target < 0 || target >= nodeCount) {
                throw new IllegalArgumentException("Edge node out of range at index " + index);
            }

            edges.add(new BellmanFord.Edge(source, target, weight));
        }

        if (position >= tokens.length) {
            throw new IllegalArgumentException("Missing start node");
        }

        int start = Integer.parseInt(tokens[position]);
        if (start < 0 || start >= nodeCount) {
            throw new IllegalArgumentException("Invalid start node");
        }

        return new ParsedInput(nodeCount, edges, start);
    }

    private static void printDistances(List<Long> distances, int start) {
        StringBuilder builder = new StringBuilder();
        builder.append("Shortest distances from ").append(start).append(':');
        for (Long distance : distances) {
            builder.append(' ');
            builder.append(distance == null ? "INF" : distance);
        }
        System.out.println(builder);
    }

    public static void main(String[] args) {
        try {
            ProgramOptions options = parseArguments(args);
            ParsedInput input = readInput(options.inputPath);

            long startTime = System.nanoTime();
            BellmanFord.Result result = BellmanFord.bellmanFord(input.nodeCount, input.edges, input.start);
            double elapsedMs = (System.nanoTime() - startTime) / 1_000_000.0;

            if (options.benchmarkMode) {
                System.out.printf(Locale.US, "Bellman-Ford time: %.3f ms%n", elapsedMs);
            }

            if (result.status == BellmanFord.Status.OVERFLOW) {
                System.err.println("Overflow detected while relaxing edges");
                System.exit(1);
            }

            if (result.status == BellmanFord.Status.NEGATIVE_CYCLE) {
                System.out.println("Negative cycle reachable from " + input.start);
                return;
            }

            if (!options.benchmarkMode) {
                printDistances(result.distances, input.start);
            }
        } catch (IllegalArgumentException error) {
            System.err.println(error.getMessage());
            System.exit(1);
        } catch (IOException error) {
            System.err.println("Failed to open input file: " + error.getMessage());
            System.exit(1);
        }
    }
}
