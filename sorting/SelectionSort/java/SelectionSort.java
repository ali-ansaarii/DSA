public final class SelectionSort {
    private SelectionSort() {}

    public static void selectionSort(int[] values) {
        for (int i = 0; i < values.length; i++) {
            int minIndex = i;
            for (int j = i + 1; j < values.length; j++) {
                if (values[j] < values[minIndex]) {
                    minIndex = j;
                }
            }

            if (minIndex != i) {
                int temporary = values[i];
                values[i] = values[minIndex];
                values[minIndex] = temporary;
            }
        }
    }
}
