import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public final class Main {
    public static void main(String[] args) throws IOException {
        Path inputPath = Path.of("inputs/input.txt");
        boolean time_flag_time_bidirectional_bfs = false;

        for (String argument : args) {
            if (argument.equals("--time-bidirectional-bfs")) {
                time_flag_time_bidirectional_bfs = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        FastScanner scanner = new FastScanner(inputPath);
        int n = scanner.nextIntRequired("missing vertex count");
        int m = scanner.nextIntRequired("missing edge count");
        if (n < 0 || m < 0) {
            throw new IllegalArgumentException("n and m must be non-negative");
        }

        List<List<Integer>> graph = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            graph.add(new ArrayList<>());
        }

        for (int i = 0; i < m; i++) {
            int u = scanner.nextIntRequired("missing edge endpoint");
            int v = scanner.nextIntRequired("missing edge endpoint");
            if (u < 0 || v < 0 || u >= n || v >= n) {
                throw new IllegalArgumentException("invalid edge at index " + i);
            }
            graph.get(u).add(v);
            graph.get(v).add(u);
        }

        int source = scanner.nextIntRequired("missing source");
        int target = scanner.nextIntRequired("missing target");
        if (source < 0 || target < 0 || source >= n || target >= n) {
            throw new IllegalArgumentException("invalid source/target query");
        }

        BidirectionalBFS.Result result;
        if (time_flag_time_bidirectional_bfs) {
            long start = System.nanoTime();
            result = BidirectionalBFS.shortestPath(graph, source, target);
            long end = System.nanoTime();
            System.err.println("algorithm_time_ns: " + (end - start));
        } else {
            result = BidirectionalBFS.shortestPath(graph, source, target);
        }

        System.out.println("distance: " + result.distance);
        StringBuilder pathLine = new StringBuilder("path:");
        for (int vertex : result.path) {
            pathLine.append(' ').append(vertex);
        }
        System.out.println(pathLine);
    }

    private static final class FastScanner {
        private final BufferedReader reader;
        private StringTokenizer tokenizer;

        FastScanner(Path path) throws IOException {
            this.reader = Files.newBufferedReader(path);
        }

        int nextIntRequired(String message) throws IOException {
            while (tokenizer == null || !tokenizer.hasMoreTokens()) {
                String line = reader.readLine();
                if (line == null) {
                    throw new IllegalArgumentException(message);
                }
                tokenizer = new StringTokenizer(line);
            }
            return Integer.parseInt(tokenizer.nextToken());
        }
    }
}
