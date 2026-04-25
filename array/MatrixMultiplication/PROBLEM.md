# Matrix Multiplication

## What is Matrix Multiplication?
Matrix multiplication combines an `m x n` matrix `A` with an `n x p` matrix `B` to produce an `m x p` matrix `C`, where each entry `C[i][j]` is the dot product of row `i` of `A` and column `j` of `B`. This family contains two implementations of the same dense-matrix operation: a classical triple-loop algorithm and a blocked algorithm that performs the same arithmetic in cache-friendlier tiles.

## Problem in this folder
Given two compatible dense integer matrices, compute their product exactly and print the resulting matrix. Both variants use the same input contract and produce byte-for-byte identical output for the same input.

For build, run, and benchmark commands, see `USAGE.md`.

## Variants in this family
- `classical/` uses the direct `O(mnp)` triple-loop method.
- `blocked/` uses the same `O(mnp)` arithmetic but groups iterations into square tiles to improve locality for large matrices.

The blocked version is included for systems reasons, not because it solves a different mathematical problem. Dense matrix multiplication is a standard example where asymptotic complexity alone does not explain performance: a loop order or tiling strategy can reduce cache misses and memory traffic while computing the same result.

## Core idea
For every output cell `(i, j)`, accumulate:

```text
C[i][j] = sum(A[i][k] * B[k][j]) for k = 0..n-1
```

The classical variant evaluates this directly. The blocked variant partitions the `i`, `k`, and `j` loops into fixed-size ranges and performs the same updates inside those ranges. Blocking preserves the invariant that every pairwise product `A[i][k] * B[k][j]` is added exactly once, but it tries to keep reused rows, columns, and partial sums closer to the CPU cache.

## Input Format
All variants and languages read the same dense-matrix file format:

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
Both variants perform `m * n * p` multiply-add operations, so the asymptotic time complexity is `O(mnp)`. For square `N x N` matrices, this is `O(N^3)`.

## Space Complexity
Both variants allocate the output matrix, requiring `O(mp)` extra space beyond the input matrices. The blocked variant uses only constant additional loop/index storage beyond the output.

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
