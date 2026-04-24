# Sliding Window, Fixed Size

## What problem does this variant solve?
This variant solves problems where every candidate window has the same length.

Given:

- an array
- a fixed window size `k`

find the best contiguous subarray of exactly length `k`.

In this folder, "best" means:

- the maximum window sum

If multiple windows have the same maximum sum, the earliest one is reported.

## Why a sliding window helps
The naive approach recomputes the sum of each length-`k` subarray from scratch.

If there are `n` elements, that costs:

- `O(k)` per window
- `O((n - k + 1) * k)` overall

The sliding-window idea reuses work:

- start with the first window sum
- when the window moves right by one position:
  - subtract the value leaving the window
  - add the value entering the window

That makes each slide `O(1)`, so the full scan becomes `O(n)`.

## Core invariant
At any moment, the algorithm maintains the sum of exactly one window:

- `values[left..right]`

with:

- `right - left + 1 = k`

When the window slides:

- `left` increases by `1`
- `right` increases by `1`
- the sum is updated by removing the old left value and adding the new right value

This invariant is what makes the algorithm both fast and easy to reason about.

## Problem in this folder
Given:

- an integer array
- a fixed positive integer `k`

find the contiguous window of length `k` with the maximum sum.

Indices are zero-based.
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
- Line 1: `n k`
- Next `n` lines: one array value per line

Constraints enforced by the runners:

- `n >= 1`
- `1 <= k <= n`

All array values and window sums are treated as signed 64-bit integers in every
language implementation in this folder.
If a fixed-window sum would overflow that range, the program reports overflow
and exits instead of silently wrapping.

## Time Complexity
- Initial window sum: `O(k)`
- Sliding across the rest of the array: `O(n - k)`
- Total: `O(n)`

## Space Complexity
- `O(1)` extra space beyond the input array

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
6 3
2
1
5
1
3
2
```

## Intended Output
Expected output:

```text
Best window sum: 9
Best window range: 2 4
```
