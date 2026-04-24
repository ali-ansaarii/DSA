# Prefix Sum

## What is Prefix Sum?
Prefix sum is a preprocessing technique that turns repeated range-sum queries into constant-time lookups.

Instead of summing each query range from scratch, we build an auxiliary array:

`prefix[i] = sum of the first i elements`

That definition is deliberate:
- `prefix[0] = 0`
- `prefix[1] = values[0]`
- `prefix[2] = values[0] + values[1]`
- and so on

If the original array has length `n`, the prefix array has length `n + 1`.

## Why the `n + 1` form matters
Students often first imagine:

`prefix[i] = sum from values[0] through values[i]`

That version can work, but the `n + 1` version is cleaner for query logic because every inclusive range sum `[left, right]` becomes:

`prefix[right + 1] - prefix[left]`

This removes special cases for ranges that start at index `0`.

## Core idea
After preprocessing, the sum of:
- `values[left] + values[left + 1] + ... + values[right]`

is computed by:

`prefix[right + 1] - prefix[left]`

Why this works:
- `prefix[right + 1]` contains the sum of everything up to `right`
- `prefix[left]` contains the sum of everything before `left`
- subtracting them removes the unwanted prefix and leaves exactly the query range

## Problem in this folder
Given:
- an integer array
- several inclusive range-sum queries

Build the prefix-sum array and answer every query.

Indices are zero-based.
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
- Line 1: `n q`
- Next `n` lines: one array value per line
- Next `q` lines: `left right`

Each query asks for the inclusive sum over indices `[left, right]`.

All query indices must satisfy:
- `0 <= left <= right < n`

Values and range sums are treated as signed 64-bit integers in every language implementation in this folder.
If building the prefix array or answering a query would overflow that range, the program reports overflow and exits instead of silently wrapping.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
8 5
3
-2
5
1
-4
6
2
-1
0 0
0 2
2 5
1 7
4 7
```

## Intended Output
Expected output:

```text
Range-sum results: 3 6 8 7 3
```
