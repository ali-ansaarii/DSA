#include "AStarSearch.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using namespace std;

namespace {
struct ParsedInput {
    vector<string> grid;
    int startRow;
    int startCol;
    int goalRow;
    int goalCol;
};

ParsedInput parseInputFile(const string& inputPath) {
    ifstream input(inputPath);
    if (!input) {
        throw runtime_error("Unable to open input file: " + inputPath);
    }

    int rows = 0;
    int cols = 0;
    int startRow = 0;
    int startCol = 0;
    int goalRow = 0;
    int goalCol = 0;

    if (!(input >> rows >> cols >> startRow >> startCol >> goalRow >> goalCol)) {
        throw runtime_error("Input must contain rows, cols, start, and goal coordinates");
    }

    if (rows <= 0 || cols <= 0) {
        throw runtime_error("rows and cols must be positive");
    }

    vector<string> grid(rows);
    for (int row = 0; row < rows; ++row) {
        if (!(input >> grid[row])) {
            throw runtime_error("Missing grid row " + to_string(row));
        }
        if (static_cast<int>(grid[row].size()) != cols) {
            throw runtime_error("Grid row " + to_string(row) + " has the wrong length");
        }
        for (char cell : grid[row]) {
            if (cell != '.' && cell != '#') {
                throw runtime_error("Grid may contain only '.' and '#'");
            }
        }
    }

    return ParsedInput{grid, startRow, startCol, goalRow, goalCol};
}
}  // namespace

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool time_flag_time_a_star_search = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-a-star-search") {
            time_flag_time_a_star_search = true;
        } else {
            inputPath = argument;
        }
    }

    try {
        const ParsedInput parsed = parseInputFile(inputPath);

        int distance = -1;
        if (time_flag_time_a_star_search) {
            const auto start = chrono::steady_clock::now();
            distance = shortestPathLengthAStar(parsed.grid, parsed.startRow, parsed.startCol,
                                               parsed.goalRow, parsed.goalCol);
            const auto end = chrono::steady_clock::now();
            const auto micros = chrono::duration_cast<chrono::microseconds>(end - start).count();
            cerr << "Algorithm time (microseconds): " << micros << '\n';
        } else {
            distance = shortestPathLengthAStar(parsed.grid, parsed.startRow, parsed.startCol,
                                               parsed.goalRow, parsed.goalCol);
        }

        if (distance >= 0) {
            cout << "Shortest path length: " << distance << '\n';
        } else {
            cout << "UNREACHABLE\n";
        }
    } catch (const exception& error) {
        cerr << "Error: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
