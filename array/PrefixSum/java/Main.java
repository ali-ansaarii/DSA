import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;

public final class Main {
    private static final class Query {
        final int left;
        final int right;

        Query(int left, int right) {
            this.left = left;
            this.right = right;
        }
    }

    private static final class ProgramOptions {
        String inputPath;
        boolean benchmarkMode;
    }

    private static final class ParsedInput {
        final long[] values;
        final Query[] queries;

        ParsedInput(long[] values, Query[] queries) {
            this.values = values;
            this.queries = queries;
        }
    }

    private Main() {}

    private static ProgramOptions parseArguments(String[] args) {
        ProgramOptions options = new ProgramOptions();
        for (String argument : args) {
            if ("--time-prefix-sum".equals(argument)) {
                options.benchmarkMode = true;
            } else if (options.inputPath == null) {
                options.inputPath = argument;
            } else {
                throw new IllegalArgumentException("Usage: Main <input-file> [--time-prefix-sum]");
            }
        }

        if (options.inputPath == null) {
            throw new IllegalArgumentException("Usage: Main <input-file> [--time-prefix-sum]");
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

        if (position + valueCount + (2 * queryCount) != tokens.length) {
            throw new IllegalArgumentException("Input length does not match n and q");
        }

        long[] values = new long[valueCount];
        for (int index = 0; index < valueCount; ++index) {
            values[index] = Long.parseLong(tokens[position++]);
        }

        Query[] queries = new Query[queryCount];
        for (int index = 0; index < queryCount; ++index) {
            int left = Integer.parseInt(tokens[position++]);
            int right = Integer.parseInt(tokens[position++]);
            if (left < 0 || right < left || right >= valueCount) {
                throw new IllegalArgumentException("Query indices out of range at index " + index);
            }
            queries[index] = new Query(left, right);
        }

        return new ParsedInput(values, queries);
    }

    public static void main(String[] args) {
        try {
            ProgramOptions options = parseArguments(args);
            ParsedInput input = readInput(options.inputPath);

            long startTime = System.nanoTime();
            long[] prefix = PrefixSum.buildPrefixSums(input.values);
            if (prefix == null) {
                System.err.println("Overflow detected while building prefix sums");
                System.exit(1);
            }

            long[] results = new long[input.queries.length];
            for (int index = 0; index < input.queries.length; ++index) {
                Long total = PrefixSum.rangeSum(prefix, input.queries[index].left, input.queries[index].right);
                if (total == null) {
                    System.err.println("Overflow detected while answering a range query");
                    System.exit(1);
                }
                results[index] = total;
            }
            double elapsedMs = (System.nanoTime() - startTime) / 1_000_000.0;

            if (options.benchmarkMode) {
                System.out.printf(Locale.US, "Prefix-sum time: %.3f ms%n", elapsedMs);
                return;
            }

            StringBuilder builder = new StringBuilder("Range-sum results:");
            for (long result : results) {
                builder.append(' ').append(result);
            }
            System.out.println(builder);
        } catch (IllegalArgumentException error) {
            System.err.println(error.getMessage());
            System.exit(1);
        } catch (IOException error) {
            System.err.println("Failed to open input file: " + error.getMessage());
            System.exit(1);
        }
    }
}
