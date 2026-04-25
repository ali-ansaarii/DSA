import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public final class Main {
    private Main() {}

    private static final class Parser {
        private final String[] tokens;
        private int index;

        Parser(Path inputPath) throws IOException {
            String content = Files.readString(inputPath).trim();
            this.tokens = content.isEmpty() ? new String[0] : content.split("\\s+");
            this.index = 0;
        }

        int nextInt(String description) {
            if (index >= tokens.length) {
                throw new IllegalArgumentException("failed to read " + description);
            }
            return Integer.parseInt(tokens[index++]);
        }

        long nextLong(String description) {
            if (index >= tokens.length) {
                throw new IllegalArgumentException("failed to read " + description);
            }
            return Long.parseLong(tokens[index++]);
        }
    }

    private static long[][] readMatrix(Parser parser, int rows, int cols) {
        long[][] matrix = new long[rows][cols];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = parser.nextLong("matrix value");
            }
        }
        return matrix;
    }

    private static void printMatrix(long[][] matrix) {
        int rows = matrix.length;
        int cols = rows == 0 ? 0 : matrix[0].length;
        StringBuilder output = new StringBuilder();
        output.append(rows).append(' ').append(cols).append('\n');
        for (long[] row : matrix) {
            for (int j = 0; j < cols; j++) {
                if (j > 0) {
                    output.append(' ');
                }
                output.append(row[j]);
            }
            output.append('\n');
        }
        System.out.print(output);
    }

    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean timeMatrixMultiplication = false;

        for (String argument : args) {
            if (argument.equals("--time-matrix-multiplication")) {
                timeMatrixMultiplication = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        try {
            Parser parser = new Parser(inputPath);
            int m = parser.nextInt("first matrix row count");
            int n = parser.nextInt("first matrix column count");
            long[][] left = readMatrix(parser, m, n);

            int n2 = parser.nextInt("second matrix row count");
            int p = parser.nextInt("second matrix column count");
            if (n != n2) {
                throw new IllegalArgumentException("matrix dimensions are incompatible");
            }
            long[][] right = readMatrix(parser, n2, p);

            long start = System.nanoTime();
            long[][] result = MatrixMultiplication.multiply(left, right);
            long finish = System.nanoTime();

            if (timeMatrixMultiplication) {
                double elapsedMillis = (finish - start) / 1_000_000.0;
                System.err.printf("matrix_multiplication_ms=%.6f%n", elapsedMillis);
            }

            printMatrix(result);
        } catch (Exception error) {
            System.err.println("error: " + error.getMessage());
            System.exit(1);
        }
    }
}
