public final class SlidingWindow {
    private SlidingWindow() {}

    private static boolean addOverflow(long a, long b) {
        return (b > 0 && a > Long.MAX_VALUE - b) || (b < 0 && a < Long.MIN_VALUE - b);
    }

    private static boolean subOverflow(long a, long b) {
        return (b < 0 && a > Long.MAX_VALUE + b) || (b > 0 && a < Long.MIN_VALUE + b);
    }

    public static Result minWindowAtLeastTarget(long[] values, long target) {
        long windowSum = 0;
        int left = 0;
        int bestLength = -1;
        int bestLeft = -1;
        int bestRight = -1;

        for (int right = 0; right < values.length; right++) {
            if (addOverflow(windowSum, values[right])) {
                return null;
            }
            windowSum += values[right];

            while (windowSum >= target) {
                int currentLength = right - left + 1;
                if (bestLength == -1 || currentLength < bestLength) {
                    bestLength = currentLength;
                    bestLeft = left;
                    bestRight = right;
                }

                if (subOverflow(windowSum, values[left])) {
                    return null;
                }
                windowSum -= values[left];
                left++;
            }
        }

        return new Result(bestLength, bestLeft, bestRight);
    }

    public record Result(int bestLength, int bestLeft, int bestRight) {}
}
