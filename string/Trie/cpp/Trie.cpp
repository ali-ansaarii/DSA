#include "Trie.hpp"

#include <stdexcept>

using namespace std;

Trie::Trie() : root(make_unique<Node>()) {}

void Trie::insert(const string& word) {
    Node* current = root.get();
    for (char ch : word) {
        const int index = ch - 'a';
        if (index < 0 || index >= 26) {
            throw invalid_argument("Trie only supports lowercase English letters");
        }
        if (!current->children[index]) {
            current->children[index] = make_unique<Node>();
        }
        current = current->children[index].get();
    }
    current->is_word = true;
}

bool Trie::search(const string& word) const {
    const Node* node = findNode(word);
    return node != nullptr && node->is_word;
}

bool Trie::startsWith(const string& prefix) const {
    return findNode(prefix) != nullptr;
}

const Trie::Node* Trie::findNode(const string& text) const {
    const Node* current = root.get();
    for (char ch : text) {
        const int index = ch - 'a';
        if (index < 0 || index >= 26) {
            throw invalid_argument("Trie only supports lowercase English letters");
        }
        if (!current->children[index]) {
            return nullptr;
        }
        current = current->children[index].get();
    }
    return current;
}

vector<string> executeTrieCommands(const vector<TrieCommand>& commands) {
    Trie trie;
    vector<string> output;

    for (const TrieCommand& command : commands) {
        if (command.operation == "insert") {
            trie.insert(command.value);
        } else if (command.operation == "search") {
            output.push_back(trie.search(command.value) ? "true" : "false");
        } else if (command.operation == "starts_with") {
            output.push_back(trie.startsWith(command.value) ? "true" : "false");
        } else {
            throw invalid_argument("Unknown trie command: " + command.operation);
        }
    }

    return output;
}
