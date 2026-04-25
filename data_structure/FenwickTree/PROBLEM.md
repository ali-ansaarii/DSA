# Fenwick Tree

## What is a Fenwick Tree?
A Fenwick Tree, also called a Binary Indexed Tree, stores partial sums in a way
that supports:

- point updates
- prefix sum queries

both in `O(log n)` time.

This topic uses the classic extension:

- range sum query `sum(l, r) = prefix(r) - prefix(l - 1)`

So the external problem supports:

- `add index delta`
- `sum left right`

The internal structure still works by repeatedly combining **prefix**
contributions.

## Problem in this folder
Given:

- an initial integer array
- a sequence of update and sum operations

process the operations in order and print the results of every `sum` query.

Indices are zero-based in the input.
For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
The Fenwick Tree stores values in a 1-based internal array `tree`.

For each internal index `i`, `tree[i]` stores the sum of a suffix-sized block
ending at `i`.

The size of that block is:

- `lowbit(i) = i & -i`

That lowest set bit tells us how large the covered range is.

Examples:

- `i = 12` is `1100` in binary
- `lowbit(12) = 4`
- so `tree[12]` stores the sum of the last 4 elements ending at position 12 in
  the internal 1-based indexing

## Why prefix queries are fast
To compute a prefix sum up to index `r`, we:

1. move to internal index `r + 1`
2. add `tree[i]`
3. subtract `lowbit(i)` from `i`
4. repeat until `i = 0`

Each step jumps over one stored block.
So instead of summing every element, the query decomposes the prefix into
`O(log n)` disjoint blocks.

## Why updates are fast
For `add index delta`, we:

1. move to internal index `index + 1`
2. add `delta` to `tree[i]`
3. add `lowbit(i)` to `i`
4. repeat while `i` stays inside the tree

That visits exactly the internal nodes whose covered ranges include the updated
position.

## Why the 1-based indexing matters
Fenwick Trees are easiest to understand with 1-based internal indices because:

- `lowbit(i)` is zero only at `i = 0`
- jumping by `i += i & -i` and `i -= i & -i` works cleanly

The input for this repository still uses zero-based indices because that is the
external convention used in the other topics.

So every implementation performs this translation:

- external index `x`
- internal index `x + 1`

That off-by-one boundary is one of the main sources of mistakes, so it is worth
studying explicitly.

## Input Format
- Line 1: `n q`
- Next `n` lines: one initial array value per line
- Next `q` lines: one of
  - `add index delta`
  - `sum left right`

Constraints enforced by the runners:

- `n >= 1`
- `q >= 0`
- all indices must be in `[0, n)`
- for `sum`, `left <= right`
- all numeric values must fit in signed 64-bit range

All implementations detect signed 64-bit overflow in the maintained sums and
report it instead of silently wrapping.

## Time Complexity
- build by repeated point updates: `O(n log n)`
- `add`: `O(log n)`
- `sum`: `O(log n)`
- total processing: `O((n + q) log n)` with this baseline build strategy

## Space Complexity
- `O(n)` for the Fenwick tree
- plus `O(number of sum queries)` for the collected printed answers

## Why this problem is a good baseline
This is the cleanest Fenwick Tree introduction because it shows:

- why the structure is built around prefix sums
- how `lowbit` controls both update and query traversal
- how range sums are derived from prefix sums
- where 0-based external indexing and 1-based internal indexing meet

The same structure later appears in:

- inversion counting
- coordinate-compressed frequency tables
- order statistics with binary lifting on counts
- 2D Fenwick Tree variants

## Why the challenge input is challenging
The challenge input uses:

- an array length that is a power of two
- updates concentrated on indices near power-of-two boundaries
- a mix of single-point, prefix-wide, and suffix-wide sum ranges

That does not change the asymptotic complexity, but it is designed to stress:

- lowbit traversal patterns
- off-by-one boundary handling
- repeated reuse of the same high-level tree nodes

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
5 5
1
2
3
4
5
sum 0 4
add 2 5
sum 1 3
add 0 -1
sum 0 2
```

## Intended Output
Expected output:

```text
Query sums:
15
14
10
```
