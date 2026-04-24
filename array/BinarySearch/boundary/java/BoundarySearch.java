public final class BoundarySearch {
    private BoundarySearch() {}

    public static int lowerBoundRangeHalving(long[] values, long target) {
        int left = 0;
        int right = values.length;

        while (left < right) {
            int mid = left + (right - left) / 2;
            if (values[mid] < target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        return left;
    }

    public static int lowerBoundPowersOfTwo(long[] values, long target) {
        int position = -1;
        int step = 1;
        while (step < values.length) {
            step <<= 1;
        }

        for (; step > 0; step >>= 1) {
            int next = position + step;
            if (next < values.length && values[next] < target) {
                position = next;
            }
        }

        return position + 1;
    }
}
