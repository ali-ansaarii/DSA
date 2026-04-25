import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Main {
    private Main() {}

    private static List<Trie.Operation> readOperations(Path inputPath) throws IOException {
        List<String> tokens = List.of(Files.readString(inputPath).split("\\s+"));
        if (tokens.isEmpty() || tokens.get(0).isEmpty()) {
            throw new IllegalArgumentException("Input file is empty");
        }

        int operationCount = Integer.parseInt(tokens.get(0));
        int expectedTokens = 1 + operationCount * 2;
        if (tokens.size() < expectedTokens) {
            throw new IllegalArgumentException("Input file ended before all commands were read");
        }

        List<Trie.Operation> operations = new ArrayList<>(operationCount);
        int index = 1;
        for (int i = 0; i < operationCount; i++) {
            operations.add(new Trie.Operation(tokens.get(index), tokens.get(index + 1)));
            index += 2;
        }

        return operations;
    }

    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean time_flag_time_trie = false;

        for (String argument : args) {
            if (argument.equals("--time-trie")) {
                time_flag_time_trie = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        try {
            List<Trie.Operation> operations = readOperations(inputPath);

            long start = System.nanoTime();
            List<String> output = Trie.executeCommands(operations);
            long finish = System.nanoTime();

            StringBuilder builder = new StringBuilder();
            for (String line : output) {
                builder.append(line).append(System.lineSeparator());
            }
            System.out.print(builder);

            if (time_flag_time_trie) {
                double elapsedMs = (finish - start) / 1_000_000.0;
                System.err.printf("trie_processing_ms=%.6f%n", elapsedMs);
            }
        } catch (Exception error) {
            System.err.println("Error: " + error.getMessage());
            System.exit(1);
        }
    }
}
