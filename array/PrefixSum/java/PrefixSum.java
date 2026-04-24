public final class PrefixSum {
    private PrefixSum() {}

    private static Long checkedAdd(long left, long right) {
        if (right > 0 && left > Long.MAX_VALUE - right) {
            return null;
        }
        if (right < 0 && left < Long.MIN_VALUE - right) {
            return null;
        }
        return left + right;
    }

    private static Long checkedSub(long left, long right) {
        if (right == Long.MIN_VALUE) {
            if (left >= 0) {
                return null;
            }
            return left - right;
        }
        return checkedAdd(left, -right);
    }

    public static long[] buildPrefixSums(long[] values) {
        long[] prefix = new long[values.length + 1];
        for (int index = 0; index < values.length; ++index) {
            Long total = checkedAdd(prefix[index], values[index]);
            if (total == null) {
                return null;
            }
            prefix[index + 1] = total;
        }
        return prefix;
    }

    public static Long rangeSum(long[] prefix, int left, int right) {
        return checkedSub(prefix[right + 1], prefix[left]);
    }
}
