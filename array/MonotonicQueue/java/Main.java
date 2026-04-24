import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Main {
    private static final long MIN_I64 = Long.MIN_VALUE;
    private static final long MAX_I64 = Long.MAX_VALUE;

    private record InputData(List<Long> values, int windowSize) {}

    private static InputData readInput(Path inputPath) throws IOException {
        List<String> tokens = Files.readAllLines(inputPath)
                .stream()
                .flatMap(line -> List.of(line.trim().split("\\s+")).stream())
                .filter(token -> !token.isEmpty())
                .toList();

        if (tokens.size() < 2) {
            throw new IllegalArgumentException("Invalid input header.");
        }

        final int n;
        final int windowSize;
        try {
            n = Integer.parseInt(tokens.get(0));
            windowSize = Integer.parseInt(tokens.get(1));
        } catch (NumberFormatException exception) {
            throw new IllegalArgumentException("Invalid input header.");
        }

        if (n <= 0 || windowSize <= 0 || windowSize > n) {
            throw new IllegalArgumentException("Invalid input header.");
        }

        if (tokens.size() != n + 2) {
            throw new IllegalArgumentException("Input size does not match header.");
        }

        List<Long> values = new ArrayList<>(n);
        for (int index = 0; index < n; ++index) {
            try {
                long value = Long.parseLong(tokens.get(index + 2));
                if (value < MIN_I64 || value > MAX_I64) {
                    throw new NumberFormatException();
                }
                values.add(value);
            } catch (NumberFormatException exception) {
                throw new IllegalArgumentException(
                        "Failed to read array value at index " + index + ".");
            }
        }

        return new InputData(values, windowSize);
    }

    private static void printAnswer(List<Long> maxima) {
        StringBuilder builder = new StringBuilder("Window maxima:");
        for (long value : maxima) {
            builder.append(' ').append(value);
        }
        System.out.println(builder);
    }

    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean timeMonotonicQueue = false;

        for (String argument : args) {
            if (argument.equals("--time-monotonic-queue")) {
                timeMonotonicQueue = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        final InputData inputData;
        try {
            inputData = readInput(inputPath);
        } catch (IOException exception) {
            System.err.println("Failed to open input file: " + inputPath);
            System.exit(1);
            return;
        } catch (IllegalArgumentException exception) {
            System.err.println(exception.getMessage());
            System.exit(1);
            return;
        }

        long start = System.nanoTime();
        List<Long> maxima =
                MonotonicQueue.slidingWindowMaximum(inputData.values(), inputData.windowSize());
        long end = System.nanoTime();

        if (timeMonotonicQueue) {
            double elapsedMs = (end - start) / 1_000_000.0;
            System.out.printf("Monotonic-queue time: %.6f ms%n", elapsedMs);
        } else {
            printAnswer(maxima);
        }
    }
}
