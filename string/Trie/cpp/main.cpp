#include "Trie.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using namespace std;

static vector<TrieCommand> readCommands(const string& inputPath) {
    ifstream input(inputPath);
    if (!input) {
        throw runtime_error("Unable to open input file: " + inputPath);
    }

    int commandCount = 0;
    input >> commandCount;
    if (!input || commandCount < 0) {
        throw runtime_error("Invalid command count in input file");
    }

    vector<TrieCommand> commands;
    commands.reserve(static_cast<size_t>(commandCount));

    for (int i = 0; i < commandCount; ++i) {
        TrieCommand command;
        input >> command.operation >> command.value;
        if (!input) {
            throw runtime_error("Invalid command line in input file");
        }
        commands.push_back(command);
    }

    return commands;
}

int main(int argc, char* argv[]) {
    string inputPath = "inputs/input.txt";
    bool time_flag_time_trie = false;

    for (int i = 1; i < argc; ++i) {
        string argument = argv[i];
        if (argument == "--time-trie") {
            time_flag_time_trie = true;
        } else {
            inputPath = argument;
        }
    }

    try {
        const vector<TrieCommand> commands = readCommands(inputPath);

        const auto start = chrono::steady_clock::now();
        const vector<string> output = executeTrieCommands(commands);
        const auto finish = chrono::steady_clock::now();

        for (const string& line : output) {
            cout << line << '\n';
        }

        if (time_flag_time_trie) {
            const chrono::duration<double, milli> elapsed = finish - start;
            cerr << "trie_processing_ms=" << elapsed.count() << '\n';
        }
    } catch (const exception& error) {
        cerr << "Error: " << error.what() << '\n';
        return 1;
    }

    return 0;
}
