import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Main {
    private static boolean isValidChild(int child, int n) {
        return child == -1 || (child >= 0 && child < n);
    }

    public static void main(String[] args) {
        String inputPath = "../inputs/input.txt";
        boolean timeInorder = false;

        for (String arg : args) {
            if ("--time-inorder".equals(arg)) {
                timeInorder = true;
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
            System.err.println("Invalid tree header. Expected: n root");
            System.exit(1);
            return;
        }

        String[] header = lines.get(0).split("\\s+");
        if (header.length != 2) {
            System.err.println("Invalid tree header. Expected: n root");
            System.exit(1);
            return;
        }

        int n;
        int root;
        try {
            n = Integer.parseInt(header[0]);
            root = Integer.parseInt(header[1]);
        } catch (NumberFormatException e) {
            System.err.println("Invalid tree header. Expected: n root");
            System.exit(1);
            return;
        }

        if (n <= 0 || root < 0 || root >= n) {
            System.err.println("Invalid tree header. Expected: n root");
            System.exit(1);
            return;
        }

        if (lines.size() < n + 1) {
            System.err.println("Input ended early. Expected child pairs for all nodes.");
            System.exit(1);
            return;
        }

        int[] leftChildren = new int[n];
        int[] rightChildren = new int[n];

        for (int node = 0; node < n; node++) {
            String[] childParts = lines.get(node + 1).split("\\s+");
            if (childParts.length != 2) {
                System.err.println("Invalid child pair at line " + (node + 2));
                System.exit(1);
                return;
            }

            int left;
            int right;
            try {
                left = Integer.parseInt(childParts[0]);
                right = Integer.parseInt(childParts[1]);
            } catch (NumberFormatException e) {
                System.err.println("Invalid child pair at line " + (node + 2));
                System.exit(1);
                return;
            }

            if (!isValidChild(left, n) || !isValidChild(right, n)) {
                System.err.println("Invalid child pair at line " + (node + 2));
                System.exit(1);
                return;
            }

            leftChildren[node] = left;
            rightChildren[node] = right;
        }

        long traversalStart = System.nanoTime();
        List<Integer> order = InorderTraversal.InorderTraversal(leftChildren, rightChildren, root);
        double traversalDurationMs = (System.nanoTime() - traversalStart) / 1_000_000.0;

        if (timeInorder) {
            System.out.println("Visited nodes: " + order.size());
            System.out.printf(Locale.US, "InorderTraversal call time (ms): %.3f%n", traversalDurationMs);
        } else {
            System.out.print("Inorder traversal order:");
            for (int node : order) {
                System.out.print(" " + node);
            }
            System.out.println();
        }
    }
}
