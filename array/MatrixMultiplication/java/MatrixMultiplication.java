public final class MatrixMultiplication {
    private MatrixMultiplication() {}

    public static long[][] multiply(long[][] left, long[][] right) {
        if (left.length == 0 || right.length == 0) {
            throw new IllegalArgumentException("matrices must be non-empty");
        }

        int rows = left.length;
        int shared = left[0].length;
        int rightRows = right.length;
        int cols = right[0].length;

        if (shared == 0 || cols == 0 || shared != rightRows) {
            throw new IllegalArgumentException("matrix dimensions are incompatible");
        }

        for (long[] row : left) {
            if (row.length != shared) {
                throw new IllegalArgumentException("left matrix rows have inconsistent lengths");
            }
        }
        for (long[] row : right) {
            if (row.length != cols) {
                throw new IllegalArgumentException("right matrix rows have inconsistent lengths");
            }
        }

        long[][] result = new long[rows][cols];
        for (int i = 0; i < rows; i++) {
            for (int k = 0; k < shared; k++) {
                long value = left[i][k];
                for (int j = 0; j < cols; j++) {
                    result[i][j] += value * right[k][j];
                }
            }
        }
        return result;
    }
}
