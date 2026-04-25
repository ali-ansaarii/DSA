# Trie

## What is Trie?
A trie, also called a prefix tree, is a rooted tree data structure for storing strings. Each edge represents one character, and each node represents the prefix formed by the path from the root to that node. This implementation stores lowercase English words and supports insertion, exact word lookup, and prefix lookup.

## Problem in this folder
Given a sequence of commands, maintain an initially empty trie. Execute each command in order:

- `insert word`: add `word` to the trie.
- `search word`: print whether `word` has previously been inserted as a complete word.
- `starts_with prefix`: print whether at least one inserted word starts with `prefix`.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
Each trie node owns up to 26 child links, one for each lowercase English letter, plus a boolean marker saying whether a complete word ends at that node. To insert a word, walk one character at a time from the root and create missing child nodes. To search for a word or prefix, walk the same character path. Exact search additionally requires the final node's end-of-word marker to be true; prefix search only requires the path to exist.

## Input Format
All language implementations use the same command-based file format:

```text
q
command_1 word_1
command_2 word_2
...
command_q word_q
```

- `q` is the number of commands.
- `command_i` is one of `insert`, `search`, or `starts_with`.
- `word_i` contains only lowercase English letters `a` through `z`.
- `insert` commands produce no output.
- `search` and `starts_with` commands each output one line: `true` or `false`.

## Time Complexity
Let `L` be the length of the word or prefix in a single command.

- `insert`: `O(L)`
- `search`: `O(L)`
- `starts_with`: `O(L)`

Processing the whole input is `O(total_characters_in_all_commands)`.

## Space Complexity
The trie uses `O(total_characters_in_inserted_words)` nodes in the worst case. With fixed lowercase English alphabet links, each node stores 26 child references plus one end-of-word marker.

## Why the challenge input is challenging
The challenge input uses many words that share a long common prefix, plus searches for long near-matches. This stresses two common trie edge cases: deep traversal along a narrow branch and distinguishing a prefix that exists from a complete word that has actually been inserted.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
16
insert apple
search apple
search app
starts_with app
insert app
search app
insert apply
starts_with appl
search apply
search apples
starts_with banana
insert banana
starts_with ban
search band
insert band
search band
```

## Intended Output
Expected output:

```text
true
false
true
true
true
true
false
false
true
false
true
```
