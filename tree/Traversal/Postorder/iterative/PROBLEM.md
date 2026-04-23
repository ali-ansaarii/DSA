# Postorder Traversal - Iterative

## What is Postorder Traversal?
Postorder traversal visits a binary tree in this order:
1. Traverse the left subtree.
2. Traverse the right subtree.
3. Visit the current node.

The iterative version here simulates recursion with an explicit stack and a per-node expanded-state flag.

## Problem in this folder
Given:
- number of nodes
- a root node
- left and right child indices for every node

Run iterative postorder traversal from the root and print the visitation order.

Nodes are numbered from `0` to `n-1`.
For build, run, and benchmark commands, see `USAGE.md`.

## Input Format
- Line 1: `n root`
- Next `n` lines: `left right`

Each child is either a node index in `[0, n)` or `-1` for a missing child.

## Test Case
This is the test case currently used in `../inputs/input.txt`:

```text
7 0
1 2
3 4
5 6
-1 -1
-1 -1
-1 -1
-1 -1
```

## Intended Output
Expected output:

```text
Postorder traversal order: 3 4 1 5 6 2 0
```
