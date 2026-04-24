import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Main {
    private static long[] readInput(String inputPath) throws IOException {
        String content = Files.readString(Path.of(inputPath));
        String[] rawTokens = content.trim().split("\\s+");
        List<String> tokens = new ArrayList<>();
        for (String token : rawTokens) {
            if (!token.isEmpty()) {
                tokens.add(token);
            }
        }

        if (tokens.isEmpty()) {
            throw new IllegalArgumentException("Invalid input header.");
        }

        int n;
        try {
            n = Integer.parseInt(tokens.get(0));
        } catch (NumberFormatException exception) {
            throw new IllegalArgumentException("Invalid input header.");
        }

        if (n <= 0) {
            throw new IllegalArgumentException("Invalid input header.");
        }

        if (tokens.size() != 1 + n) {
            throw new IllegalArgumentException("Input size does not match header.");
        }

        long[] values = new long[n];
        for (int index = 0; index < n; index++) {
            try {
                values[index] = Long.parseLong(tokens.get(1 + index));
            } catch (NumberFormatException exception) {
                throw new IllegalArgumentException("Invalid array value.");
            }
        }

        return values;
    }

    public static void main(String[] args) {
        String inputPath = "inputs/input.txt";
        boolean timeMonotonicStack = false;

        for (String argument : args) {
            if ("--time-monotonic-stack".equals(argument)) {
                timeMonotonicStack = true;
            } else {
                inputPath = argument;
            }
        }

        long[] values;
        try {
            values = readInput(inputPath);
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
        long[] answer = MonotonicStack.nextGreaterElements(values);
        long elapsedNs = System.nanoTime() - start;

        if (timeMonotonicStack) {
            System.out.printf("Monotonic-stack time: %.3f ms%n", elapsedNs / 1_000_000.0);
        } else {
            StringBuilder builder = new StringBuilder("Next greater elements:");
            for (long value : answer) {
                builder.append(' ').append(value);
            }
            System.out.println(builder);
        }
    }
}
