import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public final class Main {
    private Main() {}

    private static long[] readInput(Path inputPath) throws IOException {
        String content = Files.readString(inputPath).trim();
        if (content.isEmpty()) {
            throw new IllegalArgumentException("input must start with a positive element count");
        }

        String[] tokens = content.split("\\s+");
        int n = Integer.parseInt(tokens[0]);
        if (n <= 0) {
            throw new IllegalArgumentException("input must start with a positive element count");
        }
        if (tokens.length != n + 1) {
            throw new IllegalArgumentException("expected " + n + " array values, found " + (tokens.length - 1));
        }

        long[] values = new long[n];
        for (int i = 0; i < n; i++) {
            values[i] = Long.parseLong(tokens[i + 1]);
        }
        return values;
    }

    private static void printResult(Kadane.Result result, long[] values) {
        System.out.println("maximum_sum: " + result.maximumSum);
        System.out.println("start_index: " + result.startIndex);
        System.out.println("end_index: " + result.endIndex);

        StringBuilder subarray = new StringBuilder("subarray:");
        for (int i = result.startIndex; i <= result.endIndex; i++) {
            subarray.append(' ').append(values[i]);
        }
        System.out.println(subarray);
    }

    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean timeKadane = false;

        for (String argument : args) {
            if (argument.equals("--time-kadane")) {
                timeKadane = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        try {
            long[] values = readInput(inputPath);

            Kadane.Result result;
            long elapsedNs = 0L;
            if (timeKadane) {
                long start = System.nanoTime();
                result = Kadane.maxSubarrayKadane(values);
                elapsedNs = System.nanoTime() - start;
            } else {
                result = Kadane.maxSubarrayKadane(values);
            }

            printResult(result, values);
            if (timeKadane) {
                System.out.println("algorithm_time_ns: " + elapsedNs);
            }
        } catch (Exception error) {
            System.err.println("error: " + error.getMessage());
            System.exit(1);
        }
    }
}
