# 2D Prefix Sum

## What is 2D Prefix Sum?
A 2D Prefix Sum is a static range-query data structure for matrices. After one preprocessing pass, it can return the sum of any axis-aligned rectangular submatrix in constant time. It extends the one-dimensional prefix-sum idea by storing, for every matrix cell, the sum of all values in the rectangle from the matrix origin to that cell.

## Problem in this folder
Given an `R x C` integer matrix and `Q` rectangle-sum queries, output the sum of each requested rectangle. The matrix does not change between queries, so this is the baseline static rectangle-sum problem.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
Use a one-cell padded prefix table `prefix` with dimensions `(R + 1) x (C + 1)`, where `prefix[0][*]` and `prefix[*][0]` are zero. For a zero-based matrix cell `(r, c)`, store the sum of all matrix values in rows `0..r` and columns `0..c` at `prefix[r + 1][c + 1]`:

```text
prefix[r + 1][c + 1] = matrix[r][c]
                       + prefix[r][c + 1]
                       + prefix[r + 1][c]
                       - prefix[r][c]
```

The subtraction removes the top-left overlap counted by both neighboring prefix regions.

For an inclusive query `(r1, c1, r2, c2)`, the rectangle sum is computed by inclusion-exclusion:

```text
sum(r1, c1, r2, c2) = prefix[r2 + 1][c2 + 1]
                    - prefix[r1][c2 + 1]
                    - prefix[r2 + 1][c1]
                    + prefix[r1][c1]
```

The final addition restores the area above and left of the query rectangle because it was subtracted twice.

## Input Format
All implementations use the same whitespace-separated file format:

```text
R C
matrix_row_0_col_0 matrix_row_0_col_1 ... matrix_row_0_col_C-1
...
matrix_row_R-1_col_0 matrix_row_R-1_col_1 ... matrix_row_R-1_col_C-1
Q
r1 c1 r2 c2
...
```

- `R` is the number of rows.
- `C` is the number of columns.
- Matrix values are signed integers.
- `Q` is the number of rectangle queries.
- Each query uses zero-based, inclusive coordinates.
- Query coordinates are expected to satisfy `0 <= r1 <= r2 < R` and `0 <= c1 <= c2 < C`.

Each output line is the sum for one query, in input order.

## Time Complexity
- Preprocessing: `O(R * C)`
- Each query: `O(1)`
- Total for `Q` queries: `O(R * C + Q)`

## Space Complexity
`O(R * C)` for the padded prefix table.

## Why the challenge input is challenging
`inputs/input_challenge.txt` contains large positive and negative values that exceed 32-bit integer safety when accumulated over rectangles. It also includes border, single-cell, full-matrix, and sign-canceling queries to stress off-by-one errors in the padded table and the inclusion-exclusion formula. Correct implementations should use 64-bit sums.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
4 5
3 0 1 4 2
5 6 3 2 1
1 2 0 1 5
4 1 0 1 7
6
0 0 0 0
0 0 1 1
1 1 2 3
0 2 3 4
2 0 3 4
0 0 3 4
```

## Intended Output
Expected output:

```text
3
14
14
27
22
49
```
