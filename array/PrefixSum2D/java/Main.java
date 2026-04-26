import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Main {
    private static final class ParsedInput {
        final long[][] matrix;
        final List<PrefixSum2D.RectQuery> queries;

        ParsedInput(long[][] matrix, List<PrefixSum2D.RectQuery> queries) {
            this.matrix = matrix;
            this.queries = queries;
        }
    }

    private static final class FastScanner {
        private final byte[] data;
        private int index = 0;

        FastScanner(Path path) throws IOException {
            this.data = Files.readAllBytes(path);
        }

        long nextLong() {
            while (index < data.length && data[index] <= ' ') {
                index++;
            }

            int sign = 1;
            if (data[index] == '-') {
                sign = -1;
                index++;
            }

            long value = 0;
            while (index < data.length && data[index] > ' ') {
                value = value * 10 + (data[index] - '0');
                index++;
            }
            return sign * value;
        }

        int nextInt() {
            return (int) nextLong();
        }
    }

    private static ParsedInput parseInput(Path inputPath) throws IOException {
        FastScanner scanner = new FastScanner(inputPath);
        int rows = scanner.nextInt();
        int cols = scanner.nextInt();

        long[][] matrix = new long[rows][cols];
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                matrix[r][c] = scanner.nextLong();
            }
        }

        int queryCount = scanner.nextInt();
        List<PrefixSum2D.RectQuery> queries = new ArrayList<>(queryCount);
        for (int i = 0; i < queryCount; i++) {
            int r1 = scanner.nextInt();
            int c1 = scanner.nextInt();
            int r2 = scanner.nextInt();
            int c2 = scanner.nextInt();
            queries.add(new PrefixSum2D.RectQuery(r1, c1, r2, c2));
        }

        return new ParsedInput(matrix, queries);
    }

    public static void main(String[] args) throws IOException {
        Path inputPath = Path.of("inputs/input.txt");
        boolean time_flag_time_prefix_sum_2d = false;

        for (String argument : args) {
            if (argument.equals("--time-prefix-sum-2d")) {
                time_flag_time_prefix_sum_2d = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        ParsedInput parsedInput = parseInput(inputPath);

        long start = System.nanoTime();
        List<Long> answers = PrefixSum2D.answerRectangleQueries(parsedInput.matrix, parsedInput.queries);
        long stop = System.nanoTime();

        if (time_flag_time_prefix_sum_2d) {
            double elapsedMs = (stop - start) / 1_000_000.0;
            System.err.printf("algorithm_time_ms %.3f%n", elapsedMs);
        }

        StringBuilder output = new StringBuilder();
        for (long answer : answers) {
            output.append(answer).append('\n');
        }
        System.out.print(output);
    }
}
