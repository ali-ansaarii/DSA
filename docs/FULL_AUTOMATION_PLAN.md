# Full Automation Plan

## Purpose
The repository now has a reusable acceleration layer:

- `scripts/scaffold_topic.py`
- `scripts/verify_topic.sh`
- `scripts/benchmark_with_memory.sh`
- `docs/ENGINEERING_SYSTEM.md`

The next goal is to build a higher-level automation system that can drive the
full repository workflow with minimal human intervention while preserving the
current quality bar.

This document defines that system before implementation.

## End Goal
One command should eventually be able to:

1. read the local checklist
2. pick the next algorithm to implement
3. create a branch
4. scaffold the topic
5. generate code, docs, and inputs
6. verify locally
7. commit and push
8. open a PR
9. request Codex review
10. poll for review feedback
11. apply fixes when the feedback is actionable
12. re-run verification
13. merge only when review is clean
14. mark the checklist item done
15. continue to the next algorithm

## Non-Goals
The first implementation should not attempt to solve everything.

Out of scope for the first version:

- parallel execution across multiple algorithms
- fully unattended recovery from merge conflicts
- automatic handling of missing toolchains
- auto-resolving review threads without a confirmed fix
- arbitrary self-healing around network or platform instability
- replacing the existing scaffold and verifier instead of using them

## Source Of Truth

### Checklist
The algorithm queue source of truth is:

- `.local/ALGORITHM_CHECKLIST.md`

The automation system should treat that file as the work queue and local state
signal for repository progress.

### GitHub State
GitHub is the source of truth for:

- PR existence
- PR review state
- merge state

### Local Run State
Automation-specific progress should be stored separately from the checklist in
a local-only run-state directory, for example:

- `.local/automation_runs/`

This state should make the system resumable after interruption.

## Design Principles

### 1. Reuse Existing Tooling
The automation system should wrap the current acceleration layer instead of
creating a second parallel workflow.

It should call:

- `scripts/scaffold_topic.py`
- `scripts/verify_topic.sh`
- topic Makefiles

### 2. Explicit State Machine
Every algorithm should move through named states. Silent partial progress is
not acceptable.

### 3. Stop On Ambiguity
If the system cannot confidently interpret a failure or review comment, it
should stop and mark the algorithm for manual attention rather than guessing.

### 4. Quality Before Throughput
The system should never merge an algorithm that failed local verification or
still has actionable review feedback.

### 5. Deterministic Side Effects
Branch names, commit messages, log locations, and PR operations should follow
predictable rules.

## High-Level Architecture

### Top-Level Controller
A top-level controller should orchestrate the full workflow.

Candidate entrypoint:

- `automation/run_factory.py`

Responsibilities:

- choose next work item
- advance the state machine
- call other automation components
- persist run state
- stop on policy violations

### Checklist Reader/Writer
Candidate module:

- `automation/checklist.py`

Responsibilities:

- parse `.local/ALGORITHM_CHECKLIST.md`
- pick the next unchecked algorithm
- mark progress only after merge

### Git Operations Layer
Candidate module:

- `automation/git_ops.py`

Responsibilities:

- create feature branches
- stage and commit
- push
- fetch and sync as needed
- guard against dirty state

### Model Layer
Candidate module:

- `automation/model.py`

Responsibilities:

- wrap OpenAI API calls
- provide generation and fix entrypoints
- capture prompts and outputs in logs
- enforce retry and cost limits

### GitHub Layer
Candidate module:

- `automation/github.py`

Responsibilities:

- create PRs
- request review
- poll review status
- extract actionable review feedback
- merge clean PRs

### Run-State Layer
Candidate directory:

- `.local/automation_runs/`

Responsibilities:

- persist state per algorithm
- persist logs
- allow resume after interruption
- persist a step-by-step progress manifest with timestamps and evidence links

### Prompt Layer
Candidate directory:

- `automation/prompts/`

Responsibilities:

- prompt template for initial generation
- prompt template for review-fix passes
- prompt template for summarizing verification failures

## State Machine
Each algorithm should advance through explicit states:

- `queued`
- `branch_created`
- `scaffolded`
- `generated`
- `verified`
- `committed`
- `pushed`
- `pr_open`
- `review_requested`
- `review_waiting`
- `review_fixing`
- `review_clean`
- `merged`
- `checklist_updated`
- `done`
- `failed`
- `manual_attention`

### State Notes

- `queued`
  - algorithm exists in checklist but has not started
- `branch_created`
  - feature branch exists locally
- `scaffolded`
  - topic skeleton exists
- `generated`
  - initial code/docs/inputs generated
