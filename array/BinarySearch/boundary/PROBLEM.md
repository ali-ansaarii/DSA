# Binary Search - Boundary Search

## What does this variant solve?
This variant answers a different class of question:

`What is the first index where the array value becomes at least the target?`

That is the standard lower-bound problem.

For a sorted array `values`, the answer is the smallest index `i` such that:

`values[i] >= target`

If no such index exists, the answer is `n`, which is the insertion position at the end of the array.

## Why this is a separate learning topic
Boundary search is the more reusable binary-search pattern.
It is the form that appears behind:
- `lower_bound`
- insertion position
- first true in a monotonic boolean predicate
- many "binary search on answer" reductions

It is conceptually different from exact-match search:
- exact match asks whether one value exists
- boundary search asks where a monotonic condition switches from false to true

## Two implementations in this folder
This folder includes two correct ways to solve the same lower-bound problem.

### 1. Range-Halving Binary Search
This is the standard lower-bound pattern using a half-open interval `[left, right)`.

Invariant:
- every index strictly before `left` is known to be too small
- every index at or after `right` is a valid answer candidate

Update rule:
- if `values[mid] < target`, the boundary must be to the right of `mid`, so set `left = mid + 1`
- otherwise `mid` itself is a valid candidate, so keep it by setting `right = mid`

When `left == right`, that index is the first valid position.

### 2. Powers-of-Two Search
This implementation keeps one pointer `position` and tries to move it forward in decreasing jump sizes:
- first a large jump
- then half that jump
- then half again

Invariant:
- `position` is the last index known to satisfy `values[position] < target`

The algorithm tests whether jumping forward still stays on the "too small" side.
If it does, the jump is accepted.
After all jump sizes are processed, the boundary is `position + 1`.

This method is especially useful later in topics such as:
- Fenwick tree order statistics
- binary lifting style searches
- monotonic predicate searches where jump-based reasoning feels natural

## Problem in this folder
Given:
- a sorted array
- several target queries

For every query, compute the lower-bound index:
- the first index with `value >= target`
- or `n` if no such index exists

The default runners in this folder execute both implementations and print both result lists so students can compare them directly.
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
Shared inputs live in `../inputs/`.

- Line 1: `n q`
- Next `n` lines: one sorted array value per line
- Next `q` lines: one query target per line

This boundary-search topic assumes the array is sorted in non-decreasing order.
Duplicate values are allowed and are important, because lower-bound search is precisely about finding the first position in such runs.

## Test Case
This is the test case currently used in `../inputs/boundary_input.txt`:

```text
8 5
1
2
2
2
5
8
8
13
0
2
3
8
14
```

## Intended Output
Expected output:

```text
Boundary results (range-halving): 0 1 4 5 8
Boundary results (powers-of-two): 0 1 4 5 8
```
