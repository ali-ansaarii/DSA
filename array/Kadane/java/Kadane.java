public final class Kadane {
    private Kadane() {}

    public static final class Result {
        public final long maximumSum;
        public final int startIndex;
        public final int endIndex;

        public Result(long maximumSum, int startIndex, int endIndex) {
            this.maximumSum = maximumSum;
            this.startIndex = startIndex;
            this.endIndex = endIndex;
        }
    }

    public static Result maxSubarrayKadane(long[] values) {
        if (values.length == 0) {
            throw new IllegalArgumentException("Kadane's Algorithm requires a non-empty array");
        }

        long currentSum = values[0];
        long bestSum = values[0];
        int currentStart = 0;
        int bestStart = 0;
        int bestEnd = 0;

        for (int i = 1; i < values.length; i++) {
            long extendedSum = currentSum + values[i];

            if (extendedSum < values[i]) {
                currentSum = values[i];
                currentStart = i;
            } else {
                currentSum = extendedSum;
            }

            if (currentSum > bestSum) {
                bestSum = currentSum;
                bestStart = currentStart;
                bestEnd = i;
            }
        }

        return new Result(bestSum, bestStart, bestEnd);
    }
}
