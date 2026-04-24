import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;

public final class Main {
    private static final class ProgramOptions {
        String inputPath;
        boolean benchmarkMode;
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
            if ("--time-exact".equals(argument)) {
                options.benchmarkMode = true;
            } else if (options.inputPath == null) {
                options.inputPath = argument;
            } else {
                throw new IllegalArgumentException("Usage: Main <input-file> [--time-exact]");
            }
        }

        if (options.inputPath == null) {
            throw new IllegalArgumentException("Usage: Main <input-file> [--time-exact]");
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

            int[] results = new int[input.queries.length];
            long startTime = System.nanoTime();
            for (int index = 0; index < input.queries.length; ++index) {
                results[index] = BinarySearchExact.binarySearchExact(input.values, input.queries[index]);
            }
            double elapsedMs = (System.nanoTime() - startTime) / 1_000_000.0;

            if (options.benchmarkMode) {
                System.out.printf(Locale.US, "Exact binary search time: %.3f ms%n", elapsedMs);
                return;
            }

            StringBuilder builder = new StringBuilder("Exact-match results:");
            for (int result : results) {
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
