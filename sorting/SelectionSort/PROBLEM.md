# Selection Sort

## What is Selection Sort?
Selection Sort is a simple comparison-based sorting algorithm. It repeatedly scans the unsorted suffix of an array to find the smallest remaining element, then swaps that element into the next position of the sorted prefix. After the `i`th pass, the first `i + 1` positions contain the smallest `i + 1` values in ascending order.

## Problem in this folder
Given one array of integers, sort the array in ascending order using classic in-place Selection Sort and print the sorted values.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
Maintain a boundary between a sorted prefix and an unsorted suffix. For each index `i` from left to right, scan positions `i` through `n - 1` to find the index of the minimum value in the unsorted suffix. Swap that minimum value with `array[i]`. This preserves the invariant that every value before `i + 1` is in final sorted position and no value in the suffix is smaller than any value in the prefix.

## Input Format
All language implementations use the same whitespace-separated file format:

```text
n
x1 x2 x3 ... xn
```

- `n` is the number of integers in the array.
- The next `n` integers are the array values.
- Values may span multiple lines because parsing is whitespace-based.

## Output Format
Print the sorted integers on one line, separated by single spaces. For an empty array, print an empty line.

## Time Complexity
Selection Sort always performs `n(n - 1) / 2` comparisons, so its best-case, average-case, and worst-case time complexity are all `O(n^2)`.

## Space Complexity
The algorithm sorts in place and uses only a constant number of extra variables, so its auxiliary space complexity is `O(1)` outside the input/output storage used by the runners.

## Why the challenge input is challenging
`inputs/input_challenge.txt` is reverse sorted. Selection Sort still performs the same quadratic number of comparisons for every ordering, but reverse order causes frequent minimum-index updates during each inner scan and swaps on nearly every outer pass. It is useful for demonstrating that Selection Sort does not benefit from already known order and remains quadratic even on structured inputs.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
12
64 25 12 22 11 -3 0 99 25 4 -10 8
```

## Intended Output
Expected output:

```text
-10 -3 0 4 8 11 12 22 25 25 64 99
```
