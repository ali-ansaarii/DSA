public final class DifferenceArray {
    private static final long MIN_I64 = Long.MIN_VALUE;
    private static final long MAX_I64 = Long.MAX_VALUE;

    private DifferenceArray() {}

    private static boolean addOverflow(long a, long b) {
        return (b > 0 && a > MAX_I64 - b) || (b < 0 && a < MIN_I64 - b);
    }

    private static boolean subOverflow(long a, long b) {
        return (b < 0 && a > MAX_I64 + b) || (b > 0 && a < MIN_I64 + b);
    }

    public static long[] buildDifferenceArray(long[] values) {
        long[] diff = new long[values.length];
        if (values.length == 0) {
            return diff;
        }

        diff[0] = values[0];
        for (int index = 1; index < values.length; index++) {
            if (subOverflow(values[index], values[index - 1])) {
                return null;
            }
            diff[index] = values[index] - values[index - 1];
        }
        return diff;
    }

    public static boolean applyRangeAdd(long[] diff, int left, int right, long delta) {
        if (addOverflow(diff[left], delta)) {
            return false;
        }
        diff[left] += delta;

        if (right + 1 < diff.length) {
            if (subOverflow(diff[right + 1], delta)) {
                return false;
            }
            diff[right + 1] -= delta;
        }

        return true;
    }

    public static long[] reconstructValues(long[] diff) {
        long[] values = new long[diff.length];
        if (diff.length == 0) {
            return values;
        }

        values[0] = diff[0];
        for (int index = 1; index < diff.length; index++) {
            if (addOverflow(values[index - 1], diff[index])) {
                return null;
            }
            values[index] = values[index - 1] + diff[index];
        }
        return values;
    }
}
