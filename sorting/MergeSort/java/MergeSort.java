public final class MergeSort {
    private MergeSort() {}

    public static long[] mergeSort(long[] values) {
        long[] sorted = values.clone();
        long[] buffer = new long[sorted.length];
        mergeSortRecursive(sorted, buffer, 0, sorted.length);
        return sorted;
    }

    private static void mergeSortRecursive(long[] values, long[] buffer, int left, int right) {
        if (right - left <= 1) {
            return;
        }

        int mid = left + (right - left) / 2;
        mergeSortRecursive(values, buffer, left, mid);
        mergeSortRecursive(values, buffer, mid, right);
        mergeRanges(values, buffer, left, mid, right);
    }

    private static void mergeRanges(long[] values, long[] buffer, int left, int mid, int right) {
        int i = left;
        int j = mid;
        int k = left;

        while (i < mid && j < right) {
            if (values[i] <= values[j]) {
                buffer[k++] = values[i++];
            } else {
                buffer[k++] = values[j++];
            }
        }

        while (i < mid) {
            buffer[k++] = values[i++];
        }

        while (j < right) {
            buffer[k++] = values[j++];
        }

        System.arraycopy(buffer, left, values, left, right - left);
    }
}
