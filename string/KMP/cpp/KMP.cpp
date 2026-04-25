#include "KMP.hpp"

using namespace std;

vector<int> buildLPS(const string& pattern) {
    vector<int> lps(pattern.size(), 0);
    int length = 0;

    for (size_t i = 1; i < pattern.size(); ++i) {
        while (length > 0 && pattern[i] != pattern[length]) {
            length = lps[length - 1];
        }
        if (pattern[i] == pattern[length]) {
            ++length;
            lps[i] = length;
        }
    }

    return lps;
}

vector<int> KMP(const string& text, const string& pattern) {
    vector<int> matches;

    if (pattern.empty()) {
        matches.reserve(text.size() + 1);
        for (size_t i = 0; i <= text.size(); ++i) {
            matches.push_back(static_cast<int>(i));
        }
        return matches;
    }

    const vector<int> lps = buildLPS(pattern);
    int matched = 0;

    for (size_t i = 0; i < text.size(); ++i) {
        while (matched > 0 && text[i] != pattern[matched]) {
            matched = lps[matched - 1];
        }

        if (text[i] == pattern[matched]) {
            ++matched;
        }

        if (matched == static_cast<int>(pattern.size())) {
            matches.push_back(static_cast<int>(i + 1 - pattern.size()));
            matched = lps[matched - 1];
        }
    }

    return matches;
}
