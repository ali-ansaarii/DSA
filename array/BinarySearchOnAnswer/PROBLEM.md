# Binary Search on Answer

## What is Binary Search on Answer?
Binary Search on Answer is a technique for optimization problems where the possible answer values form an ordered range and a yes/no feasibility predicate is monotone over that range. Instead of searching through stored array indices, the algorithm searches the answer space itself: it asks whether a candidate value is achievable, then discards the half of the numeric range that cannot contain the optimum.

## Problem in this folder
Given an array of non-negative integers and an integer `k`, partition the array into at most `k` non-empty contiguous groups. Minimize the maximum sum among all groups and output that minimum possible maximum group sum.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
For a candidate maximum group sum `limit`, the feasibility predicate is:

> Can the array be split into at most `k` contiguous groups such that every group sum is `<= limit`?

This predicate is monotone:

- If `limit` is feasible, then every larger limit is also feasible.
- If `limit` is not feasible, then every smaller limit is also not feasible.

The smallest possible answer is at least `max(array)`, because every element must belong to some group. The largest useful answer is `sum(array)`, corresponding to one group containing the whole array. Binary search over this numeric range. For each candidate `mid`, greedily scan left to right and start a new group exactly when adding the next element would exceed `mid`. This greedy check uses the fewest groups possible for that `mid`, so it correctly decides feasibility.

## Input Format
All implementations read the same whitespace-separated file format:

```text
n k
a1 a2 a3 ... an
```

Where:

- `n` is the number of array elements.
- `k` is the maximum allowed number of contiguous groups.
- `a1 ... an` are non-negative integer values.

## Output Format
Print one integer: the minimum possible maximum group sum.

## Time Complexity
Let `S = sum(array)` and `M = max(array)`. The feasibility check is `O(n)`, and binary search performs `O(log(S - M + 1))` checks, so the total running time is:

```text
O(n log(S - M + 1))
```

## Space Complexity
The algorithm uses `O(1)` auxiliary space beyond the input array.

## Why the challenge input is challenging
`inputs/input_challenge.txt` contains large values near `10^12` mixed with tiny values. This creates a wide answer range, forcing many binary-search iterations, while the alternating pattern stresses the greedy feasibility boundary between forming a new group and extending the current group. It is intended to confirm that implementations use 64-bit integer arithmetic and do not confuse answer-space search with array-index search.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
7 3
7 2 5 10 8 1 4
```

## Intended Output
Expected output:

```text
14
```
