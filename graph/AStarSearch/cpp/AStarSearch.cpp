#include "AStarSearch.hpp"

#include <cstdlib>
#include <functional>
#include <limits>
#include <queue>
#include <tuple>

using namespace std;

namespace {
int manhattanDistance(int row, int col, int goalRow, int goalCol) {
    return abs(row - goalRow) + abs(col - goalCol);
}

bool isOpenCell(const vector<string>& grid, int row, int col) {
    return row >= 0 && row < static_cast<int>(grid.size()) &&
           col >= 0 && col < static_cast<int>(grid[row].size()) &&
           grid[row][col] != '#';
}
}  // namespace

int shortestPathLengthAStar(const vector<string>& grid,
                            int startRow,
                            int startCol,
                            int goalRow,
                            int goalCol) {
    if (grid.empty() || grid[0].empty()) {
        return -1;
    }

    const int rows = static_cast<int>(grid.size());
    const int cols = static_cast<int>(grid[0].size());

    if (startRow < 0 || startRow >= rows || startCol < 0 || startCol >= cols ||
        goalRow < 0 || goalRow >= rows || goalCol < 0 || goalCol >= cols ||
        !isOpenCell(grid, startRow, startCol) || !isOpenCell(grid, goalRow, goalCol)) {
        return -1;
    }

    const int infinity = numeric_limits<int>::max() / 4;
    vector<vector<int>> distance(rows, vector<int>(cols, infinity));

    // (f_score, h_score, g_score, row, col). Lower h_score breaks equal f_score ties
    // in favor of cells closer to the goal without changing correctness.
    using State = tuple<int, int, int, int, int>;
    priority_queue<State, vector<State>, greater<State>> open;

    const int startHeuristic = manhattanDistance(startRow, startCol, goalRow, goalCol);
    distance[startRow][startCol] = 0;
    open.emplace(startHeuristic, startHeuristic, 0, startRow, startCol);

    const int directions[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};

    while (!open.empty()) {
        const auto [fScore, hScore, currentDistance, row, col] = open.top();
        open.pop();
        (void)fScore;
        (void)hScore;

        if (currentDistance != distance[row][col]) {
            continue;
        }

        if (row == goalRow && col == goalCol) {
            return currentDistance;
        }

        for (const auto& direction : directions) {
            const int nextRow = row + direction[0];
            const int nextCol = col + direction[1];

            if (!isOpenCell(grid, nextRow, nextCol)) {
                continue;
            }

            const int nextDistance = currentDistance + 1;
            if (nextDistance < distance[nextRow][nextCol]) {
                distance[nextRow][nextCol] = nextDistance;
                const int heuristic = manhattanDistance(nextRow, nextCol, goalRow, goalCol);
                open.emplace(nextDistance + heuristic, heuristic, nextDistance, nextRow, nextCol);
            }
        }
    }

    return -1;
}
