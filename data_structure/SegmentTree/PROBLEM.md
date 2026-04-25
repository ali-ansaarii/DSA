# Segment Tree

## What is a Segment Tree?
A Segment Tree stores aggregate information over array intervals so that both:

- point updates
- range queries

can be answered in `O(log n)` time.

This topic uses the baseline variant:

- point-add update
- range-sum query

That makes it directly comparable with the Fenwick Tree topic while still
showing the more general interval-decomposition structure of a segment tree.

## Problem in this folder
Given:

- an initial integer array
- a sequence of update and sum operations

process the operations in order and print the result of every `sum` query.

Indices are zero-based in the input.
For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
This topic uses an iterative bottom-up segment tree stored in a flat array.

If the input length is `n`, the tree stores:

- leaves at positions `[n, 2n)`
- internal nodes at positions `[1, n)`

Each internal node stores the sum of its two children.

So:

- building the tree means filling the leaves from the input array and then
  computing parents bottom-up
- a point update changes one leaf and recomputes all ancestors up to the root
- a range sum decomposes the query interval into `O(log n)` disjoint covered
  nodes

## Why range queries are fast
To evaluate `sum(left, right)`, the algorithm works on the half-open interval:

- `[left, right + 1)`

after shifting both endpoints to the leaf layer.

While the two pointers move upward:

- if the left pointer is a right child, its node is fully inside the answer, so
  consume it and move to the next node
- if the right pointer is a right boundary, move it left first and consume that
  node
- then move both pointers to their parents

This collects only the nodes that exactly cover the query range.

## Why updates are fast
For `add index delta`:

1. move to the leaf that stores the single array element
2. apply the delta there
3. recompute every ancestor on the path to the root

That path has length `O(log n)`.

## Why this problem is a good baseline
This is the cleanest introduction because it shows:

- explicit interval decomposition
- the relationship between leaves and parents
- how the tree supports dynamic updates
- how a segment tree and a Fenwick tree solve the same baseline query class in
  different ways

It is also a natural stepping stone toward:

- range minimum / maximum trees
- lazy propagation
- custom associative operations

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

All implementations detect signed 64-bit overflow in maintained sums and report
it instead of silently wrapping.

## Time Complexity
- build: `O(n)`
- `add`: `O(log n)`
- `sum`: `O(log n)`
- total processing: `O(n + q log n)`

## Space Complexity
- `O(n)` for the segment-tree array
- plus `O(number of sum queries)` for collected outputs

## Why the challenge input is challenging
The challenge input uses:

- an array length that is a power of two
- updates concentrated near power-of-two boundaries
- a mix of whole-prefix, narrow, and suffix range sums

This stresses:

- correct handling of interval splitting in the iterative query loop
- off-by-one handling around inclusive input ranges
- repeated recomputation of shared ancestors near structural boundaries

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
