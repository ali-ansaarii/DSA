import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        String inputPath = "inputs/input.txt";
        boolean timeDijkstra = false;

        for (String arg : args) {
            if ("--time-dijkstra".equals(arg)) {
                timeDijkstra = true;
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

        if (lines.size() < m + 2) {
            System.err.println("Input ended early. Expected edges and start node.");
            System.exit(1);
            return;
        }

        List<List<Dijkstra.Edge>> graph = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            graph.add(new ArrayList<>());
        }

        for (int i = 0; i < m; i++) {
            String[] edgeParts = lines.get(i + 1).split("\\s+");
            if (edgeParts.length != 3) {
                System.err.println("Invalid weighted edge at line " + (i + 2));
                System.exit(1);
                return;
            }

            int u;
            int v;
            long w;
            try {
                u = Integer.parseInt(edgeParts[0]);
                v = Integer.parseInt(edgeParts[1]);
                w = Long.parseLong(edgeParts[2]);
            } catch (NumberFormatException e) {
                System.err.println("Invalid weighted edge at line " + (i + 2));
                System.exit(1);
                return;
            }

            if (u < 0 || u >= n || v < 0 || v >= n || w < 0) {
                System.err.println("Invalid weighted edge at line " + (i + 2));
                System.exit(1);
                return;
            }

            graph.get(u).add(new Dijkstra.Edge(v, w));
            graph.get(v).add(new Dijkstra.Edge(u, w));
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

        for (List<Dijkstra.Edge> neighbors : graph) {
            neighbors.sort(Comparator.comparingInt(edge -> edge.to));
        }

        Dijkstra.Result result;
        long dijkstraStart = System.nanoTime();
        try {
            result = Dijkstra.Dijkstra(graph, start);
        } catch (ArithmeticException e) {
            System.err.println(e.getMessage());
            System.exit(1);
            return;
        }
        double dijkstraDurationMs = (System.nanoTime() - dijkstraStart) / 1_000_000.0;

        int reachableNodes = 0;
        for (boolean isReachable : result.reachable) {
            if (isReachable) {
                reachableNodes++;
            }
        }

        if (timeDijkstra) {
            System.out.println("Reachable nodes: " + reachableNodes);
            System.out.printf(Locale.US, "Dijkstra call time (ms): %.3f%n", dijkstraDurationMs);
        } else {
            System.out.print("Shortest distances from " + start + ":");
            for (int i = 0; i < result.distances.length; i++) {
                if (!result.reachable[i]) {
                    System.out.print(" INF");
                } else {
                    System.out.print(" " + result.distances[i]);
                }
            }
            System.out.println();
        }
    }
}
