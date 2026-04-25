# Ternary Search

## What is Ternary Search?
Ternary search is a divide-and-conquer search technique for unimodal data: data that increases up to one maximum and then decreases, or decreases down to one minimum and then increases. Instead of checking one midpoint like binary search, ternary search checks two interior points and discards the third of the search interval that cannot contain the optimum. This folder implements the discrete-array analogue of ternary search over unimodal functions.

## Problem in this folder
Given a non-empty discrete unimodal array of integers, return the index and value of its maximum element. The baseline assumes a single maximum: the values strictly increase until the peak and strictly decrease after it. Purely increasing or purely decreasing arrays are accepted as boundary cases where the maximum is at the right or left edge.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
Maintain a closed interval `[left, right]` that is guaranteed to contain the maximum. While the interval has more than four candidate positions, choose two interior indices:

- `mid1 = left + (right - left) / 3`
- `mid2 = right - (right - left) / 3`

If `array[mid1] < array[mid2]`, the maximum must be to the right of `mid1`, so discard `[left, mid1]`. If `array[mid1] > array[mid2]`, the maximum must be to the left of `mid2`, so discard `[mid2, right]`. If the two values are equal, keep the middle interval because, in a unimodal array, the peak cannot be outside both equal-height interior points. Once the interval is small, scan the remaining constant-size window and report the largest value.

## Input Format
All implementations read the same file format:

```text
n
a0 a1 a2 ... a(n-1)
```

- `n` is the number of elements and must be positive.
- The next `n` integers are the unimodal array values.
- Indices in the output are zero-based.

## Time Complexity
`O(log n)`. Each iteration removes roughly one third of the remaining candidate interval, and the final scan checks only a constant-size window.

## Space Complexity
`O(1)` auxiliary space for the search itself, excluding the input array used by the runner.

## Why the challenge input is challenging
`inputs/input_challenge.txt` is a monotone decreasing array, so the maximum is at index `0`. This stresses boundary handling and catches implementations that assume the peak is strictly inside the array or accidentally discard the left edge during interval updates.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
9
1 3 8 12 17 15 9 4 0
```

## Intended Output
Expected output:

```text
Maximum index: 4
Maximum value: 17
```
