import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean time_flag_time_merge_sort = false;

        for (String argument : args) {
            if (argument.equals("--time-merge-sort")) {
                time_flag_time_merge_sort = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        try {
            long[] values = readInput(inputPath);

            long[] sorted;
            if (time_flag_time_merge_sort) {
                long start = System.nanoTime();
                sorted = MergeSort.mergeSort(values);
                long end = System.nanoTime();
                System.err.printf(Locale.ROOT, "merge_sort_seconds=%.9f%n", (end - start) / 1_000_000_000.0);
            } else {
                sorted = MergeSort.mergeSort(values);
            }

            System.out.println(formatValues(sorted));
        } catch (Exception error) {
            System.err.println("Error: " + error.getMessage());
            System.exit(1);
        }
    }

    private static long[] readInput(Path inputPath) throws IOException {
        String content = Files.readString(inputPath);
        String trimmed = content.trim();
        if (trimmed.isEmpty()) {
            throw new IllegalArgumentException("input must start with the element count");
        }

        String[] tokens = trimmed.split("\\s+");
        int n = Integer.parseInt(tokens[0]);
        if (n < 0) {
            throw new IllegalArgumentException("element count cannot be negative");
        }
        if (tokens.length != n + 1) {
            throw new IllegalArgumentException("declared " + n + " elements but found " + (tokens.length - 1));
        }

        long[] values = new long[n];
        for (int i = 0; i < n; ++i) {
            values[i] = Long.parseLong(tokens[i + 1]);
        }
        return values;
    }

    private static String formatValues(long[] values) {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < values.length; ++i) {
            if (i > 0) {
                builder.append(' ');
            }
            builder.append(values[i]);
        }
        return builder.toString();
    }
}
