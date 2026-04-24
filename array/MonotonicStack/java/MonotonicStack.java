public final class MonotonicStack {
    private MonotonicStack() {}

    public static long[] nextGreaterElements(long[] values) {
        long[] answer = new long[values.length];
        java.util.Arrays.fill(answer, -1L);

        long[] stack = new long[values.length];
        int size = 0;

        for (int index = values.length - 1; index >= 0; index--) {
            while (size > 0 && stack[size - 1] <= values[index]) {
                size--;
            }
            if (size > 0) {
                answer[index] = stack[size - 1];
            }
            stack[size++] = values[index];
        }

        return answer;
    }
}
