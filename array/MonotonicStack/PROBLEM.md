# Monotonic Stack

## What is a monotonic stack?
A monotonic stack is a stack that preserves an ordering property while we scan
through an array.

Common forms are:

- increasing stack
- decreasing stack

The purpose is not the stack itself.
The purpose is to discard elements that can no longer help answer future
queries.

## Problem in this folder
This folder uses the canonical monotonic-stack problem:

- for every array index, find the next greater element to its right

If there is no greater element to the right, the answer is `-1`.

Indices are zero-based.
For build, run, and benchmark commands, see `USAGE.md`.

## Why this problem is a good baseline
This is the cleanest way to learn the pattern because it shows:

- why elements are pushed onto the stack
- why smaller-or-equal elements become useless
- why each index is pushed once and popped once

The same idea later appears in:

- next smaller element
- stock span
- largest rectangle in histogram
- daily temperatures
- many range-boundary problems

## Core idea
We scan the array from right to left and maintain a stack of candidate values.

For the current value `values[i]`:

1. pop every stack value that is less than or equal to `values[i]`
2. after those pops:
   - the stack top, if it exists, is the next greater value
   - if the stack is empty, the answer is `-1`
3. push `values[i]` onto the stack

The stack stays strictly decreasing from bottom to top.

## Why popping works
Suppose we are processing `values[i]`.

If a stack top is:

- less than `values[i]`, it can never be the answer for `values[i]`
- and it can never be the answer for any earlier index either, because
  `values[i]` is closer and at least as large

So such elements are permanently useless and can be removed.

That is the key monotonic-stack insight:
- once an element loses future usefulness, discard it immediately

## Input Format
- Line 1: `n`
- Next `n` lines: one array value per line

Constraints enforced by the runners:

- `n >= 1`
- every value must fit in signed 64-bit range

The algorithm only compares values, so there is no arithmetic overflow risk in
the core logic.

## Time Complexity
- Each element is pushed at most once
- Each element is popped at most once
- Total: `O(n)`

## Space Complexity
- `O(n)` in the worst case for the stack and result array

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
5
2
1
2
4
3
```

## Intended Output
Expected output:

```text
Next greater elements: 4 2 4 -1 -1
```
