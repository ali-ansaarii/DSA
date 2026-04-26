# Kadane's Algorithm

## What is Kadane's Algorithm?
Kadane's Algorithm is a linear-time dynamic programming technique for finding a contiguous subarray with the maximum possible sum. Instead of checking every start and end position, it scans the array once while tracking the best subarray that must end at the current position and the best subarray found anywhere so far.

## Problem in this folder
Given a non-empty array of signed integers, find the maximum sum over all contiguous subarrays. This implementation reports:

- the maximum subarray sum,
- the inclusive zero-based start index of one optimal subarray,
- the inclusive zero-based end index of that subarray,
- and the selected subarray values.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
At each position `i`, the best subarray ending at `i` is either:

1. the previous best suffix extended by `array[i]`, or
2. a new subarray starting at `i`.

If extending the previous suffix is worse than starting fresh, the algorithm resets the current subarray at `i`; otherwise it extends. Whenever the current sum is greater than the best global sum, the global answer and its bounds are updated.

This topic uses the classical all-negative-safe baseline: initialization starts from the first element, not from zero. Therefore, when every value is negative, the answer is the largest single element. For ties, the implementations keep the earliest optimal subarray encountered by the left-to-right scan.

## Input Format
All language implementations use the same whitespace-separated file format:

```text
n
a1 a2 a3 ... an
```

- `n` is the number of elements and must be positive.
- `a1` through `an` are signed integers.
- Line breaks are flexible; any whitespace separation is accepted.

## Time Complexity
`O(n)`, because the array is scanned once.

## Space Complexity
`O(1)` auxiliary space for the algorithm itself, excluding the input array and the output subarray formatting.

## Why the challenge input is challenging
`inputs/input_challenge.txt` contains only negative numbers. Implementations that incorrectly initialize the best sum to `0` will return an empty subarray or sum `0`, which is invalid for this non-empty maximum-subarray problem. The correct behavior is to return the least negative single element.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
9
-2 1 -3 4 -1 2 5 -9 4
```

## Intended Output
Expected output:

```text
maximum_sum: 10
start_index: 3
end_index: 6
subarray: 4 -1 2 5
```
