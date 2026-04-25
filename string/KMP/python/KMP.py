from __future__ import annotations


def build_lps(pattern: str) -> list[int]:
    """Build the longest-prefix-suffix table for KMP."""
    lps = [0] * len(pattern)
    length = 0

    for i in range(1, len(pattern)):
        while length > 0 and pattern[i] != pattern[length]:
            length = lps[length - 1]
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length

    return lps


def kmp(text: str, pattern: str) -> list[int]:
    """Return all 0-based starting indices where pattern occurs in text."""
    if pattern == "":
        return list(range(len(text) + 1))

    lps = build_lps(pattern)
    matches: list[int] = []
    matched = 0

    for i, character in enumerate(text):
        while matched > 0 and character != pattern[matched]:
            matched = lps[matched - 1]

        if character == pattern[matched]:
            matched += 1

        if matched == len(pattern):
            matches.append(i + 1 - len(pattern))
            matched = lps[matched - 1]

    return matches
