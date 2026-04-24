import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Main {
    private record ParsedInput(long[] values, long target) {}

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
        long target;
        try {
            n = Integer.parseInt(tokens.get(0));
            target = Long.parseLong(tokens.get(1));
        } catch (NumberFormatException exception) {
            throw new IllegalArgumentException("Invalid input header.");
        }

        if (n <= 0 || target <= 0) {
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
            if (values[index] <= 0) {
                throw new IllegalArgumentException("Variable-size sliding window requires positive values.");
            }
        }

        return new ParsedInput(values, target);
    }

    public static void main(String[] args) {
        String inputPath = "inputs/input.txt";
        boolean timeVariableWindow = false;

        for (String argument : args) {
            if ("--time-variable-window".equals(argument)) {
                timeVariableWindow = true;
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
        SlidingWindow.Result result = SlidingWindow.minWindowAtLeastTarget(parsedInput.values(), parsedInput.target());
        long elapsedNs = System.nanoTime() - start;

        if (result == null) {
            System.err.println("Overflow while evaluating variable-size windows.");
            System.exit(1);
            return;
        }

        if (timeVariableWindow) {
            System.out.printf("Variable-window time: %.3f ms%n", elapsedNs / 1_000_000.0);
        } else if (result.bestLength() == -1) {
            System.out.println("No valid window");
        } else {
            System.out.printf("Minimum window length: %d%n", result.bestLength());
            System.out.printf("Minimum window range: %d %d%n", result.bestLeft(), result.bestRight());
        }
    }
}
