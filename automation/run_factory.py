from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from automation import checklist as checklist_ops
from automation import git_ops, github, model, scaffold, specs, state, verify
from automation.shell import CommandError


class AutomationRunner:
    def __init__(self, repo_root: Path, args: argparse.Namespace) -> None:
        self.repo_root = repo_root
        self.args = args
        self.spec = self._resolve_spec()
        self.paths = state.RunPaths.create(
            self.repo_root / ".local" / "automation_runs",
            self.spec.run_id,
        )
        self.store = state.RunStore(self.paths)
        self.snapshot, self._state_persisted = self._load_or_initialize_snapshot()
        self.model_client: model.ResponsesModelClient | None = None

    def _resolve_spec(self) -> specs.AlgorithmSpec:
        catalog_path = Path(self.args.catalog)
        catalog_spec = specs.load_spec_from_catalog(catalog_path, self.args.algorithm)
        if catalog_spec is not None:
            return catalog_spec
        return specs.build_spec_from_args(self.args)

    def _load_or_initialize_snapshot(self) -> tuple[state.RunSnapshot, bool]:
        if self.paths.state_path.exists():
            snapshot = self.store.load_snapshot()
            expected = (
                snapshot.algorithm_name == self.spec.algorithm_name
                and snapshot.branch_name == self.spec.branch_name
                and snapshot.topic_path == self.spec.topic_path
            )
            if not expected:
                raise RuntimeError(
                    "existing run state does not match the requested algorithm spec"
                )
            return snapshot, True
        snapshot = state.RunSnapshot(
            run_id=self.spec.run_id,
            algorithm_name=self.spec.algorithm_name,
            checklist_label=self.spec.checklist_label,
            branch_name=self.spec.branch_name,
            topic_path=self.spec.topic_path,
            display_name=self.spec.display_name,
            pr_title=self.spec.pr_title,
        )
        return snapshot, False

    def run(self) -> None:
        try:
            self._run_loop()
        except Exception as exc:
            self._mark_manual_attention(f"automation stopped: {exc}")
            raise

    def _run_loop(self) -> None:
        while self.snapshot.current_state not in state.TERMINAL_STATES:
            if self.args.stop_after and self.snapshot.current_state == self.args.stop_after:
                self.store.append_summary(f"stopped after requested state: {self.args.stop_after}")
                return

            current = self.snapshot.current_state
            if current == state.STATE_QUEUED:
                self._create_branch()
            elif current == state.STATE_BRANCH_CREATED:
                self._scaffold_topic()
            elif current == state.STATE_SCAFFOLDED:
                self._generate_topic()
            elif current == state.STATE_GENERATED:
                self._verify_topic()
            elif current == state.STATE_VERIFIED:
                self._commit_topic()
            elif current == state.STATE_COMMITTED:
                self._push_topic()
            elif current == state.STATE_PUSHED:
                if self.snapshot.pr_number is None:
                    self._open_pr()
                else:
                    self._request_review()
            elif current == state.STATE_PR_OPEN:
                self._request_review()
            elif current == state.STATE_REVIEW_REQUESTED:
                self.snapshot = self.store.transition(
                    self.snapshot,
                    step_name="enter_review_wait",
                    next_state=state.STATE_REVIEW_WAITING,
                    note="review requested; waiting for Codex response",
                )
            elif current == state.STATE_REVIEW_WAITING:
                self._poll_review()
            elif current == state.STATE_REVIEW_FIXING:
                self._apply_review_fix()
            elif current == state.STATE_REVIEW_CLEAN:
                self._merge_pr()
            elif current == state.STATE_MERGED:
                self._update_checklist()
            elif current == state.STATE_CHECKLIST_UPDATED:
                self.snapshot = self.store.transition(
                    self.snapshot,
                    step_name="complete_run",
                    next_state=state.STATE_DONE,
                    evidence={"run_dir": str(self.paths.run_dir)},
                    note="run completed successfully",
                )
                self.store.append_summary("run completed successfully")
            else:
                raise RuntimeError(f"unsupported state: {current}")

    def _topic_dir(self) -> Path:
        return self.repo_root / self.spec.topic_path

    def _ensure_model_client(self) -> model.ResponsesModelClient:
        if self.model_client is None:
            self.model_client = model.ResponsesModelClient.from_environment(self.repo_root)
        return self.model_client

    def _create_branch(self) -> None:
        git_ops.ensure_clean_base_branch(self.repo_root, self.args.base_branch)
        if not self._state_persisted:
            self.store.initialize(self.snapshot)
            self.store.append_summary(f"initialized run for {self.spec.algorithm_name}")
            self._state_persisted = True
        git_ops.create_branch(self.repo_root, self.spec.branch_name)
        self.snapshot = self.store.transition(
            self.snapshot,
            step_name="create_branch",
            next_state=state.STATE_BRANCH_CREATED,
            evidence={"branch": self.spec.branch_name},
            note=f"created branch {self.spec.branch_name}",
        )

    def _scaffold_topic(self) -> None:
        self._ensure_run_branch_checked_out()
        scaffold.invoke_scaffold(self.repo_root, self.spec)
        expected = scaffold.validate_scaffold(self.repo_root, self.spec)
        self.snapshot = self.store.transition(
            self.snapshot,
            step_name="scaffold_topic",
            next_state=state.STATE_SCAFFOLDED,
            evidence={"files": expected},
            note=f"scaffolded {self.spec.topic_path}",
        )

    def _generate_topic(self) -> None:
        self._ensure_run_branch_checked_out()
        self.snapshot.generation_attempts += 1
        self.store.save_snapshot(self.snapshot)
        result = self._ensure_model_client().generate_initial_bundle(
            repo_root=self.repo_root,
            spec=self.spec,
        )
        self._log_model_call(self.paths.generation_log_path, "initial_generation", result)
        changed = self._apply_file_bundle(result.bundle)
        self.snapshot = self.store.transition(
            self.snapshot,
            step_name="generate_topic",
            next_state=state.STATE_GENERATED,
            evidence={"files_written": changed},
            note=result.bundle.summary,
        )

    def _verify_topic(self) -> None:
        self._ensure_run_branch_checked_out()
        try:
            stdout, stderr = verify.run_verification(
                self.repo_root,
                self.spec.topic_path,
                benchmarks=self.spec.benchmark_expected,
            )
        except CommandError as exc:
            verification_output = _combine_output(exc.result.stdout, exc.result.stderr)
            _append_text(self.paths.verification_log_path, verification_output)
            if self.snapshot.verification_fix_attempts >= self.args.max_verification_fixes:
                raise RuntimeError("verification failed after bounded local fix attempts")
            self.snapshot.verification_fix_attempts += 1
            self.store.save_snapshot(self.snapshot)
            result = self._ensure_model_client().generate_verification_fix_bundle(
                repo_root=self.repo_root,
                spec=self.spec,
                verification_output=verification_output,
            )
            self._log_model_call(self.paths.generation_log_path, "verification_fix", result)
            changed = self._apply_file_bundle(result.bundle)
            self.snapshot = self.store.transition(
                self.snapshot,
                step_name="apply_verification_fix",
                next_state=state.STATE_GENERATED,
                evidence={"files_written": changed},
                note=result.bundle.summary,
            )
            return

        verification_output = _combine_output(stdout, stderr)
        _append_text(self.paths.verification_log_path, verification_output)
        self.snapshot = self.store.transition(
            self.snapshot,
            step_name="verify_topic",
            next_state=state.STATE_VERIFIED,
            evidence={"log": str(self.paths.verification_log_path)},
            note="local verification passed",
        )

    def _commit_topic(self) -> None:
        self._ensure_run_branch_checked_out()
        git_ops.stage_paths(self.repo_root, [self.spec.topic_path])
        commit_message = (
            f"Add {self.spec.display_name}"
            if self.snapshot.pr_number is None
            else f"Fix {self.spec.display_name} review feedback"
        )
        git_ops.commit(self.repo_root, commit_message)
        self.snapshot.latest_commit = git_ops.current_commit(self.repo_root)
        self.snapshot = self.store.transition(
            self.snapshot,
            step_name="commit_topic",
            next_state=state.STATE_COMMITTED,
            evidence={"commit": self.snapshot.latest_commit},
            note=commit_message,
        )

    def _push_topic(self) -> None:
        self._ensure_run_branch_checked_out()
        if self.snapshot.pr_number is None:
            git_ops.push_new_branch(self.repo_root, self.spec.branch_name)
        else:
            git_ops.push_current_branch(self.repo_root)
        self.snapshot = self.store.transition(
            self.snapshot,
            step_name="push_topic",
            next_state=state.STATE_PUSHED,
            evidence={
                "branch": self.spec.branch_name,
                "pr_number": self.snapshot.pr_number,
            },
            note="pushed branch to origin",
        )

    def _open_pr(self) -> None:
        self._ensure_run_branch_checked_out()
        body = (
            f"Automated Phase B MVP delivery for `{self.spec.display_name}`.\n\n"
            f"- Topic path: `{self.spec.topic_path}`\n"
            f"- Checklist label: `{self.spec.checklist_label}`\n"
            f"- Generated by `automation/run_factory.py`\n"
        )
        pr_number, pr_url = github.create_pr(
            self.repo_root,
            title=self.spec.pr_title,
            body=body,
            base=self.args.base_branch,
            head=self.spec.branch_name,
        )
        self.snapshot.pr_number = pr_number
        self.snapshot.pr_url = pr_url
        self.snapshot = self.store.transition(
            self.snapshot,
            step_name="open_pr",
            next_state=state.STATE_PR_OPEN,
            evidence={"pr_number": pr_number, "pr_url": pr_url},
            note=f"opened PR #{pr_number}",
        )

    def _request_review(self) -> None:
        self._ensure_run_branch_checked_out()
        assert self.snapshot.pr_number is not None
        github.request_codex_review(self.repo_root, self.snapshot.pr_number)
        self.snapshot = self.store.transition(
            self.snapshot,
            step_name="request_review",
            next_state=state.STATE_REVIEW_REQUESTED,
            evidence={"pr_number": self.snapshot.pr_number},
            note="requested Codex review",
        )

    def _poll_review(self) -> None:
        self._ensure_run_branch_checked_out()
        assert self.snapshot.pr_number is not None
        progress = self.store.load_progress()
        entered_wait_at = _state_entered_at(progress, state.STATE_REVIEW_WAITING)
        latest_review_request_at = _latest_step_timestamp(progress, "request_review")
        if entered_wait_at is None:
            entered_wait_at = datetime.now(tz=UTC)

        while True:
            status = github.fetch_review_status(
                self.repo_root,
                self.snapshot.pr_number,
                not_before=latest_review_request_at.isoformat() if latest_review_request_at else None,
            )
            _append_text(
                self.paths.review_log_path,
                json.dumps(
                    {
                        "observed_at": datetime.now(tz=UTC).isoformat(timespec="seconds"),
                        "state": status.state,
                        "latest_bot_comment": status.latest_bot_comment,
                        "actionable_count": len(status.actionable_comments),
                    },
                    indent=2,
                    sort_keys=True,
                ),
            )

            if status.state == "clean":
                self.snapshot = self.store.transition(
                    self.snapshot,
                    step_name="review_clean",
                    next_state=state.STATE_REVIEW_CLEAN,
                    evidence={"pr_number": self.snapshot.pr_number},
                    note=status.latest_bot_comment or "Codex review clean",
                )
                return

            if status.state == "actionable":
                if self.snapshot.review_fix_attempts >= self.args.max_review_fixes:
                    raise RuntimeError("review returned actionable comments after bounded fix attempts")
                self.snapshot.review_fix_attempts += 1
                self.store.save_snapshot(self.snapshot)
                self._cached_review_comments = status.actionable_comments
                self.snapshot = self.store.transition(
                    self.snapshot,
                    step_name="review_actionable",
                    next_state=state.STATE_REVIEW_FIXING,
                    evidence={"comments": len(status.actionable_comments)},
                    note="Codex review returned actionable unresolved comments",
                )
                return

            elapsed = datetime.now(tz=UTC) - entered_wait_at
            if elapsed.total_seconds() >= self.args.review_timeout_seconds:
                raise RuntimeError("timed out waiting for a decisive review result")
            time.sleep(self.args.poll_interval_seconds)

    def _apply_review_fix(self) -> None:
        self._ensure_run_branch_checked_out()
        comments = getattr(self, "_cached_review_comments", None)
        if not comments:
            raise RuntimeError("review_fixing state entered without cached actionable comments")
        result = self._ensure_model_client().generate_review_fix_bundle(
            repo_root=self.repo_root,
            spec=self.spec,
            review_comments=comments,
        )
        self._log_model_call(self.paths.review_log_path, "review_fix", result)
        changed = self._apply_file_bundle(result.bundle)
        self.snapshot = self.store.transition(
            self.snapshot,
            step_name="apply_review_fix",
            next_state=state.STATE_GENERATED,
            evidence={"files_written": changed},
            note=result.bundle.summary,
        )
        self._cached_review_comments = None

    def _merge_pr(self) -> None:
        self._ensure_run_branch_checked_out()
        assert self.snapshot.pr_number is not None
        github.merge_pr(self.repo_root, self.snapshot.pr_number)
        git_ops.checkout_base_branch(self.repo_root, self.args.base_branch)
        git_ops.pull_base_ff_only(self.repo_root, self.args.base_branch)
        try:
            git_ops.delete_local_branch(self.repo_root, self.spec.branch_name)
        except Exception:
            pass
        self.snapshot = self.store.transition(
            self.snapshot,
            step_name="merge_pr",
            next_state=state.STATE_MERGED,
            evidence={
                "pr_number": self.snapshot.pr_number,
                "base_commit": git_ops.current_commit(self.repo_root),
            },
            note=f"merged PR #{self.snapshot.pr_number}",
        )

    def _update_checklist(self) -> None:
        checklist_path = self.repo_root / ".local" / "ALGORITHM_CHECKLIST.md"
        updated = checklist_ops.mark_algorithm_done(checklist_path, self.spec.checklist_label)
        self.snapshot = self.store.transition(
            self.snapshot,
            step_name="update_checklist",
            next_state=state.STATE_CHECKLIST_UPDATED,
            evidence={"updated_entries": updated},
            note=f"updated checklist label {self.spec.checklist_label}",
        )

    def _apply_file_bundle(self, bundle: model.FileBundle) -> list[str]:
        if not bundle.files:
            raise RuntimeError("model returned an empty file bundle")

        topic_dir = self._topic_dir().resolve()
        changed: list[str] = []
        for entry in bundle.files:
            target = self._normalize_bundle_path(entry.path, topic_dir)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(entry.content, encoding="utf-8")
            changed.append(target.relative_to(self.repo_root).as_posix())
        return changed

    def _ensure_run_branch_checked_out(self) -> None:
        current = git_ops.current_branch(self.repo_root)
        if current != self.spec.branch_name:
            git_ops.checkout_branch(self.repo_root, self.spec.branch_name)

    def _normalize_bundle_path(self, raw_path: str, topic_dir: Path) -> Path:
        relative_candidate = Path(raw_path)
        if relative_candidate.is_absolute():
            raise RuntimeError(f"model returned an absolute path: {raw_path}")

        spec_prefix = Path(self.spec.topic_path)
        if relative_candidate.parts[: len(spec_prefix.parts)] == spec_prefix.parts:
            target = (self.repo_root / relative_candidate).resolve()
        else:
            target = (topic_dir / relative_candidate).resolve()

        try:
            target.relative_to(topic_dir)
        except ValueError as exc:
            raise RuntimeError(f"model attempted to write outside topic scope: {raw_path}") from exc
        return target

    def _log_model_call(
        self,
        log_path: Path,
        label: str,
        result: model.ModelCallResult,
    ) -> None:
        payload = {
            "label": label,
            "prompt": result.prompt,
            "raw_response": result.raw_response,
            "summary": result.bundle.summary,
            "files": [file.path for file in result.bundle.files],
        }
        _append_text(log_path, json.dumps(payload, indent=2, sort_keys=True))

    def _mark_manual_attention(self, note: str) -> None:
        if self.snapshot.current_state in state.TERMINAL_STATES:
            return
        try:
            self.snapshot = self.store.transition(
                self.snapshot,
                step_name="manual_attention",
                next_state=state.STATE_MANUAL_ATTENTION,
                outcome="failure",
                note=note,
                evidence={"run_dir": str(self.paths.run_dir)},
            )
        except Exception:
            self.store.append_summary(note)


