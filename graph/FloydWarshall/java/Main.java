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
        final List<FloydWarshall.Edge> edges;

        ParsedInput(int nodeCount, List<FloydWarshall.Edge> edges) {
            this.nodeCount = nodeCount;
            this.edges = edges;
        }
    }

    private Main() {}

    private static ProgramOptions parseArguments(String[] args) {
        ProgramOptions options = new ProgramOptions();
        for (String argument : args) {
            if ("--time-floyd-warshall".equals(argument)) {
                options.benchmarkMode = true;
            } else if (options.inputPath == null) {
                options.inputPath = argument;
            } else {
                throw new IllegalArgumentException("Usage: Main <input-file> [--time-floyd-warshall]");
            }
        }

        if (options.inputPath == null) {
            throw new IllegalArgumentException("Usage: Main <input-file> [--time-floyd-warshall]");
        }

        return options;
    }

    private static ParsedInput readInput(String path) throws IOException {
        String[] tokens = Files.readString(Path.of(path)).trim().split("\\s+");
        int position = 0;

        if (tokens.length < 2) {
            throw new IllegalArgumentException("Invalid graph input");
        }

        int nodeCount = Integer.parseInt(tokens[position++]);
        int edgeCount = Integer.parseInt(tokens[position++]);

        if (nodeCount <= 0 || edgeCount < 0) {
            throw new IllegalArgumentException("Invalid graph header");
        }

        List<FloydWarshall.Edge> edges = new ArrayList<>(edgeCount);
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

            edges.add(new FloydWarshall.Edge(source, target, weight));
        }

        return new ParsedInput(nodeCount, edges);
    }

    private static void printMatrix(Long[][] distances) {
        System.out.println("All-pairs shortest distances:");
        for (Long[] row : distances) {
            StringBuilder builder = new StringBuilder();
            for (int column = 0; column < row.length; ++column) {
                if (column > 0) {
                    builder.append(' ');
                }
                builder.append(row[column] == null ? "INF" : row[column]);
            }
            System.out.println(builder);
        }
    }

    public static void main(String[] args) {
        try {
            ProgramOptions options = parseArguments(args);
            ParsedInput input = readInput(options.inputPath);

            long startTime = System.nanoTime();
            FloydWarshall.Result result = FloydWarshall.floydWarshall(input.nodeCount, input.edges);
            double elapsedMs = (System.nanoTime() - startTime) / 1_000_000.0;

            if (options.benchmarkMode) {
                System.out.printf(Locale.US, "Floyd-Warshall time: %.3f ms%n", elapsedMs);
            }

            if (result.status == FloydWarshall.Status.OVERFLOW) {
                System.err.println("Overflow detected while updating the distance matrix");
                System.exit(1);
            }

            if (result.status == FloydWarshall.Status.NEGATIVE_CYCLE) {
                System.out.println("Negative cycle detected");
                return;
            }

            if (!options.benchmarkMode) {
                printMatrix(result.distances);
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
