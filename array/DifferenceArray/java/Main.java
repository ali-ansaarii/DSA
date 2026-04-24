import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Main {
    private record Update(int left, int right, long delta) {}

    private record ParsedInput(long[] values, List<Update> updates) {}

    private static ParsedInput readInput(String inputPath) throws IOException {
        List<String> tokens = Files.readAllLines(Path.of(inputPath)).stream()
                .flatMap(line -> List.of(line.trim().split("\\s+")).stream())
                .filter(token -> !token.isEmpty())
                .toList();

        if (tokens.size() < 2) {
            throw new IllegalArgumentException("Invalid input header.");
        }

        int n = Integer.parseInt(tokens.get(0));
        int q = Integer.parseInt(tokens.get(1));
        if (n < 0 || q < 0) {
            throw new IllegalArgumentException("Invalid input header.");
        }

        int expected = 2 + n + 3 * q;
        if (tokens.size() != expected) {
            throw new IllegalArgumentException("Input size does not match header.");
        }

        long[] values = new long[n];
        for (int index = 0; index < n; index++) {
            values[index] = Long.parseLong(tokens.get(2 + index));
        }

        List<Update> updates = new ArrayList<>(q);
        int cursor = 2 + n;
        for (int index = 0; index < q; index++) {
            int left = Integer.parseInt(tokens.get(cursor));
            int right = Integer.parseInt(tokens.get(cursor + 1));
            long delta = Long.parseLong(tokens.get(cursor + 2));
            cursor += 3;

            if (left < 0 || right < left || right >= n) {
                throw new IllegalArgumentException("Invalid update range.");
            }

            updates.add(new Update(left, right, delta));
        }

        return new ParsedInput(values, updates);
    }

    private static long[] runDifferenceArray(long[] values, List<Update> updates) {
        long[] diff = DifferenceArray.buildDifferenceArray(values);
        if (diff == null) {
            System.err.println("Overflow while building the difference array.");
            return null;
        }

        for (Update update : updates) {
            if (!DifferenceArray.applyRangeAdd(diff, update.left(), update.right(), update.delta())) {
                System.err.println("Overflow while applying a range update.");
                return null;
            }
        }

        long[] finalValues = DifferenceArray.reconstructValues(diff);
        if (finalValues == null) {
            System.err.println("Overflow while reconstructing the final array.");
            return null;
        }
        return finalValues;
    }

    private static void printValues(long[] values) {
        StringBuilder builder = new StringBuilder("Final array:");
        for (long value : values) {
            builder.append(' ').append(value);
        }
        System.out.println(builder);
    }

    public static void main(String[] args) {
        String inputPath = "inputs/input.txt";
        boolean timeDifferenceArray = false;

        for (String argument : args) {
            if ("--time-difference-array".equals(argument)) {
                timeDifferenceArray = true;
            } else {
                inputPath = argument;
            }
        }

        ParsedInput parsedInput;
        try {
            parsedInput = readInput(inputPath);
        } catch (IOException exception) {
            System.err.printf("Failed to open input file: %s%n", inputPath);
            System.exit(1);
            return;
        } catch (IllegalArgumentException exception) {
            System.err.println(exception.getMessage());
            System.exit(1);
            return;
        }

        long start = System.nanoTime();
        long[] finalValues = runDifferenceArray(parsedInput.values(), parsedInput.updates());
        long elapsedNs = System.nanoTime() - start;

        if (finalValues == null) {
            System.exit(1);
            return;
        }

        if (timeDifferenceArray) {
            System.out.printf("Difference-array time: %.3f ms%n", elapsedNs / 1_000_000.0);
        } else {
            printValues(finalValues);
        }
    }
}
