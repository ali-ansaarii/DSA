public final class SlidingWindow {
    private SlidingWindow() {}

    private static boolean addOverflow(long a, long b) {
        return (b > 0 && a > Long.MAX_VALUE - b) || (b < 0 && a < Long.MIN_VALUE - b);
    }

    private static boolean subOverflow(long a, long b) {
        return (b < 0 && a > Long.MAX_VALUE + b) || (b > 0 && a < Long.MIN_VALUE + b);
    }

    public static Result bestFixedWindow(long[] values, int k) {
        long windowSum = 0;
        for (int index = 0; index < k; index++) {
            if (addOverflow(windowSum, values[index])) {
                return null;
            }
            windowSum += values[index];
        }

        long bestSum = windowSum;
        int bestLeft = 0;
        int bestRight = k - 1;

        for (int right = k; right < values.length; right++) {
            if (subOverflow(windowSum, values[right - k])) {
                return null;
            }
            windowSum -= values[right - k];
            if (addOverflow(windowSum, values[right])) {
                return null;
            }
            windowSum += values[right];

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
