import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Main {
    private static final long MIN_I64 = Long.MIN_VALUE;
    private static final long MAX_I64 = Long.MAX_VALUE;

    private record InputData(List<Long> values, int windowSize) {}

    private static final class FastScanner {
        private final InputStream input;
        private final byte[] buffer = new byte[1 << 16];
        private int length = 0;
        private int index = 0;

        private FastScanner(InputStream input) {
            this.input = input;
        }

        private int read() throws IOException {
            if (index >= length) {
                length = input.read(buffer);
                index = 0;
                if (length <= 0) {
                    return -1;
                }
            }
            return buffer[index++];
        }

        private String nextToken() throws IOException {
            StringBuilder builder = new StringBuilder();
            int current = read();
            while (current != -1 && Character.isWhitespace(current)) {
                current = read();
            }
            if (current == -1) {
                return null;
            }
            while (current != -1 && !Character.isWhitespace(current)) {
                builder.append((char) current);
                current = read();
            }
            return builder.toString();
        }
    }

    private static InputData readInput(Path inputPath) throws IOException {
        try (InputStream stream = new BufferedInputStream(java.nio.file.Files.newInputStream(inputPath))) {
            FastScanner scanner = new FastScanner(stream);
            String nToken = scanner.nextToken();
            String windowSizeToken = scanner.nextToken();
            if (nToken == null || windowSizeToken == null) {
                throw new IllegalArgumentException("Invalid input header.");
            }

            final int n;
            final int windowSize;
            try {
                n = Integer.parseInt(nToken);
                windowSize = Integer.parseInt(windowSizeToken);
            } catch (NumberFormatException exception) {
                throw new IllegalArgumentException("Invalid input header.");
            }

            if (n <= 0 || windowSize <= 0 || windowSize > n) {
                throw new IllegalArgumentException("Invalid input header.");
            }

            List<Long> values = new ArrayList<>(n);
            for (int index = 0; index < n; ++index) {
                String valueToken = scanner.nextToken();
                if (valueToken == null) {
                    throw new IllegalArgumentException(
                            "Failed to read array value at index " + index + ".");
                }
                try {
                    long value = Long.parseLong(valueToken);
                    if (value < MIN_I64 || value > MAX_I64) {
                        throw new NumberFormatException();
                    }
                    values.add(value);
                } catch (NumberFormatException exception) {
                    throw new IllegalArgumentException(
                            "Failed to read array value at index " + index + ".");
                }
            }

            if (scanner.nextToken() != null) {
                throw new IllegalArgumentException("Input size does not match header.");
            }

            return new InputData(values, windowSize);
        }
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
