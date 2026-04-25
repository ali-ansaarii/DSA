#pragma once

#include <array>
#include <memory>
#include <string>
#include <vector>

using namespace std;

struct TrieCommand {
    string operation;
    string value;
};

class Trie {
public:
    Trie();

    void insert(const string& word);
    bool search(const string& word) const;
    bool startsWith(const string& prefix) const;

private:
    struct Node {
        array<unique_ptr<Node>, 26> children{};
        bool is_word = false;
    };

    unique_ptr<Node> root;

    const Node* findNode(const string& text) const;
};

vector<string> executeTrieCommands(const vector<TrieCommand>& commands);
