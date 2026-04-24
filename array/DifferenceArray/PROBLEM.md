# Difference Array

## What is a Difference Array?
A difference array is a representation that makes repeated range updates cheap.

Instead of storing every value directly, we store how the array changes from one
position to the next:

- `diff[0] = values[0]`
- `diff[i] = values[i] - values[i - 1]` for `i > 0`

If we later reconstruct the original array by taking a prefix sum over `diff`,
we get the current values back.

## Why this is useful
Suppose we want to add `delta` to every element in an inclusive range
`[left, right]`.

Updating each element one by one costs:

- `O(right - left + 1)` per update

That is too expensive when there are many large updates.

With a difference array, the same range add becomes:

- `diff[left] += delta`
- if `right + 1 < n`, then `diff[right + 1] -= delta`

That is only `O(1)` work per update.

After all updates are recorded, one prefix-sum pass reconstructs the final array
in `O(n)`.

## Why this works
The difference array marks where an increment starts and where it stops.

For an update over `[left, right]`:

- adding `delta` at `left` means the prefix sum starts carrying that increment
- subtracting `delta` at `right + 1` means the prefix sum stops carrying it

So every index inside the range sees the added value, and every index after the
range returns to normal.

## Relationship to Prefix Sum
Prefix sum answers repeated range queries quickly after preprocessing.

Difference array applies repeated range updates quickly before reconstruction.

They are closely related:

- prefix sum accumulates values forward
- difference array stores local changes and relies on prefix accumulation to
  rebuild the array

That is why difference array is often taught immediately after prefix sum.

## Problem in this folder
Given:

- an initial integer array
- several inclusive range-add updates

Apply all updates efficiently and output the final array.

Indices are zero-based.
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
- Line 1: `n q`
- Next `n` lines: one initial array value per line
- Next `q` lines: `left right delta`

Each update means:

- add `delta` to every index from `left` through `right`, inclusive

All indices must satisfy:

- `0 <= left <= right < n`

All values, updates, intermediate states, and final answers are treated as
signed 64-bit integers in every language implementation in this folder.
If building the difference array, applying an update, or reconstructing the
final array would overflow that range, the program reports overflow and exits
instead of silently wrapping.

## Core Operations
The implementations separate three logical operations:

1. build the difference array from the initial values
2. apply each range-add update in `O(1)`
3. reconstruct the final values with one prefix-sum pass

This keeps the algorithm itself easy to study without mixing it with parsing or
benchmark code.

## Time Complexity
- Building the difference array: `O(n)`
- Applying `q` range updates: `O(q)`
- Reconstructing the final array: `O(n)`
- Total: `O(n + q)`

## Space Complexity
- `O(n)` for the difference array

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
6 4
10
20
30
40
50
60
0 2 5
1 4 -10
3 5 7
5 5 -3
```

## Intended Output
Expected output:

```text
Final array: 15 15 25 37 47 64
```