- `verified`
  - local verification passed for current revision
- `committed`
  - current good revision committed
- `pushed`
  - remote branch updated
- `pr_open`
  - PR exists on GitHub
- `review_requested`
  - `@codex review` posted
- `review_waiting`
  - polling for review response
- `review_fixing`
  - applying a review-driven change
- `review_clean`
  - latest review reports no major issues
- `merged`
  - PR merged to `main`
- `checklist_updated`
  - local checklist updated
- `done`
  - all required post-merge steps complete
- `manual_attention`
  - workflow stopped for a human decision

## Workflow Definition

### Phase 1: Select Work
1. Read `.local/ALGORITHM_CHECKLIST.md`
2. Pick the next unchecked item according to current queue policy
3. Create a run-state file for that item

### Phase 2: Branch And Scaffold
1. Create a branch from `main`
2. Scaffold the topic using `scripts/scaffold_topic.py`
3. Validate scaffold success

### Phase 3: Generate
1. Generate algorithm-specific code, docs, and inputs
2. Keep outputs aligned with repository structure
3. Do not mark generated output as acceptable until verification passes

### Phase 4: Verify
1. Run `scripts/verify_topic.sh <topic-dir>`
2. If benchmarks are expected, run:
   - `scripts/verify_topic.sh <topic-dir> --benchmarks`
3. On failure:
   - collect failure output
   - attempt bounded fixes
   - stop with `manual_attention` if unresolved

### Phase 5: Commit And Publish
1. Stage only intended files
2. Create logical commits
3. Push branch
4. Open PR against `main`
5. Request review with `@codex review`

### Phase 6: Review Loop
1. Poll GitHub for review results
2. If review is clean:
   - continue to merge
3. If actionable feedback exists:
   - summarize feedback
   - apply bounded fixes
   - re-run verification
   - push
   - request review again

### Phase 7: Merge And Record
1. Merge only if:
   - verification passed
   - latest review is clean
2. Update local checklist
3. Mark run state `done`

## Safety Rules
These rules should be enforced in code.

- never merge if verification failed
- never merge if current actionable review feedback exists
- never continue after ambiguous or conflicting review feedback without
  escalation
- never overwrite unrelated files outside the intended topic scope
- never continue if git state is unexpectedly dirty
- never print or persist secrets
- never auto-resolve a review thread unless the fix is confirmed in code
- never run unbounded review/fix loops

## Retry And Stop Policy

### Suggested Limits
- max local generation attempts per algorithm: `2`
- max verification-fix attempts before PR: `3`
- max review-fix loops per PR: `3`
- max total automation attempts per algorithm before manual stop: `5`

### Review-Fix Bound
- A PR may receive at most `3` automation-driven review-fix rounds.
- If the PR still has actionable review feedback after the third fix round, it
  must not be merged automatically.
- In that case the run must be moved to `manual_attention` and kept out of the
  success path.

### Escalate To `manual_attention` When
- local verification still fails after bounded retries
- review comments are ambiguous or contradictory
- review comments remain actionable after `3` automation fix rounds
- toolchain is missing
- branch/merge state is inconsistent
- checklist parsing fails
- PR creation or merge policy cannot be completed safely

### Queue Continuation Policy
- In single-algorithm Phase B, `manual_attention` ends the run.
- In later queue-based phases, `manual_attention` on one algorithm must not stop
  the entire automation campaign.
- A blocked algorithm should be recorded, skipped, and left for human review
  while the controller proceeds to the next unchecked checklist item.

## Logging And Auditability
Each run should persist:

- chosen algorithm
- branch name
- current step and last completed step
- prompts sent to the model
- model outputs
- verification commands and results
- review summaries
- merge result

Suggested location:

- `.local/automation_runs/<algorithm-id>/`
- queue summaries under `.local/automation_queue_runs/<queue-run-id>/`

When queue mode uses disposable worktrees, the child runner must still write to
the shared canonical local root rather than to a worktree-local `.local`
directory. The checklist and run manifests must remain centralized.

Suggested files:

- `state.json`
- `progress.json`
- `generation.log`
- `verification.log`
- `review.log`
- `summary.txt`

### Progress Manifest
The automation should maintain a machine-readable progress manifest per run:

- `.local/automation_runs/<algorithm-id>/progress.json`

This file should be append-friendly and reflect what actually happened, not
what the controller hoped to do next.

Each recorded step should include:

- step name
- state before
- state after
- start timestamp
- end timestamp
- outcome (`success`, `failure`, `skipped`)
- evidence pointers
  - relevant log file
  - relevant commit hash if created
  - relevant PR number if created
- short human-readable note

