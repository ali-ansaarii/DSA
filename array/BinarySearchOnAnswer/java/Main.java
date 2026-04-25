import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public final class Main {
    private record ProblemInput(int k, long[] values) {}

    private static ProblemInput readInput(Path inputPath) throws IOException {
        List<String> tokens = Files.readString(inputPath).trim().isEmpty()
            ? List.of()
            : List.of(Files.readString(inputPath).trim().split("\\s+"));

        if (tokens.size() < 2) {
            throw new IllegalArgumentException("Input must start with n and k");
        }

        int n = Integer.parseInt(tokens.get(0));
        int k = Integer.parseInt(tokens.get(1));
        if (n < 0) {
            throw new IllegalArgumentException("n must be non-negative");
        }
        if (tokens.size() < 2 + n) {
            throw new IllegalArgumentException("Input ended before reading all array values");
        }

        long[] values = new long[n];
        for (int i = 0; i < n; i++) {
            values[i] = Long.parseLong(tokens.get(2 + i));
        }

        return new ProblemInput(k, values);
    }

    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean time_flag_time_binary_search_on_answer = false;

        for (String argument : args) {
            if (argument.equals("--time-binary-search-on-answer")) {
                time_flag_time_binary_search_on_answer = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        try {
            ProblemInput input = readInput(inputPath);

            long answer;
            if (time_flag_time_binary_search_on_answer) {
                long start = System.nanoTime();
                answer = BinarySearchOnAnswer.minimizeLargestGroupSum(input.values(), input.k());
                long elapsed = System.nanoTime() - start;
                System.err.println("algorithm_time_ns " + elapsed);
            } else {
                answer = BinarySearchOnAnswer.minimizeLargestGroupSum(input.values(), input.k());
            }

            System.out.println(answer);
        } catch (Exception error) {
            System.err.println("Error: " + error.getMessage());
            System.exit(1);
        }
    }
}
