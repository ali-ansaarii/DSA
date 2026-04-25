import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;

public final class Main {
    private Main() {}

    private static long[] readInput(Path inputPath) throws IOException {
        String content = Files.readString(inputPath);
        String[] tokens = content.trim().isEmpty() ? new String[0] : content.trim().split("\\s+");

        if (tokens.length == 0) {
            throw new IllegalArgumentException("input must start with the number of elements");
        }

        long nValue = Long.parseLong(tokens[0]);
        if (nValue < 0) {
            throw new IllegalArgumentException("number of elements must be nonnegative");
        }
        if (nValue > Integer.MAX_VALUE) {
            throw new IllegalArgumentException("number of elements is too large for this Java runner");
        }

        int n = (int) nValue;
        if (tokens.length - 1 < n) {
            throw new IllegalArgumentException("input ended before all elements were read");
        }

        long[] values = new long[n];
        for (int i = 0; i < n; i++) {
            values[i] = Long.parseLong(tokens[i + 1]);
        }

        return values;
    }

    private static void printValues(long[] values) {
        StringBuilder output = new StringBuilder();
        for (int i = 0; i < values.length; i++) {
            if (i > 0) {
                output.append(' ');
            }
            output.append(values[i]);
        }
        System.out.println(output);
    }

    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean time_flag_time_insertion_sort = false;

        for (String argument : args) {
            if (argument.equals("--time-insertion-sort")) {
                time_flag_time_insertion_sort = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        try {
            long[] values = readInput(inputPath);

            if (time_flag_time_insertion_sort) {
                long start = System.nanoTime();
                InsertionSort.insertionSort(values);
                long elapsedMicroseconds = (System.nanoTime() - start) / 1_000L;
                System.err.printf(Locale.ROOT, "algorithm_time_microseconds=%d%n", elapsedMicroseconds);
            } else {
                InsertionSort.insertionSort(values);
            }

            printValues(values);
        } catch (Exception error) {
            System.err.println("error: " + error.getMessage());
            System.exit(1);
        }
    }
}
