import java.math.BigInteger;

public final class SlidingWindow {
    private SlidingWindow() {}

    private static final BigInteger MIN_I64 = BigInteger.valueOf(Long.MIN_VALUE);
    private static final BigInteger MAX_I64 = BigInteger.valueOf(Long.MAX_VALUE);

    private static Long toLongExact(BigInteger value) {
        if (value.compareTo(MIN_I64) < 0 || value.compareTo(MAX_I64) > 0) {
            return null;
        }
        return value.longValue();
    }

    public static Result bestFixedWindow(long[] values, int k) {
        BigInteger windowSumWide = BigInteger.ZERO;
        for (int index = 0; index < k; index++) {
            windowSumWide = windowSumWide.add(BigInteger.valueOf(values[index]));
        }

        Long initialWindow = toLongExact(windowSumWide);
        if (initialWindow == null) {
            return null;
        }

        long bestSum = initialWindow;
        int bestLeft = 0;
        int bestRight = k - 1;

        for (int right = k; right < values.length; right++) {
            windowSumWide = windowSumWide
                    .subtract(BigInteger.valueOf(values[right - k]))
                    .add(BigInteger.valueOf(values[right]));

            Long windowSum = toLongExact(windowSumWide);
            if (windowSum == null) {
                return null;
            }

            int left = right - k + 1;
            if (windowSum > bestSum) {
                bestSum = windowSum;
                bestLeft = left;
                bestRight = right;
            }
        }

        return new Result(bestSum, bestLeft, bestRight);
    }

    public record Result(long bestSum, int bestLeft, int bestRight) {}
}
