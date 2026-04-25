#include "KMP.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using namespace std;

static pair<string, string> readInput(const string& inputPath) {
    ifstream input(inputPath);
    if (!input) {
        throw runtime_error("failed to open input file: " + inputPath);
    }

    string text;
    string pattern;
    if (!getline(input, text)) {
        throw runtime_error("input file must contain a text line");
    }
    if (!getline(input, pattern)) {
        throw runtime_error("input file must contain a pattern line");
    }

    return {text, pattern};
}

static void printMatches(const vector<int>& matches) {
    for (size_t i = 0; i < matches.size(); ++i) {
        if (i > 0) {
            cout << ' ';
        }
        cout << matches[i];
    }
    cout << '\n';
}

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool time_flag_time_kmp = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-kmp") {
            time_flag_time_kmp = true;
        } else {
            inputPath = argument;
        }
    }

    try {
        const auto [text, pattern] = readInput(inputPath);

        vector<int> matches;
        if (time_flag_time_kmp) {
            const auto start = chrono::steady_clock::now();
            matches = KMP(text, pattern);
            const auto end = chrono::steady_clock::now();
            const double elapsedMs = chrono::duration<double, milli>(end - start).count();
            cerr << "algorithm_time_ms: " << elapsedMs << '\n';
        } else {
            matches = KMP(text, pattern);
        }

        printMatches(matches);
    } catch (const exception& error) {
        cerr << "Error: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
