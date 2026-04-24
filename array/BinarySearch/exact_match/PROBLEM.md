# Binary Search - Exact Match

## What does this variant solve?
This variant answers the most direct binary-search question:

`Given a sorted array and a target value, is the target present, and if so, at which index?`

The implementation in this folder uses the classic range-halving method with two pointers:
- `left`
- `right`

At every step, the search keeps only the half of the range that can still contain the target.

## Why this is a separate learning topic
Exact-match binary search is the simplest form of binary search and is the right first mental model for students:
- compare with the middle value
- discard one half
- repeat until the interval is empty

It is different from boundary-style binary search.
Exact-match search is about finding one specific value.
Boundary search is about finding the first or last position where a monotonic condition changes.

## Core invariant
During the search, the algorithm maintains this invariant:

`If the target exists in the array, then it is somewhere inside the current closed interval [left, right].`

Each comparison preserves that statement:
- if `values[mid] == target`, the search is done
- if `values[mid] < target`, everything at or left of `mid` is too small, so the new range is `[mid + 1, right]`
- if `values[mid] > target`, everything at or right of `mid` is too large, so the new range is `[left, mid - 1]`

When `left > right`, the interval is empty, so the target is not present.

## Problem in this folder
Given:
- a sorted array
- several target queries

Run exact-match binary search for every query and print:
- the index of the target if it exists
- `-1` if it does not exist

Indices are zero-based.
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
Shared inputs live in `../inputs/`.

- Line 1: `n q`
- Next `n` lines: one sorted array value per line
- Next `q` lines: one query target per line

This exact-match topic assumes the array is sorted in non-decreasing order.
When duplicate values exist, any matching index would be a valid exact-match answer, but the provided inputs in this topic use distinct values so the output is unambiguous.

## Test Case
This is the test case currently used in `../inputs/exact_input.txt`:

```text
8 5
1
4
7
9
13
21
29
42
13
8
42
1
100
```

## Intended Output
Expected output:

```text
Exact-match results: 4 -1 7 0 -1
```