The purpose of `progress.json` is:

- accurate resume behavior
- accurate post-run summaries
- easier debugging of partial or failed runs
- a durable audit trail for unattended execution

`state.json` remains the current snapshot of the run.
`progress.json` becomes the chronological history of what happened.

## Branch And Commit Policy

### Branch Naming
Use plain descriptive names consistent with repository rules.

Example:

- `heap-sort`
- `segment-tree`

### Commit Policy
Prefer small logical commits where feasible, but automation may initially use a
smaller number of structured commits for reliability.

Recommended first automation commit structure:

1. inputs
2. implementations
3. docs and orchestration

## PR Policy

- PR base branch: `main`
- PR creation: use `gh pr create`
- review request: post `@codex review`
- merge method: squash merge only

## Definition Of Done
An algorithm is done only when all of the following are true:

- PR merged into `main`
- latest review reported no major issues
- local checklist updated
- run state recorded as `done`

Anything short of that is not done.

## Phased Delivery Plan

### Phase A: Design And Foundation
Goal:

- finalize this plan
- keep the acceleration layer stable

Deliverables:

- `docs/FULL_AUTOMATION_PLAN.md`
- clarified state model
- agreed safety rules

### Phase B: Single-Algorithm MVP
Goal:

- automate one algorithm end-to-end

Suggested entrypoint:

- `python3 automation/run_factory.py --algorithm "Heap Sort"`

Must support:

- branch creation
- scaffold
- model generation
- verification
- commit/push
- PR creation
- review request
- review polling
- bounded fix loop
- merge when clean

### Phase C: Resume And Recovery
Goal:

- resume interrupted runs from saved state

Must support:

- restart after process crash
- restart after transient network failure
- no duplicate PR creation for the same state

### Phase D: Checklist Queue
Goal:

- run sequentially over multiple algorithms

Must support:

- pick next unchecked item
- isolate each algorithm run in a disposable worktree
- continue past `manual_attention` or other blocked runs
- update checklist after successful merge
- keep a queue-level summary of runnable, blocked, and completed items

### Phase E: Family Batching
Goal:

- improve throughput with deliberate batching

Possible families:

- sorting
- string matching
- query data structures
- tree families

### Phase F: Limited Parallelism
Goal:

- run multiple independent automation workers safely

This should only be attempted after the sequential system is stable.

## Implementation Checklist

### Phase A: Design And Foundation
- [x] Write the full automation plan
- [x] Define the state machine
- [x] Define safety rules and stop policy
- [x] Land the acceleration layer in `main`
- [ ] Review and close all open design questions for the MVP
- [ ] Freeze the Phase B scope before coding

### Phase B: Single-Algorithm MVP
- [ ] Create an `automation/` package with a stable module layout
- [ ] Implement run-state persistence under `.local/automation_runs/`
- [ ] Implement progress-manifest recording under `.local/automation_runs/`
- [ ] Implement checklist read support for a named algorithm
- [ ] Implement branch creation from `main`
- [ ] Implement scaffold invocation and validation
- [ ] Implement model-call wrapper with prompt logging
- [ ] Implement local verification orchestration
- [ ] Implement bounded pre-PR fix loop for verification failures
- [ ] Implement commit and push steps
- [ ] Implement PR creation through `gh`
- [ ] Implement review request with `@codex review`
- [ ] Implement review polling
- [ ] Implement actionable review extraction
- [ ] Implement bounded review-fix loop
- [ ] Implement squash merge when review is clean
- [ ] Implement checklist update after merge
- [ ] Implement structured summary output for the run

### Phase C: Resume And Recovery
- [ ] Resume a stopped run from `state.json`
- [ ] Detect and reuse an existing branch for the same run
- [ ] Detect and reuse an existing PR for the same run
- [ ] Avoid duplicate review-request comments when already waiting
- [ ] Stop cleanly on inconsistent local or GitHub state

### Phase D: Checklist Queue
- [ ] Select the next unchecked item automatically
- [ ] Process algorithms sequentially
- [ ] Stop on first blocked algorithm
- [ ] Record queue progress without corrupting checklist state

### Phase E: Family Batching
- [ ] Define how a family is represented in configuration
- [ ] Reuse prompts and scaffolds across a family
- [ ] Preserve the same verification and merge quality gates per topic

### Phase F: Limited Parallelism
- [ ] Define a locking strategy for checklist access
- [ ] Define a locking strategy for branch and PR ownership
- [ ] Ensure parallel workers cannot merge or mutate the same item
- [ ] Add worker-safe logging and run identification

## Acceptance Tests

