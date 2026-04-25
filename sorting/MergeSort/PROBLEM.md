# Merge Sort

## What is Merge Sort?
Merge Sort is a stable, divide-and-conquer sorting algorithm. It recursively splits an array into two halves, sorts each half, and then merges the two sorted halves back together. Because every level of recursion processes all elements once and there are logarithmically many levels, top-down merge sort guarantees `O(n log n)` running time regardless of the original input order.

## Problem in this folder
Given an array of signed 64-bit integers, output the same values in nondecreasing order using top-down Merge Sort.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
The recursive invariant is: after sorting a subarray `[left, right)`, every element in that range is in nondecreasing order and the relative order of equal values from the original range is preserved. The algorithm sorts `[left, mid)` and `[mid, right)`, then merges them by repeatedly taking the smaller front value. When the two front values are equal, the value from the left half is taken first, which is what preserves stability.

## Input Format
All implementations use the same whitespace-separated input format:

```text
n
x1 x2 x3 ... xn
```

- `n` is the number of integers.
- The next `n` tokens are signed 64-bit integers.
- The integers may appear on one line or across multiple lines.

## Output Format
The sorted integers are printed on one line separated by single spaces, followed by a newline. For an empty input array, the output is a blank line.

## Time Complexity
Merge Sort always takes `O(n log n)` time for `n` elements in the best, average, and worst cases. Its running time is not degraded by already sorted, reverse sorted, duplicate-heavy, or otherwise adversarial value orderings.

## Space Complexity
This top-down implementation uses `O(n)` auxiliary memory for the merge buffer, plus `O(log n)` recursion stack space. It is not an in-place sort.

## Why the challenge input is challenging
`inputs/input_challenge.txt` is reverse sorted and includes many duplicate values as well as the minimum and maximum signed 64-bit integer values. Reverse order stresses the merge logic because many elements must move across halves, duplicates exercise stability-preserving tie handling, and the extreme values verify that implementations compare signed 64-bit integers without narrowing or overflow-prone arithmetic.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
12
5 -3 9223372036854775807 0 -3 42 -9223372036854775808 17 17 8 -1 5
```

## Intended Output
Expected output:

```text
-9223372036854775808 -3 -3 -1 0 5 5 8 17 17 42 9223372036854775807
```
