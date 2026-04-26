import java.util.ArrayList;
import java.util.List;

public final class PrefixSum2D {
    private final long[][] prefix;

    public PrefixSum2D(long[][] matrix) {
        int rows = matrix.length;
        int cols = rows == 0 ? 0 : matrix[0].length;
        this.prefix = new long[rows + 1][cols + 1];

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                prefix[r + 1][c + 1] = matrix[r][c]
                                      + prefix[r][c + 1]
                                      + prefix[r + 1][c]
                                      - prefix[r][c];
            }
        }
    }

    public long rectangleSum(int r1, int c1, int r2, int c2) {
        return prefix[r2 + 1][c2 + 1]
             - prefix[r1][c2 + 1]
             - prefix[r2 + 1][c1]
             + prefix[r1][c1];
    }

    public static List<Long> answerRectangleQueries(long[][] matrix, List<RectQuery> queries) {
        PrefixSum2D prefixSum = new PrefixSum2D(matrix);
        List<Long> answers = new ArrayList<>(queries.size());
        for (RectQuery query : queries) {
            answers.add(prefixSum.rectangleSum(query.r1, query.c1, query.r2, query.c2));
        }
        return answers;
    }

    public static final class RectQuery {
        public final int r1;
        public final int c1;
        public final int r2;
        public final int c2;

        public RectQuery(int r1, int c1, int r2, int c2) {
            this.r1 = r1;
            this.c1 = c1;
            this.r2 = r2;
            this.c2 = c2;
        }
    }
}
