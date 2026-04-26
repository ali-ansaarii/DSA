public final class BinarySearchOnAnswer {
    private BinarySearchOnAnswer() {}

    public static boolean canPartitionWithMaxGroupSum(long[] values, int maxGroups, long limit) {
        if (maxGroups <= 0) {
            return false;
        }

        int groupsUsed = 1;
        long currentSum = 0L;

        for (long value : values) {
            if (value < 0) {
                throw new IllegalArgumentException(
                    "Binary Search on Answer partition baseline requires non-negative values"
                );
            }
            if (value > limit) {
                return false;
            }
            if (currentSum + value > limit) {
                groupsUsed++;
                currentSum = value;
                if (groupsUsed > maxGroups) {
                    return false;
                }
            } else {
                currentSum += value;
            }
        }

        return true;
    }

    public static long minimizeLargestGroupSum(long[] values, int maxGroups) {
        if (values.length == 0) {
            return 0L;
        }
        if (maxGroups <= 0) {
            throw new IllegalArgumentException("maxGroups must be positive");
        }

        long low = values[0];
        long high = 0L;
        for (long value : values) {
            if (value > low) {
                low = value;
            }
            high += value;
        }

        while (low < high) {
            long mid = low + (high - low) / 2L;
            if (canPartitionWithMaxGroupSum(values, maxGroups, mid)) {
                high = mid;
            } else {
                low = mid + 1L;
            }
        }

        return low;
    }
}
