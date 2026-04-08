# Agent Instructions for This Repository

## Project Goal
This repository collects implementations of data structures and algorithms in multiple programming languages.

## Organization
- Organize by topic first (example: `graph/DFS/recursive`).
- Keep language implementations for the same problem inside the same topic folder.
- If one algorithm has multiple variants (for example, `recursive` and `iterative`), use a parent topic folder named after the algorithm and place each variant in a child folder.
- In a single-variant topic folder, keep shared documentation and orchestration files at the topic root (`PROBLEM.md`, `USAGE.md`, `Makefile`), store test data under an `inputs/` subfolder, and place code under language subfolders.
- In a multi-variant topic parent, keep shared assets at the parent level (for example, `inputs/`, a parent `Makefile`) and keep variant-specific code/docs inside each child folder.
- Preferred language subfolders: `cpp/`, `python/`, `java/`, `rust/`.

### Topic Folder Layout (Preferred)
```
topic_name/
	inputs/
	PROBLEM.md
	USAGE.md
	Makefile
	cpp/
	python/
	java/
	rust/
```

### Variant Layout (When Needed)
```
algorithm_name/
	inputs/
	Makefile
	variant_one/
		PROBLEM.md
		Makefile
		cpp/
		python/
		java/
		rust/
	variant_two/
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
- If you add benchmarking or timing, keep the timer in `main` or a wrapper script, not inside the core algorithm function.
- Do not hardcode problem input values in source code.

## Input Rules
- Read input from external files (for example, `input.txt`).
- Use a consistent input format across languages for the same problem.
- Document the algorithm explanation, problem statement, input format, sample test case, and intended output in `PROBLEM.md`.
- Keep operational guidance such as available input files, run commands, and benchmark commands in a separate `USAGE.md` file so `PROBLEM.md` stays focused on understanding the algorithm.
- For single-variant topics too, prefer storing the actual input files under a dedicated `inputs/` folder instead of placing `input*.txt` directly at the topic root.
- If multiple variants share the same test data, store the files once in a shared parent `inputs/` folder instead of duplicating them in each variant folder.
- Prefer providing three kinds of inputs when practical:
  - one small/default input for correctness and easy manual inspection
  - one long general input for performance benchmarking on a representative workload
  - one intentionally challenging input designed to expose algorithm-specific weaknesses, edge cases, or worst-case behavior
- When you add a challenging input, document why it is challenging and what behavior it is intended to stress.

## Build and Run Rules
- Provide a simple build/run entry for each implementation (for example, a `Makefile` target for C++).
- Keep commands straightforward so they are easy for humans and agents to execute.
- Use one topic-level `Makefile` to orchestrate all language implementations for that topic.
- If a parent topic contains multiple variants, the parent `Makefile` may orchestrate those variant folders and each variant folder should still provide its own language-specific targets.
- Prefer explicit targets per language: `build_cpp`, `run_cpp`, `run_py`, `run_java`, `run_rs`.
- Keep `build` and `run` as convenience aliases (defaulting to C++ unless explicitly changed).
- Put build artifacts in language-local build folders, not in topic root (for example, `cpp/build/`).
- Ensure `clean` removes auxiliary files/folders for all languages (for example, `cpp/build/`, `python/__pycache__/`, `java/build/`, `rust/target/`).
- When build output is noisy, redirect it to topic-local `logs/` files and keep terminal output focused on the important run/benchmark results.

## Verification Rules
- Before committing, run at least one normal smoke test for each changed variant when the local toolchain is available.
- If you add or modify benchmark targets, run those benchmark targets at least once before committing when feasible.
- If a required language toolchain is unavailable or a verification step cannot be run, document that clearly.

## Benchmark Rules
- Be explicit about what a benchmark measures.
- Distinguish clearly between whole-program benchmarking and algorithm-only benchmarking.
- Benchmark target names and `PROBLEM.md` text should state whether timing includes only the algorithm call or also includes parsing, setup, and output.
- If a benchmark is intentionally adversarial, document whether failure is expected and what kind of limitation or worst-case behavior it is designed to expose.
- General benchmark targets should fail hard on unexpected runtime or build errors.
- Adversarial benchmarks may allow expected failures, but that behavior should be explicit in the target design and documentation.

## Path Rules
- Do not rely more than necessary on the shell's current working directory.
- In Makefiles, prefer deriving reusable paths from the Makefile location (for example, with `MAKEFILE_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))`).
- For shared repo-level helpers, prefer computing paths from a repo-root variable instead of chaining long relative paths such as `../../../...`.
- Programs may keep a simple fallback input path for direct manual runs, but normal build/run targets should pass input paths explicitly.

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
- Ignore topic-local `logs/` directories via `.gitignore`.
- Avoid leaving generated artifacts in the topic root after build/run.
- Avoid duplicating large shared inputs across sibling variant folders.
- When changing shared inputs, benchmark targets, folder layout, or orchestration, update all affected `PROBLEM.md` files and Makefiles in the same change.

## Shared Tooling
- If a helper script is useful across multiple algorithms, place it under a repo-root `scripts/` folder instead of inside one topic.
- Reusable helper scripts should exit non-zero on real failures by default.
- If a helper supports tolerated failures for educational or adversarial benchmarks, that should be an explicit opt-in mode.
- Keep reusable helper script output human-readable and stable so it can be interpreted consistently across topics.

## Commit Hygiene
- Prefer small, logically separated commits when a topic evolves in stages.
- When practical, split shared inputs, individual variant implementations, shared orchestration, and repo-wide hygiene updates into separate commits.

## Default Delivery Workflow
- If the user gives only an algorithm name or a similarly short implementation request, treat that as a request to run the full delivery flow end to end.
- Start by creating a dedicated branch from `main` for that algorithm before making code changes.
- Implement the topic following this repository's structure and language expectations, including inputs, `PROBLEM.md`, `Makefile`, and all required language implementations unless the user narrows the scope.
- Follow the same build and verification discipline used in prior topics: prepare the required small/default, long/general, and challenging inputs when practical, add the expected run and benchmark targets, and run the relevant smoke tests before committing.
- If verification succeeds, continue through the full publishing flow without waiting for an extra prompt: stage the intended files, create the appropriate commits, push the branch, and open a PR to `main`.
- If verification fails, stop before commit/push, summarize the blocker clearly, and ask the user how to proceed.
