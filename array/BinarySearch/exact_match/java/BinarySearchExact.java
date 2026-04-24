public final class BinarySearchExact {
    private BinarySearchExact() {}

    public static int binarySearchExact(long[] values, long target) {
        int left = 0;
        int right = values.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (values[mid] == target) {
                return mid;
            }

            if (values[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return -1;
    }
}
