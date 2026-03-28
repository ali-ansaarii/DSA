# Agent Instructions for This Repository

## Project Goal
This repository collects implementations of data structures and algorithms in multiple programming languages.

## Organization
- Organize by topic first (example: `graph/dfs_recursive`).
- Keep language implementations for the same problem inside the same topic folder.
- In each topic folder, keep shared files at the topic root (`input.txt`, `PROBLEM.md`, `Makefile`) and place code under language subfolders.
- Preferred language subfolders: `cpp/`, `python/`, `java/`, `rust/`.

### Topic Folder Layout (Preferred)
```
topic_name/
	input.txt
	PROBLEM.md
	Makefile
	cpp/
	python/
	java/
	rust/
```

## Implementation Rules
- Keep the core algorithm in a standalone function.
- Keep `main` separate from core algorithm logic when practical.
- `main` should only handle input parsing, setup, function invocation, and output.
- Do not hardcode problem input values in source code.

## Input Rules
- Read input from external files (for example, `input.txt`).
- Use a consistent input format across languages for the same problem.
- Document the problem, input format, sample test case, and intended output in one topic file: `PROBLEM.md`.

## Build and Run Rules
- Provide a simple build/run entry for each implementation (for example, a `Makefile` target for C++).
- Keep commands straightforward so they are easy for humans and agents to execute.
- Use one topic-level `Makefile` to orchestrate all language implementations for that topic.
- Prefer explicit targets per language: `build_cpp`, `run_cpp`, `run_py`, `run_java`, `run_rs`.
- Keep `build` and `run` as convenience aliases (defaulting to C++ unless explicitly changed).
- Put build artifacts in language-local build folders, not in topic root (for example, `cpp/build/`).
- Ensure `clean` removes auxiliary files/folders for all languages (for example, `cpp/build/`, `python/__pycache__/`, `java/build/`, `rust/target/`).

## Naming Rules
- For acronym-based algorithms, keep acronym capitalization in identifiers and algorithm files (example: `DFS`).
- Use `main` as the runner filename where language conventions allow (`main.cpp`, `main.py`, `main.rs`).
- For Java, keep public class/file naming conventions (for example, `Main.java`, `DFS.java`).

## Rust Rules
- For multi-file Rust implementations, prefer Cargo over raw `rustc` orchestration.
- Keep algorithm logic in `rust/src/<ALGO>.rs` and entrypoint in `rust/src/main.rs`.
- Use topic Makefile targets (`build_rs`, `run_rs`) to call Cargo.

## C++ Preferences
- Prefer modern C++ (C++20 or newer when available).
- Keep function-focused files clean and easy to read.
- `using namespace std;` is acceptable in this repository style for simplicity.
- Keep executable outputs in `cpp/build/` so generated binaries are easy to ignore.

## Hygiene Rules
- Ensure generated files are ignored via `.gitignore` (language caches, build outputs, binaries).
- Avoid leaving generated artifacts in the topic root after build/run.
