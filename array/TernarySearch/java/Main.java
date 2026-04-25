import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Main {
    private Main() {}

    private static long[] readInput(Path inputPath) throws IOException {
        String content = Files.readString(inputPath);
        String[] rawTokens = content.trim().isEmpty() ? new String[0] : content.trim().split("\\s+");
        if (rawTokens.length == 0) {
            throw new IllegalArgumentException("input must start with a positive element count");
        }

        int n = Integer.parseInt(rawTokens[0]);
        if (n <= 0) {
            throw new IllegalArgumentException("input must start with a positive element count");
        }
        if (rawTokens.length - 1 < n) {
            throw new IllegalArgumentException("input ended before all array values were read");
        }

        List<Long> values = new ArrayList<>(n);
        for (int i = 0; i < n; i++) {
            values.add(Long.parseLong(rawTokens[i + 1]));
        }

        long[] array = new long[n];
        for (int i = 0; i < n; i++) {
            array[i] = values.get(i);
        }
        return array;
    }

    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean timeTernarySearch = false;

        for (String argument : args) {
            if (argument.equals("--time-ternary-search")) {
                timeTernarySearch = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        try {
            long[] values = readInput(inputPath);

            TernarySearch.Result result;
            long elapsedNanoseconds = 0L;
            if (timeTernarySearch) {
                long start = System.nanoTime();
                result = TernarySearch.findUnimodalMaximum(values);
                elapsedNanoseconds = System.nanoTime() - start;
            } else {
                result = TernarySearch.findUnimodalMaximum(values);
            }

            System.out.println("Maximum index: " + result.index());
            System.out.println("Maximum value: " + result.value());
            if (timeTernarySearch) {
                System.out.println("Algorithm time (ns): " + elapsedNanoseconds);
            }
        } catch (IOException | IllegalArgumentException error) {
            System.err.println("Error: " + error.getMessage());
            System.exit(1);
        }
    }
}
