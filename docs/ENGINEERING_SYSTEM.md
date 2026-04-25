# Repository Engineering System

## Purpose
This repository is no longer small enough to scale by hand-crafted repetition.

The goal of this system is:

- keep the implementation quality bar high
- reduce repeated setup and verification work
- make related topics easier to build in parallel
- keep the repository structurally consistent as it grows

This document defines the operating model for that.

## What We Learned From The First Wave
The current repository already has strong conventions:

- common topic layout
- separate `PROBLEM.md` and `USAGE.md`
- four language implementations
- shared inputs
- topic-level Makefiles
- smoke tests and benchmarks before publishing

The main bottleneck is not algorithm logic.
It is the repeated manual work around each topic:

- creating the same folder layout
- rewriting near-identical Makefiles
- recreating runner scaffolding
- manually remembering verification steps
- rediscovering the same review issues

That means the acceleration target is the workflow, not the quality bar.

## Design Principles

### 1. Standardize More, Not Less
Speed should come from codifying good practice, not relaxing standards.

The repository should use:

- standard scaffolds
- standard verification entry points
- standard benchmark naming
- standard parser/runner structure

### 2. Parallelize By Disjoint Ownership
Parallel work should be split so contributors do not step on the same files.

Preferred lanes for a single-topic implementation:

- lane A: docs, inputs, and Makefile
- lane B: C++ and Rust
- lane C: Python and Java

For sibling variants, ownership can also be split by variant folder.

### 3. Batch By Family
Related algorithms should be implemented in families when practical.

Examples:

- sorting family
- string matching family
- query/range data structures
- tree traversal family

This reduces context switching and increases reuse of inputs, docs structure,
and parser patterns.

### 4. Make Quality Verifiable
If a quality rule matters, it should be easy to run repeatedly.

That means:

- reusable verification scripts
- predictable Makefile targets
- stable benchmark target names
- consistent parser diagnostics

## Operating Model

### Phase 1: Scaffold
Use `scripts/scaffold_topic.py` to create the baseline structure for a new
single-topic algorithm.

The scaffold creates:

- standard folder layout
- standard per-language file layout
- standard topic Makefile
- `PROBLEM.md` and `USAGE.md` placeholders

The scaffold is intentionally generic.
It removes setup work, but algorithm-specific logic and docs still need to be
filled in carefully.

### Phase 2: Implement
After scaffolding:

- define the input contract first
- write the algorithm core next
- keep language runners aligned with the same input and output semantics

### Phase 3: Verify
Use `scripts/verify_topic.sh` to run the standard topic targets.

Default usage:

- smoke tests only: `scripts/verify_topic.sh <topic-dir>`
- smoke tests plus benchmarks: `scripts/verify_topic.sh <topic-dir> --benchmarks`

This script is not a replacement for judgment.
It is the common baseline check that every topic should pass before commit.

### Phase 4: Publish
After verification:

- update the local checklist
- split commits logically
- push branch
- open PR
- request Codex review

## Parallel Work Model

### Single Topic
Recommended split:

- worker 1 owns `inputs/`, `PROBLEM.md`, `USAGE.md`, `Makefile`
- worker 2 owns `cpp/` and `rust/`
- worker 3 owns `python/` and `java/`

Integration happens only after each lane has finished its owned files.

### Family Batch
Recommended split:

- worker 1 owns family docs and shared conventions
- worker 2 owns first topic or first variant subtree
- worker 3 owns second topic or second variant subtree

This works best when the topics share:

- input style
- runner structure
- benchmark semantics

## Quality Gates
Every completed topic should satisfy the same gates:

- topic structure follows repository rules
- four language implementations are present unless scope is explicitly narrowed
- input format is shared across languages
- `PROBLEM.md` explains the algorithm, not just commands
- `USAGE.md` explains how to run and benchmark
- smoke tests pass for every implemented language
- benchmark targets are run at least once when they exist
- benchmark scope is stated explicitly

## Near-Term System Roadmap
This repository now has two shared system components:

- topic scaffolding
- shared topic verification

The next likely reusable additions are:

- topic Makefile template extraction
- runner template families by topic class
- review-status helper for PR feedback polling
- pre-review checks for common Codex findings

## Scope Limits
This system is designed for the repository's current dominant pattern:

- one topic root
- one shared Makefile
- four language implementations
- inputs at topic root

Multi-variant topics may still need manual adjustment after scaffolding.
That is acceptable.
The system should reduce work first, then expand in controlled steps.
