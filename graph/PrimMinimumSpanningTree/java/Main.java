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
        final List<PrimMST.Edge> edges;

        ParsedInput(int nodeCount, List<PrimMST.Edge> edges) {
            this.nodeCount = nodeCount;
            this.edges = edges;
        }
    }

    private Main() {}

    private static ProgramOptions parseArguments(String[] args) {
        ProgramOptions options = new ProgramOptions();
        for (String argument : args) {
            if ("--time-prim".equals(argument)) {
                options.benchmarkMode = true;
            } else if (options.inputPath == null) {
                options.inputPath = argument;
            } else {
                throw new IllegalArgumentException("Usage: Main <input-file> [--time-prim]");
            }
        }

        if (options.inputPath == null) {
            throw new IllegalArgumentException("Usage: Main <input-file> [--time-prim]");
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

        List<PrimMST.Edge> edges = new ArrayList<>(edgeCount);
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

            edges.add(new PrimMST.Edge(source, target, weight));
        }

        return new ParsedInput(nodeCount, edges);
    }

    private static void printResult(PrimMST.Result result) {
        System.out.println("MST total weight: " + result.totalWeight);
        System.out.println("MST edges:");
        for (PrimMST.Edge edge : result.chosenEdges) {
            System.out.println(edge.source + " " + edge.target + " " + edge.weight);
        }
    }

    public static void main(String[] args) {
        try {
            ProgramOptions options = parseArguments(args);
            ParsedInput input = readInput(options.inputPath);

            long startTime = System.nanoTime();
            PrimMST.Result result = PrimMST.primMST(input.nodeCount, input.edges);
            double elapsedMs = (System.nanoTime() - startTime) / 1_000_000.0;

            if (options.benchmarkMode) {
                System.out.printf(Locale.US, "Prim time: %.3f ms%n", elapsedMs);
            }

            if (result.status == PrimMST.Status.OVERFLOW) {
                System.err.println("Overflow detected while summing MST edge weights");
                System.exit(1);
            }

            if (result.status == PrimMST.Status.DISCONNECTED) {
                System.out.println("Graph is disconnected; MST does not exist");
                return;
            }

            if (!options.benchmarkMode) {
                printResult(result);
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
