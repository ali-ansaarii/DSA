import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Main {
    private static boolean isValidElement(int element, int n) {
        return element >= 0 && element < n;
    }

    public static void main(String[] args) {
        String inputPath = "inputs/input.txt";
        boolean timeDsu = false;

        for (String arg : args) {
            if ("--time-dsu".equals(arg)) {
                timeDsu = true;
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
            System.err.println("Invalid DSU header. Expected: n q");
            System.exit(1);
            return;
        }

        String[] header = lines.get(0).split("\\s+");
        if (header.length != 2) {
            System.err.println("Invalid DSU header. Expected: n q");
            System.exit(1);
            return;
        }

        int n;
        int q;
        try {
            n = Integer.parseInt(header[0]);
            q = Integer.parseInt(header[1]);
        } catch (NumberFormatException e) {
            System.err.println("Invalid DSU header. Expected: n q");
            System.exit(1);
            return;
        }

        if (n <= 0 || q < 0) {
            System.err.println("Invalid DSU header. Expected: n q");
            System.exit(1);
            return;
        }

        if (lines.size() < q + 1) {
            System.err.println("Input ended early. Expected " + q + " operations.");
            System.exit(1);
            return;
        }

        List<DisjointSetUnion.Operation> operations = new ArrayList<>();
        for (int lineIndex = 1; lineIndex <= q; lineIndex++) {
            String[] parts = lines.get(lineIndex).split("\\s+");
            if (parts.length == 0) {
                System.err.println("Invalid operation at line " + (lineIndex + 1));
                System.exit(1);
                return;
            }

            String op = parts[0];
            if ("union".equals(op) || "connected".equals(op)) {
                if (parts.length != 3) {
                    System.err.println("Invalid operation at line " + (lineIndex + 1));
                    System.exit(1);
                    return;
                }

                int a;
                int b;
                try {
                    a = Integer.parseInt(parts[1]);
                    b = Integer.parseInt(parts[2]);
                } catch (NumberFormatException e) {
                    System.err.println("Invalid operation at line " + (lineIndex + 1));
                    System.exit(1);
                    return;
                }

                if (!isValidElement(a, n) || !isValidElement(b, n)) {
                    System.err.println("Invalid operation at line " + (lineIndex + 1));
                    System.exit(1);
                    return;
                }

                operations.add(new DisjointSetUnion.Operation(
                    "union".equals(op) ? DisjointSetUnion.OperationType.UNION : DisjointSetUnion.OperationType.CONNECTED,
                    a,
                    b
                ));
            } else if ("find".equals(op)) {
                if (parts.length != 2) {
                    System.err.println("Invalid operation at line " + (lineIndex + 1));
                    System.exit(1);
                    return;
                }

                int a;
                try {
                    a = Integer.parseInt(parts[1]);
                } catch (NumberFormatException e) {
                    System.err.println("Invalid operation at line " + (lineIndex + 1));
                    System.exit(1);
                    return;
                }

                if (!isValidElement(a, n)) {
                    System.err.println("Invalid operation at line " + (lineIndex + 1));
                    System.exit(1);
                    return;
                }

                operations.add(new DisjointSetUnion.Operation(DisjointSetUnion.OperationType.FIND, a, -1));
            } else {
                System.err.println("Invalid operation at line " + (lineIndex + 1));
                System.exit(1);
                return;
            }
        }

        long dsuStart = System.nanoTime();
        List<String> queryResults = DisjointSetUnion.DisjointSetUnion(n, operations);
        double dsuDurationMs = (System.nanoTime() - dsuStart) / 1_000_000.0;

        if (timeDsu) {
            System.out.println("Processed operations: " + operations.size());
            System.out.printf(Locale.US, "DisjointSetUnion call time (ms): %.3f%n", dsuDurationMs);
        } else {
            System.out.println("Query results:");
            for (String result : queryResults) {
                System.out.println(result);
            }
        }
    }
}
