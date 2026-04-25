import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean time_flag_time_selection_sort = false;

        for (String argument : args) {
            if (argument.equals("--time-selection-sort")) {
                time_flag_time_selection_sort = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        try {
            int[] values = readInput(inputPath);

            if (time_flag_time_selection_sort) {
                long start = System.nanoTime();
                SelectionSort.selectionSort(values);
                long elapsed = System.nanoTime() - start;
                System.err.printf("algorithm_time_ms=%.6f%n", elapsed / 1_000_000.0);
            } else {
                SelectionSort.selectionSort(values);
            }

            System.out.println(formatValues(values));
        } catch (Exception error) {
            System.err.println("Error: " + error.getMessage());
            System.exit(1);
        }
    }

    private static int[] readInput(Path inputPath) throws IOException {
        String content = Files.readString(inputPath);
        String[] tokens = content.trim().isEmpty() ? new String[0] : content.trim().split("\\s+");
        if (tokens.length == 0) {
            throw new IllegalArgumentException("input must start with the array length");
        }

        int n = Integer.parseInt(tokens[0]);
        if (n < 0) {
            throw new IllegalArgumentException("array length must be non-negative");
        }
        if (tokens.length - 1 < n) {
            throw new IllegalArgumentException("input ended before reading all array values");
        }

        int[] values = new int[n];
        for (int i = 0; i < n; i++) {
            values[i] = Integer.parseInt(tokens[i + 1]);
        }
        return values;
    }

    private static String formatValues(int[] values) {
        List<String> parts = new ArrayList<>(values.length);
        for (int value : values) {
            parts.add(Integer.toString(value));
        }
        return String.join(" ", parts);
    }
}
