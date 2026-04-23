# Inorder Traversal - Iterative

## What is Inorder Traversal?
Inorder traversal visits a binary tree in this order:
1. Traverse the left subtree.
2. Visit the current node.
3. Traverse the right subtree.

The iterative version simulates the call stack explicitly with its own stack.

## Problem in this folder
Given:
- number of nodes
- a root node
- left and right child indices for every node

Run iterative inorder traversal from the root and print the visitation order.

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
Inorder traversal order: 3 1 4 0 5 2 6
```
