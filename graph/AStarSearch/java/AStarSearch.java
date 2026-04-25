import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;

public final class AStarSearch {
    private AStarSearch() {}

    private static final class State implements Comparable<State> {
        final int fScore;
        final int hScore;
        final int gScore;
        final int row;
        final int col;

        State(int fScore, int hScore, int gScore, int row, int col) {
            this.fScore = fScore;
            this.hScore = hScore;
            this.gScore = gScore;
            this.row = row;
            this.col = col;
        }

        @Override
        public int compareTo(State other) {
            if (fScore != other.fScore) {
                return Integer.compare(fScore, other.fScore);
            }
            if (hScore != other.hScore) {
                return Integer.compare(hScore, other.hScore);
            }
            return Integer.compare(gScore, other.gScore);
        }
    }

    public static int shortestPathLengthAStar(
            List<String> grid, int startRow, int startCol, int goalRow, int goalCol) {
        if (grid.isEmpty() || grid.get(0).isEmpty()) {
            return -1;
        }

        int rows = grid.size();
        int cols = grid.get(0).length();

        if (!isOpen(grid, startRow, startCol, rows, cols)
                || !isOpen(grid, goalRow, goalCol, rows, cols)) {
            return -1;
        }

        int[][] distance = new int[rows][cols];
        for (int[] row : distance) {
            Arrays.fill(row, Integer.MAX_VALUE / 4);
        }

        PriorityQueue<State> open = new PriorityQueue<>();
        int startHeuristic = manhattan(startRow, startCol, goalRow, goalCol);
        distance[startRow][startCol] = 0;
        open.add(new State(startHeuristic, startHeuristic, 0, startRow, startCol));

        int[][] directions = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

        while (!open.isEmpty()) {
            State current = open.poll();
            if (current.gScore != distance[current.row][current.col]) {
                continue;
            }

            if (current.row == goalRow && current.col == goalCol) {
                return current.gScore;
            }

            for (int[] direction : directions) {
                int nextRow = current.row + direction[0];
                int nextCol = current.col + direction[1];

                if (!isOpen(grid, nextRow, nextCol, rows, cols)) {
                    continue;
                }

                int nextDistance = current.gScore + 1;
                if (nextDistance < distance[nextRow][nextCol]) {
                    distance[nextRow][nextCol] = nextDistance;
                    int heuristic = manhattan(nextRow, nextCol, goalRow, goalCol);
                    open.add(new State(
                            nextDistance + heuristic, heuristic, nextDistance, nextRow, nextCol));
                }
            }
        }

        return -1;
    }

    private static int manhattan(int row, int col, int goalRow, int goalCol) {
        return Math.abs(row - goalRow) + Math.abs(col - goalCol);
    }

    private static boolean isOpen(List<String> grid, int row, int col, int rows, int cols) {
        return row >= 0 && row < rows && col >= 0 && col < cols && grid.get(row).charAt(col) != '#';
    }
}
