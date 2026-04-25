# Monotonic Queue

## What is a monotonic queue?
A monotonic queue is a deque that keeps its elements ordered while we scan
through a sequence.

The usual forms are:

- decreasing queue for window maximum
- increasing queue for window minimum

The key idea is the same as a monotonic stack:

- once an element can no longer become the answer to any future query, discard
  it immediately

The queue version matters when answers are needed over a **moving window**
instead of only looking to the left or right once.

## Problem in this folder
This folder uses the canonical monotonic-queue problem:

- compute the maximum of every contiguous subarray of fixed length `k`

For an array `values` and window size `k`, produce:

- `max(values[0..k-1])`
- `max(values[1..k])`
- `max(values[2..k+1])`
- and so on until the last full window

Indices are zero-based.
For build, run, and benchmark commands, see `USAGE.md`.

## Why this problem is a good baseline
This is the cleanest monotonic-queue example because it exposes all three rules
that make the data structure useful:

1. remove expired indices that fell out of the current window
2. remove dominated indices from the back because a newer, larger value makes
   them useless
3. read the current maximum from the front in `O(1)`

The same pattern later appears in:

- sliding window minimum
- shortest subarray with monotonic prefix structures
- dynamic programming optimizations
- many queue-based range-extremum problems

## Core idea
We scan the array from left to right and store **indices**, not raw values.

That matters because the algorithm must know:

- whether an index is still inside the current window
- and which value belongs to that index

The deque maintains candidate indices in decreasing value order from front to
back.

For each new index `i`:

1. remove the front index if it is no longer inside the current window
2. while the back index has a value less than or equal to `values[i]`, remove
   it
3. push `i` at the back
4. once we have processed at least `k` elements, the front index is the maximum
   of the current window

## Why popping from the back is correct
Suppose we are processing `values[i]`.

If the deque back points to some earlier index `j` with:

- `values[j] <= values[i]`

then index `j` is permanently useless:

- `i` is newer, so it remains valid in future windows for at least as long
- `values[i]` is at least as large, so `j` can never beat `i` as a maximum

So `j` should be removed immediately.

That is the central monotonic-queue idea:
- the deque stores only candidates that still have a chance to become a future
  window maximum

## Why the front is always the answer
The deque is kept in decreasing value order.

So:

- the front is always the largest candidate still inside the current window
- every older candidate behind it is smaller
- every expired candidate is removed before we query the answer

That makes the front the correct maximum for the current window.

## Why indices are necessary
If we stored only values, we could not tell whether the leftmost candidate had
fallen out of the window.

Using indices solves both problems:

- expiration is checked by index range
- value comparisons still work through `values[index]`

## Input Format
- Line 1: `n k`
- Next `n` lines: one array value per line

Constraints enforced by the runners:

- `n >= 1`
- `1 <= k <= n`
- every value must fit in signed 64-bit range

The core algorithm only compares values and moves indices through a deque, so
there is no arithmetic overflow risk in the algorithm itself.

## Time Complexity
- Each index enters the deque once
- Each index can be removed from the front at most once
- Each index can be removed from the back at most once
- Total: `O(n)`

## Space Complexity
- `O(k)` for the deque in the typical window view
- `O(n)` total output storage because this implementation returns every window
  maximum

## Why the challenge input is challenging
The challenge input mixes:

- long decreasing runs, which grow the deque
- sudden large spikes, which trigger many back pops
- equal-value plateaus, which test the `<=` tie-handling rule

So it stresses the two different queue-maintenance behaviors that students
usually confuse:

- expiration from the front
- domination pops from the back

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
8 3
1
3
-1
-3
5
3
6
7
```

## Intended Output
Expected output:

```text
Window maxima: 3 3 5 5 6 7
```
