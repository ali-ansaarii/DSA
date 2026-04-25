import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Main {
    private static final class ParsedInput {
        final List<String> grid;
        final int startRow;
        final int startCol;
        final int goalRow;
        final int goalCol;

        ParsedInput(List<String> grid, int startRow, int startCol, int goalRow, int goalCol) {
            this.grid = grid;
            this.startRow = startRow;
            this.startCol = startCol;
            this.goalRow = goalRow;
            this.goalCol = goalCol;
        }
    }

    public static void main(String[] args) {
        Path inputPath = Path.of("inputs/input.txt");
        boolean time_flag_time_a_star_search = false;

        for (String argument : args) {
            if (argument.equals("--time-a-star-search")) {
                time_flag_time_a_star_search = true;
            } else {
                inputPath = Path.of(argument);
            }
        }

        try {
            ParsedInput parsed = parseInput(inputPath);

            int distance;
            if (time_flag_time_a_star_search) {
                long startedAt = System.nanoTime();
                distance = AStarSearch.shortestPathLengthAStar(
                        parsed.grid, parsed.startRow, parsed.startCol, parsed.goalRow, parsed.goalCol);
                long elapsedMicroseconds = (System.nanoTime() - startedAt) / 1_000L;
                System.err.println("Algorithm time (microseconds): " + elapsedMicroseconds);
            } else {
                distance = AStarSearch.shortestPathLengthAStar(
                        parsed.grid, parsed.startRow, parsed.startCol, parsed.goalRow, parsed.goalCol);
            }

            if (distance >= 0) {
                System.out.println("Shortest path length: " + distance);
            } else {
                System.out.println("UNREACHABLE");
            }
        } catch (IOException | IllegalArgumentException error) {
            System.err.println("Error: " + error.getMessage());
            System.exit(1);
        }
    }

    private static ParsedInput parseInput(Path inputPath) throws IOException {
        String[] tokens = Files.readString(inputPath).trim().split("\\s+");
        if (tokens.length < 6) {
            throw new IllegalArgumentException(
                    "input must contain rows, cols, start, and goal coordinates");
        }

        int rows = Integer.parseInt(tokens[0]);
        int cols = Integer.parseInt(tokens[1]);
        int startRow = Integer.parseInt(tokens[2]);
        int startCol = Integer.parseInt(tokens[3]);
        int goalRow = Integer.parseInt(tokens[4]);
        int goalCol = Integer.parseInt(tokens[5]);

        if (rows <= 0 || cols <= 0) {
            throw new IllegalArgumentException("rows and cols must be positive");
        }
        if (tokens.length < 6 + rows) {
            throw new IllegalArgumentException("missing grid rows");
        }

        List<String> grid = new ArrayList<>();
        for (int row = 0; row < rows; row++) {
            String line = tokens[6 + row];
            if (line.length() != cols) {
                throw new IllegalArgumentException("grid row " + row + " has the wrong length");
            }
            for (int col = 0; col < cols; col++) {
                char cell = line.charAt(col);
                if (cell != '.' && cell != '#') {
                    throw new IllegalArgumentException("grid may contain only '.' and '#'");
                }
            }
            grid.add(line);
        }

        return new ParsedInput(grid, startRow, startCol, goalRow, goalCol);
    }
}
