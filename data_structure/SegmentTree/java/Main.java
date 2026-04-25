import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Main {
    private record InputData(List<Long> initialValues, List<Query> queries) {}

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
            String qToken = scanner.nextToken();
            if (nToken == null || qToken == null) {
                throw new IllegalArgumentException("Invalid input header.");
            }

            final int n;
            final int q;
            try {
                n = Integer.parseInt(nToken);
                q = Integer.parseInt(qToken);
            } catch (NumberFormatException exception) {
                throw new IllegalArgumentException("Invalid input header.");
            }

            if (n <= 0 || q < 0) {
                throw new IllegalArgumentException("Invalid input header.");
            }

            List<Long> initialValues = new ArrayList<>(n);
            for (int index = 0; index < n; ++index) {
                String token = scanner.nextToken();
                if (token == null) {
                    throw new IllegalArgumentException(
                            "Failed to read initial value at index " + index + ".");
                }
                try {
                    initialValues.add(Long.parseLong(token));
                } catch (NumberFormatException exception) {
                    throw new IllegalArgumentException(
                            "Failed to read initial value at index " + index + ".");
                }
            }

            List<Query> queries = new ArrayList<>(q);
            for (int lineIndex = 0; lineIndex < q; ++lineIndex) {
                int operationLine = n + lineIndex + 2;
                String operation = scanner.nextToken();
                if (operation == null) {
                    throw new IllegalArgumentException("Input ended early. Expected " + q + " operations.");
                }

                if (operation.equals("add")) {
                    String indexToken = scanner.nextToken();
                    String deltaToken = scanner.nextToken();
                    if (indexToken == null || deltaToken == null) {
                        throw new IllegalArgumentException(
                                "Invalid operation at line " + operationLine + ".");
                    }

                    final int index;
                    final long delta;
                    try {
                        index = Integer.parseInt(indexToken);
                        delta = Long.parseLong(deltaToken);
                    } catch (NumberFormatException exception) {
                        throw new IllegalArgumentException(
                                "Invalid operation at line " + operationLine + ".");
                    }

                    if (index < 0 || index >= n) {
                        throw new IllegalArgumentException(
                                "Invalid operation at line " + operationLine + ".");
                    }

                    queries.add(new Query(QueryType.ADD, index, -1, delta));
                } else if (operation.equals("sum")) {
                    String leftToken = scanner.nextToken();
                    String rightToken = scanner.nextToken();
                    if (leftToken == null || rightToken == null) {
                        throw new IllegalArgumentException(
                                "Invalid operation at line " + operationLine + ".");
                    }

                    final int left;
                    final int right;
                    try {
                        left = Integer.parseInt(leftToken);
                        right = Integer.parseInt(rightToken);
                    } catch (NumberFormatException exception) {
                        throw new IllegalArgumentException(
                                "Invalid operation at line " + operationLine + ".");
                    }

                    if (left < 0 || right < left || right >= n) {
                        throw new IllegalArgumentException(
                                "Invalid operation at line " + operationLine + ".");
                    }

                    queries.add(new Query(QueryType.SUM, left, right, 0));
                } else {
                    throw new IllegalArgumentException(
                            "Invalid operation at line " + operationLine + ".");
                }
            }

            if (scanner.nextToken() != null) {
                throw new IllegalArgumentException("Input size does not match header.");
            }

            return new InputData(initialValues, queries);
        }
    }

    private static void printAnswer(List<Long> results) {
        System.out.println("Query sums:");
        for (long value : results) {
            System.out.println(value);
        }
    }

    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean timeSegmentTree = false;

        for (String argument : args) {
            if (argument.equals("--time-segment-tree")) {
                timeSegmentTree = true;
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

        final List<Long> results;
        long start = System.nanoTime();
        try {
            results = SegmentTree.processSegmentTreeQueries(
                    inputData.initialValues(),
                    inputData.queries());
        } catch (ArithmeticException exception) {
            System.err.println("Segment tree overflowed while processing the queries.");
            System.exit(1);
            return;
        }
        long end = System.nanoTime();

        if (timeSegmentTree) {
            double elapsedMs = (end - start) / 1_000_000.0;
            System.out.printf("Segment-tree time: %.6f ms%n", elapsedMs);
        } else {
            printAnswer(results);
        }
    }
}
