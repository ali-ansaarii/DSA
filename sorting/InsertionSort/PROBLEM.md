# Insertion Sort

## What is Insertion Sort?
Insertion Sort is a comparison-based sorting algorithm that builds the final sorted order one element at a time. It scans from left to right, treating the left prefix as already sorted, and inserts each new value into its correct position inside that prefix by shifting larger values one slot to the right. The algorithm sorts in-place, is stable when equal values are not moved past one another, and has quadratic worst-case time complexity.

## Problem in this folder
Given an array of signed 64-bit integers, sort the numbers in nondecreasing order using classical in-place stable insertion sort.

The implementations in this topic expose the core algorithm as a standalone function and keep file parsing, timing, and output in `main`.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
Before processing position `i`, the subarray `a[0..i-1]` is sorted. Store `a[i]` as the key, shift every element in the sorted prefix that is greater than the key one position to the right, and then write the key into the open position. Because only strictly greater elements are shifted, equal elements keep their original relative order, which makes the algorithm stable.

## Input Format
All implementations use the same whitespace-separated input format:

```text
n
x1 x2 x3 ... xn
```

- `n` is the number of integers.
- The next `n` tokens are signed 64-bit integers.
- The integers may appear on one line or across multiple lines.
- If `n` is `0`, the output is a blank line.

## Output Format
Print the sorted integers in nondecreasing order on one line, separated by single spaces.

## Time Complexity
- Best case: `O(n)` when the input is already sorted.
- Average case: `O(n^2)`.
- Worst case: `O(n^2)`, for example when the input is sorted in reverse order.

## Space Complexity
Insertion Sort is in-place and uses `O(1)` auxiliary space beyond the input array.

## Why the challenge input is challenging
`inputs/input_challenge.txt` is reverse-sorted. For insertion sort, every new key must move across the entire already-sorted prefix, producing the maximum number of comparisons and shifts: `n(n - 1) / 2`. This stresses the algorithm's quadratic worst-case behavior.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
12
5 -3 9 5 0 -9223372036854775808 42 7 -3 9223372036854775807 1 5
```

## Intended Output
Expected output:

```text
-9223372036854775808 -3 -3 0 1 5 5 5 7 9 42 9223372036854775807
```