def _state_entered_at(progress: list[dict], state_name: str) -> datetime | None:
    for entry in reversed(progress):
        if entry.get("state_after") == state_name:
            value = entry.get("end_timestamp")
            if value:
                return datetime.fromisoformat(value)
    return None


def _latest_step_timestamp(progress: list[dict], step_name: str) -> datetime | None:
    for entry in reversed(progress):
        if entry.get("step_name") == step_name:
            value = entry.get("end_timestamp")
            if value:
                return datetime.fromisoformat(value)
    return None


def _combine_output(stdout: str, stderr: str) -> str:
    stdout = stdout.strip()
    stderr = stderr.strip()
    if stdout and stderr:
        return f"{stdout}\n\n[stderr]\n{stderr}\n"
    return stdout or stderr


def _append_text(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text.rstrip() + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Phase B single-algorithm automation MVP")
    parser.add_argument("--algorithm", required=True, help="Checklist/display name for the algorithm run")
    parser.add_argument(
        "--catalog",
        default="automation/algorithm_catalog.json",
        help="Optional JSON catalog mapping algorithm names to scaffold specs",
    )
    parser.add_argument("--topic-path")
    parser.add_argument("--display-name")
    parser.add_argument("--algo-id")
    parser.add_argument("--binary-name")
    parser.add_argument("--time-flag")
    parser.add_argument("--branch-name")
    parser.add_argument("--pr-title")
    parser.add_argument("--checklist-label")
    parser.add_argument("--prompt-notes")
    parser.add_argument("--no-benchmarks", action="store_true")
    parser.add_argument("--base-branch", default="main")
    parser.add_argument("--stop-after", choices=sorted(state.ALLOWED_TRANSITIONS))
    parser.add_argument("--max-verification-fixes", type=int, default=3)
    parser.add_argument("--max-review-fixes", type=int, default=3)
    parser.add_argument("--poll-interval-seconds", type=int, default=120)
    parser.add_argument("--review-timeout-seconds", type=int, default=1800)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo_root = Path(__file__).resolve().parent.parent
    runner = AutomationRunner(repo_root, args)
    try:
        runner.run()
    except Exception as exc:
        print(f"automation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
