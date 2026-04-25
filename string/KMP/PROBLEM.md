# KMP

## What is KMP?
Knuth-Morris-Pratt (KMP) is a linear-time string matching algorithm. It searches for a pattern inside a text by first preprocessing the pattern into an LPS table, where LPS stands for longest proper prefix that is also a suffix. When a mismatch occurs, KMP uses this table to shift the pattern without re-checking text characters that are already known to match.

## Problem in this folder
Given one text string and one pattern string, report every 0-based starting index where the pattern occurs in the text. Overlapping matches are included.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
The preprocessing step builds `lps[i]`, the length of the longest proper prefix of `pattern[0..i]` that is also a suffix of `pattern[0..i]`. During the scan, `j` is the number of pattern characters currently matched. If `text[i] == pattern[j]`, both positions advance. If they differ and `j > 0`, KMP falls back to `j = lps[j - 1]` instead of moving the text index backward. Therefore each text character and each pattern fallback is processed a bounded number of times, giving linear runtime.

After a full match, the algorithm records `i - pattern_length + 1` and continues with `j = lps[pattern_length - 1]` so overlapping matches are found.

## Input Format
Each input file is command-free and contains exactly two logical lines:

```text
<text>
<pattern>
```

- The first line is the text to search.
- The second line is the pattern to find.
- Starting indices in the output are 0-based.
- If the pattern is empty, this implementation treats it as matching at every boundary index from `0` through `len(text)`.

## Output Format
Print all match starting indices on one line, separated by single spaces, followed by a newline. If there are no matches, print an empty line.

## Time Complexity
`O(n + m)`, where `n` is the length of the text and `m` is the length of the pattern.

## Space Complexity
`O(m)` auxiliary space for the LPS table, plus `O(k)` for the returned match indices, where `k` is the number of matches.

## Why the challenge input is challenging
`inputs/input_challenge.txt` uses a long run of repeated `a` characters in the text and a pattern made of many `a` characters followed by `b`. This is adversarial for naive matching because many alignments nearly match before failing at the final character. KMP avoids the repeated rescans by using the LPS table, so it still runs in linear time.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
abababa
aba
```

## Intended Output
Expected output:

```text
0 2 4
```
