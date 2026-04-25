import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public final class Main {
    private Main() {}

    private record InputData(String text, String pattern) {}

    private static InputData readInput(Path inputPath) throws IOException {
        List<String> lines = Files.readAllLines(inputPath);
        if (lines.size() < 2) {
            throw new IllegalArgumentException("input file must contain a text line and a pattern line");
        }
        return new InputData(lines.get(0), lines.get(1));
    }

    private static void printMatches(List<Integer> matches) {
        StringBuilder output = new StringBuilder();
        for (int i = 0; i < matches.size(); i++) {
            if (i > 0) {
                output.append(' ');
            }
            output.append(matches.get(i));
        }
        System.out.println(output);
    }

    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean time_flag_time_kmp = false;

        for (String argument : args) {
            if (argument.equals("--time-kmp")) {
                time_flag_time_kmp = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        try {
            InputData input = readInput(inputPath);
            List<Integer> matches;

            if (time_flag_time_kmp) {
                long start = System.nanoTime();
                matches = KMP.search(input.text(), input.pattern());
                long elapsed = System.nanoTime() - start;
                System.err.printf("algorithm_time_ms: %.6f%n", elapsed / 1_000_000.0);
            } else {
                matches = KMP.search(input.text(), input.pattern());
            }

            printMatches(matches);
        } catch (Exception error) {
            System.err.println("Error: " + error.getMessage());
            System.exit(1);
        }
    }
}