### Phase B Acceptance: Single-Algorithm MVP
The MVP is acceptable only if all of the following pass on one real algorithm:

1. Starting from a clean `main`, one command creates a new branch and scaffold.
2. The run state is persisted before any irreversible step.
3. The progress manifest records every completed transition with timestamps and evidence pointers.
4. Generated files are written only inside the intended topic scope.
5. Local verification runs and its full output is captured in logs.
6. On successful verification, the system commits, pushes, and opens exactly one PR.
7. The PR receives exactly one review-request comment per review cycle.
8. If review returns actionable comments, the system applies a bounded fix loop and re-verifies before pushing.
9. If review returns clean, the system squash-merges and updates the local checklist.
10. At the end, the run is marked `done`, the working tree returns to a clean `main`, and the manifest history is sufficient to reconstruct the run.

### Phase C Acceptance: Resume And Recovery
Resume and recovery are acceptable only if all of the following pass:

1. Killing the process after branch creation and restarting resumes from the saved state instead of creating a new branch.
2. Killing the process after PR creation and restarting reuses the same PR.
3. Restarting while waiting for review does not post duplicate `@codex review` comments.
4. Restarting after a clean merge does not try to merge again.
5. Corrupted or contradictory state is detected and moved to `manual_attention`.
6. The recorded manifest is sufficient to explain why the resumed run chose its next action.

### Phase D Acceptance: Checklist Queue
Queue processing is acceptable only if all of the following pass:

1. The system picks the next unchecked algorithm deterministically.
2. A successful merge updates the checklist exactly once.
3. A blocked algorithm stops the queue and preserves logs and state for inspection.
4. Subsequent algorithms are not started after a blocked item.

### Phase E Acceptance: Family Batching
Batching is acceptable only if all of the following pass:

1. Family-level setup reduces repeated prompt and scaffold work.
2. Each algorithm still gets its own verification, PR, review, and merge decision.
3. A failure in one family member does not silently mark other family members done.

### Phase F Acceptance: Limited Parallelism
Parallel execution is acceptable only if all of the following pass:

1. Two workers cannot select the same checklist item.
2. Two workers cannot mutate the same branch or PR.
3. Logs and run-state files remain attributable to a single worker and algorithm.
4. A worker crash does not corrupt another worker's run state.

## MVP Recommendation
Build only the single-algorithm autopilot first.

That is the smallest unit that can prove:

- the state machine is correct
- the model integration is usable
- the GitHub review loop is survivable
- the logs are sufficient

Do not start with full-checklist autopilot.

## MVP Decisions
The following decisions are now fixed for the first implementation.

### Checklist Update
- The MVP should update `.local/ALGORITHM_CHECKLIST.md` automatically, but only
  after a confirmed clean merge.
- A run that merged successfully but failed to update the checklist should be
  marked `manual_attention`, not silently considered complete.

### Commit Policy
- The MVP should use one generated topic commit before PR creation.
- After merge, the checklist update remains a local-only side effect and is not
  part of the topic branch commit history.
- Multi-commit topic publication can be added later after the basic workflow is
  stable.

### Review Policy
- The MVP should stop on any actionable unresolved Codex review comment.
- The MVP should not attempt severity filtering in the first version.
- Any unresolved actionable comment should trigger the bounded review-fix loop.

### Review Polling Policy
- Poll every 120 seconds while waiting for review.
- Escalate to `manual_attention` after 30 minutes without a decisive review
  result.
- A decisive result means either:
  - a clean top-level review outcome with no actionable unresolved comments
  - or actionable feedback that the automation can attempt to fix

### Family Batching
- Family batching is deferred entirely to Phase E.
- The MVP should process exactly one named algorithm.
- Queue-based algorithm selection begins in Phase D, not in the first MVP.

## Phase B Scope Freeze
The first implementation must stay inside this boundary.

### Included In Phase B
- one named algorithm per run
- local run-state persistence
- branch creation from clean `main`
- topic scaffold invocation
- model-driven generation
- local verification
- one generated topic commit
- push and PR creation
- review request with `@codex review`
- review polling
- bounded review-fix loop
- squash merge on clean review
- local checklist update after merge

### Explicitly Excluded From Phase B
- automatic queue traversal across multiple algorithms
- family batching
- parallel workers
- automatic review-thread resolution
- merge-conflict recovery
- flaky toolchain recovery
- severity-based review triage
- any attempt to continue after `manual_attention`

## Immediate Next Step
Before writing implementation code:

1. review this plan
2. freeze the Phase B acceptance test set
3. create a fresh feature branch from `main` for the automation implementation
4. build only the Phase B single-algorithm MVP
