public final class TernarySearch {
    private TernarySearch() {}

    public static final class Result {
        private final int index;
        private final long value;

        public Result(int index, long value) {
            this.index = index;
            this.value = value;
        }

        public int index() {
            return index;
        }

        public long value() {
            return value;
        }
    }

    public static Result findUnimodalMaximum(long[] values) {
        if (values.length == 0) {
            throw new IllegalArgumentException("ternary search requires a non-empty array");
        }

        int left = 0;
        int right = values.length - 1;

        while (right > left + 3) {
            int third = (right - left) / 3;
            int mid1 = left + third;
            int mid2 = right - third;

            if (values[mid1] < values[mid2]) {
                left = mid1 + 1;
            } else if (values[mid1] > values[mid2]) {
                right = mid2 - 1;
            } else {
                left = mid1;
                right = mid2;
            }
        }

        int bestIndex = left;
        for (int index = left + 1; index <= right; index++) {
            if (values[index] > values[bestIndex]) {
                bestIndex = index;
            }
        }

        return new Result(bestIndex, values[bestIndex]);
    }
}
