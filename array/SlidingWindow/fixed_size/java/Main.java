import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Main {
    private record ParsedInput(long[] values, int k) {}

    private static ParsedInput readInput(String inputPath) throws IOException {
        String content = Files.readString(Path.of(inputPath));
        String[] rawTokens = content.trim().split("\\s+");
        List<String> tokens = new ArrayList<>();
        for (String token : rawTokens) {
            if (!token.isEmpty()) {
                tokens.add(token);
            }
        }

        if (tokens.size() < 2) {
            throw new IllegalArgumentException("Invalid input header.");
        }

        int n;
        int k;
        try {
            n = Integer.parseInt(tokens.get(0));
            k = Integer.parseInt(tokens.get(1));
        } catch (NumberFormatException exception) {
            throw new IllegalArgumentException("Invalid input header.");
        }

        if (n <= 0 || k <= 0 || k > n) {
            throw new IllegalArgumentException("Invalid input header.");
        }

        if (tokens.size() != 2 + n) {
            throw new IllegalArgumentException("Input size does not match header.");
        }

        long[] values = new long[n];
        for (int index = 0; index < n; index++) {
            try {
                values[index] = Long.parseLong(tokens.get(2 + index));
            } catch (NumberFormatException exception) {
                throw new IllegalArgumentException("Invalid array value.");
            }
        }

        return new ParsedInput(values, k);
    }

    public static void main(String[] args) {
        String inputPath = "inputs/input.txt";
        boolean timeFixedWindow = false;

        for (String argument : args) {
            if ("--time-fixed-window".equals(argument)) {
                timeFixedWindow = true;
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
        SlidingWindow.Result result = SlidingWindow.bestFixedWindow(parsedInput.values(), parsedInput.k());
        long elapsedNs = System.nanoTime() - start;

        if (result == null) {
            System.err.println("Overflow while evaluating fixed-size windows.");
            System.exit(1);
            return;
        }

        if (timeFixedWindow) {
            System.out.printf("Fixed-window time: %.3f ms%n", elapsedNs / 1_000_000.0);
        } else {
            System.out.printf("Best window sum: %d%n", result.bestSum());
            System.out.printf("Best window range: %d %d%n", result.bestLeft(), result.bestRight());
        }
    }
}
