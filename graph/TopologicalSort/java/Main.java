import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        String inputPath = "inputs/input.txt";
        boolean timeTopologicalSort = false;

        for (String arg : args) {
            if ("--time-toposort".equals(arg)) {
                timeTopologicalSort = true;
            } else {
                inputPath = arg;
            }
        }

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

        if (lines.isEmpty()) {
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

        int n;
        int m;
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

        if (lines.size() < m + 1) {
            System.err.println("Input ended early. Expected directed edges.");
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
                System.err.println("Invalid directed edge at line " + (i + 2));
                System.exit(1);
                return;
            }

            int u;
            int v;
            try {
                u = Integer.parseInt(edgeParts[0]);
                v = Integer.parseInt(edgeParts[1]);
            } catch (NumberFormatException e) {
                System.err.println("Invalid directed edge at line " + (i + 2));
                System.exit(1);
                return;
            }

            if (u < 0 || u >= n || v < 0 || v >= n) {
                System.err.println("Invalid directed edge at line " + (i + 2));
                System.exit(1);
                return;
            }

            graph.get(u).add(v);
        }

        for (List<Integer> neighbors : graph) {
            Collections.sort(neighbors);
        }

        long topologicalSortStart = System.nanoTime();
        List<Integer> order = TopologicalSort.TopologicalSort(graph);
        double topologicalSortDurationMs = (System.nanoTime() - topologicalSortStart) / 1_000_000.0;

        if (timeTopologicalSort) {
            System.out.println("Processed nodes: " + order.size());
            System.out.printf(Locale.US, "TopologicalSort call time (ms): %.3f%n", topologicalSortDurationMs);
        }

        if (order.size() != graph.size()) {
            System.err.println("Cycle detected. Topological sort requires a DAG.");
            System.exit(1);
            return;
        }

        if (!timeTopologicalSort) {
            System.out.print("Topological order:");
            for (int node : order) {
                System.out.print(" " + node);
            }
            System.out.println();
        }
    }
}
