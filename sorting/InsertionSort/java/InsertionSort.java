public final class InsertionSort {
    private InsertionSort() {}

    public static void insertionSort(long[] values) {
        for (int i = 1; i < values.length; i++) {
            long key = values[i];
            int j = i;

            while (j > 0 && values[j - 1] > key) {
                values[j] = values[j - 1];
                j--;
            }

            values[j] = key;
        }
    }
}
