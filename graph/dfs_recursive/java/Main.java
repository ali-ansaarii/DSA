import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        String inputPath = args.length > 0 ? args[0] : "input.txt";

        List<String> lines;
        try {
            lines = new ArrayList<>();
            for (String line : Files.readAllLines(Paths.get(inputPath))) {
                line = line.trim();
                if (!line.isEmpty()) {
                    lines.add(line);
                }
            }
        } catch (IOException e) {
            System.err.println("Failed to open input file: " + inputPath);
            System.exit(1);
            return;
        }

        if (lines.size() < 2) {
            System.err.println("Invalid graph header. Expected: n m");
            System.exit(1);
            return;
        }

        String[] header = lines.get(0).split("\\s+");
        if (header.length != 2) {
            System.err.println("Invalid graph header. Expected: n m");
            System.exit(1);
            return;
        }

        int n, m;
        try {
            n = Integer.parseInt(header[0]);
            m = Integer.parseInt(header[1]);
        } catch (NumberFormatException e) {
            System.err.println("Invalid graph header. Expected: n m");
            System.exit(1);
            return;
        }

        if (n <= 0 || m < 0) {
            System.err.println("Invalid graph header. Expected: n m");
            System.exit(1);
            return;
        }

        if (lines.size() < m + 2) {
            System.err.println("Input ended early. Expected edges and start node.");
            System.exit(1);
            return;
        }

        List<List<Integer>> graph = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            graph.add(new ArrayList<>());
        }

        for (int i = 0; i < m; i++) {
            String[] edgeParts = lines.get(i + 1).split("\\s+");
            if (edgeParts.length != 2) {
                System.err.println("Invalid edge at line " + (i + 2));
                System.exit(1);
                return;
            }

            int u, v;
            try {
                u = Integer.parseInt(edgeParts[0]);
                v = Integer.parseInt(edgeParts[1]);
            } catch (NumberFormatException e) {
                System.err.println("Invalid edge at line " + (i + 2));
                System.exit(1);
                return;
            }

            if (u < 0 || u >= n || v < 0 || v >= n) {
                System.err.println("Invalid edge at line " + (i + 2));
                System.exit(1);
                return;
            }

            // Undirected graph: add both directions.
            graph.get(u).add(v);
            graph.get(v).add(u);
        }

        int start;
        try {
            start = Integer.parseInt(lines.get(m + 1));
        } catch (NumberFormatException e) {
            System.err.println("Invalid start node. Expected a node in [0, n).");
            System.exit(1);
            return;
        }

        if (start < 0 || start >= n) {
            System.err.println("Invalid start node. Expected a node in [0, n).");
            System.exit(1);
            return;
        }

        // Sort adjacency lists for deterministic traversal.
        for (List<Integer> neighbors : graph) {
            Collections.sort(neighbors);
        }

        List<Integer> traversalOrder = DFS.DFS(graph, start);

        System.out.print("DFS traversal order:");
        for (int node : traversalOrder) {
            System.out.print(" " + node);
        }
        System.out.println();
    }
}
