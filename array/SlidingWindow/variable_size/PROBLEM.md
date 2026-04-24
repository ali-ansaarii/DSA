# Sliding Window, Variable Size

## What problem does this variant solve?
This variant solves problems where the best window length is not known in
advance and can expand or shrink while scanning the array.

In this folder, the concrete problem is:

- find the shortest contiguous subarray whose sum is at least a target

## Why positivity matters
This sliding-window pattern relies on all array values being positive.

That is the key property that makes the window sum monotonic:

- expanding the window always increases the sum
- shrinking the window always decreases the sum

Because of that, once the current sum reaches the target, we can safely shrink
from the left to search for a shorter valid window without missing a better
answer.

If negative values were allowed, that monotonic reasoning would break.

## Core invariant
At any moment, the algorithm maintains a window:

- `values[left..right]`

and its current sum.

The process is:

1. expand `right` until the window sum reaches or exceeds the target
2. while the window is still valid, shrink `left` to make it as short as
   possible
3. record the best valid window seen so far

Each index enters the window once and leaves it once, so the full algorithm is
linear.

## Problem in this folder
Given:

- a positive integer array
- a positive target sum

find the minimum-length contiguous subarray whose sum is at least the target.

If multiple windows have the same minimum length, the earliest one is reported.
If no such window exists, the program reports that no valid window exists.

Indices are zero-based.
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
- Line 1: `n target`
- Next `n` lines: one positive array value per line

Constraints enforced by the runners:

- `n >= 1`
- `target >= 1`
- every array value must be in the signed 64-bit range
- every array value must be strictly positive

All sums are treated as signed 64-bit integers in every language
implementation in this folder.
If the running window sum would overflow that range, the program reports
overflow and exits instead of silently wrapping.

## Time Complexity
- Each index enters the window once and leaves it once
- Total: `O(n)`

## Space Complexity
- `O(1)` extra space beyond the input array

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
8 7
2
1
5
2
3
2
1
1
```

## Intended Output
Expected output:

```text
Minimum window length: 2
Minimum window range: 2 3
```
