# Disjoint Set Union (DSU)

## What is DSU?
Disjoint Set Union, also called Union-Find, maintains a collection of disjoint sets over elements `0` to `n-1`.

It supports three core operations:
- `union a b`: merge the sets containing `a` and `b`
- `connected a b`: check whether `a` and `b` are in the same set
- `find a`: return the representative of the set containing `a`

This topic implements DSU with path compression and union by size.

## Problem in this folder
Given:
- number of elements
- a sequence of DSU operations

Process the operations in order and print the answers for `connected` and `find` queries.

Elements are numbered from `0` to `n-1`.
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
- Line 1: `n q`
- Next `q` lines: one of
  - `union a b`
  - `connected a b`
  - `find a`

All element indices must be in `[0, n)`.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
6 8
find 0
connected 0 1
union 0 1
union 1 2
connected 0 2
find 2
union 3 4
connected 2 4
```

## Intended Output
Expected output:

```text
Query results:
0
false
true
0
false
```
