import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;

public final class Main {
    private static final class ProgramOptions {
        String inputPath;
        String method;
    }

    private static final class ParsedInput {
        final long[] values;
        final long[] queries;

        ParsedInput(long[] values, long[] queries) {
            this.values = values;
            this.queries = queries;
        }
    }

    private Main() {}

    private static ProgramOptions parseArguments(String[] args) {
        ProgramOptions options = new ProgramOptions();
        for (String argument : args) {
            if ("--time-range-halving".equals(argument)) {
                options.method = "range_halving";
            } else if ("--time-powers-of-two".equals(argument)) {
                options.method = "powers_of_two";
            } else if (options.inputPath == null) {
                options.inputPath = argument;
            } else {
                throw new IllegalArgumentException("Usage: Main <input-file> [--time-range-halving|--time-powers-of-two]");
            }
        }

        if (options.inputPath == null) {
            throw new IllegalArgumentException("Usage: Main <input-file> [--time-range-halving|--time-powers-of-two]");
        }

        return options;
    }

    private static ParsedInput readInput(String path) throws IOException {
        String[] tokens = Files.readString(Path.of(path)).trim().split("\\s+");
        if (tokens.length < 2) {
            throw new IllegalArgumentException("Invalid input header");
        }

        int position = 0;
        int valueCount = Integer.parseInt(tokens[position++]);
        int queryCount = Integer.parseInt(tokens[position++]);

        if (valueCount < 0 || queryCount < 0) {
            throw new IllegalArgumentException("Invalid input header");
        }

        if (position + valueCount + queryCount != tokens.length) {
            throw new IllegalArgumentException("Input length does not match n and q");
        }

        long[] values = new long[valueCount];
        for (int index = 0; index < valueCount; ++index) {
            values[index] = Long.parseLong(tokens[position++]);
        }

        long[] queries = new long[queryCount];
        for (int index = 0; index < queryCount; ++index) {
            queries[index] = Long.parseLong(tokens[position++]);
        }

        return new ParsedInput(values, queries);
    }

    public static void main(String[] args) {
        try {
            ProgramOptions options = parseArguments(args);
            ParsedInput input = readInput(options.inputPath);

            if (options.method != null) {
                int[] results = new int[input.queries.length];
                long startTime = System.nanoTime();
                if ("range_halving".equals(options.method)) {
                    for (int index = 0; index < input.queries.length; ++index) {
                        results[index] = BoundarySearch.lowerBoundRangeHalving(input.values, input.queries[index]);
                    }
                } else {
                    for (int index = 0; index < input.queries.length; ++index) {
                        results[index] = BoundarySearch.lowerBoundPowersOfTwo(input.values, input.queries[index]);
                    }
                }
                double elapsedMs = (System.nanoTime() - startTime) / 1_000_000.0;

                if ("range_halving".equals(options.method)) {
                    System.out.printf(Locale.US, "Boundary search time (range-halving): %.3f ms%n", elapsedMs);
                } else {
                    System.out.printf(Locale.US, "Boundary search time (powers-of-two): %.3f ms%n", elapsedMs);
                }
                return;
            }

            int[] rangeResults = new int[input.queries.length];
            int[] powersResults = new int[input.queries.length];
            for (int index = 0; index < input.queries.length; ++index) {
                rangeResults[index] = BoundarySearch.lowerBoundRangeHalving(input.values, input.queries[index]);
                powersResults[index] = BoundarySearch.lowerBoundPowersOfTwo(input.values, input.queries[index]);
            }

            for (int index = 0; index < rangeResults.length; ++index) {
                if (rangeResults[index] != powersResults[index]) {
                    System.err.println("Boundary-search implementations disagree");
                    System.exit(1);
                }
            }

            StringBuilder rangeBuilder = new StringBuilder("Boundary results (range-halving):");
            for (int result : rangeResults) {
                rangeBuilder.append(' ').append(result);
            }

            StringBuilder powersBuilder = new StringBuilder("Boundary results (powers-of-two):");
            for (int result : powersResults) {
                powersBuilder.append(' ').append(result);
            }

            System.out.println(rangeBuilder);
            System.out.println(powersBuilder);
        } catch (IllegalArgumentException error) {
            System.err.println(error.getMessage());
            System.exit(1);
        } catch (IOException error) {
            System.err.println("Failed to open input file: " + error.getMessage());
            System.exit(1);
        }
    }
}
