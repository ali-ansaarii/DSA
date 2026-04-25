# Matrix Multiplication

## What is Matrix Multiplication?
Matrix multiplication combines an `m x n` matrix `A` with an `n x p` matrix `B` to produce an `m x p` matrix `C`, where each entry `C[i][j]` is the dot product of row `i` of `A` and column `j` of `B`. This topic implements the standard dense-matrix multiplication algorithm with a direct triple-loop computation.

## Problem in this folder
Given two compatible dense integer matrices, compute their product exactly and print the resulting matrix. All language implementations use the same input contract and produce byte-for-byte identical output for the same input.

For build, run, and benchmark commands, see `USAGE.md`.

## Core idea
For every output cell `(i, j)`, accumulate:

```text
C[i][j] = sum(A[i][k] * B[k][j]) for k = 0..n-1
```

The implementation evaluates this formula directly. It iterates over each row of the left matrix, each index in the shared dimension, and each column of the right matrix, adding every pairwise product `A[i][k] * B[k][j]` exactly once to the corresponding output cell.

## Input Format
All languages read the same dense-matrix file format:

```text
m n
A[0][0] A[0][1] ... A[0][n-1]
...
A[m-1][0] ... A[m-1][n-1]
n p
B[0][0] B[0][1] ... B[0][p-1]
...
B[n-1][0] ... B[n-1][p-1]
```

Requirements:
- `m`, `n`, and `p` are positive integers.
- The number of columns in `A` must equal the number of rows in `B`.
- Matrix values are parsed as signed integers.
- Implementations store and print products as 64-bit signed integers.

## Output Format
The output starts with the result dimensions and then prints one row per line:

```text
m p
C[0][0] C[0][1] ... C[0][p-1]
...
C[m-1][0] ... C[m-1][p-1]
```

## Time Complexity
The algorithm performs `m * n * p` multiply-add operations, so the time complexity is `O(mnp)`. For square `N x N` matrices, this is `O(N^3)`.

## Space Complexity
The algorithm allocates the output matrix, requiring `O(mp)` extra space beyond the input matrices, plus constant additional loop/index storage.

## Why the challenge input is challenging
`inputs/input_challenge.txt` multiplies a very wide `8 x 128` matrix by a tall `128 x 8` matrix. The result is small, but every output cell depends on a long dot product. This stresses accumulator correctness, rectangular-dimension handling, loop-bound edge cases, and cache behavior where repeatedly traversing the shared dimension dominates the work.

## Test Case
This is the test case currently used in `inputs/input.txt`:

```text
2 3
1 2 3
4 5 6
3 2
7 8
9 10
11 12
```

## Intended Output
Expected output:

```text
2 2
58 64
139 154
```
