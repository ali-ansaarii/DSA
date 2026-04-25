from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import shutil
from pathlib import Path
import sys
from typing import Iterable

sys.dont_write_bytecode = True

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from automation import checklist, git_ops, specs, state
from automation import model as model_env
from automation.shell import CommandError, run_command


@dataclass(frozen=True)
class QueuePlanEntry:
    label: str
    status: str
    reason: str
    run_id: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return asdict(self)


def build_queue_plan(
    pending_labels: Iterable[str],
    *,
    available_run_ids: dict[str, str],
    existing_run_states: dict[str, str],
    existing_local_branches: set[str],
    existing_remote_branches: set[str],
    limit: int | None = None,
) -> list[QueuePlanEntry]:
    plan: list[QueuePlanEntry] = []
    runnable_count = 0
    first_label_by_run_id: dict[str, str] = {}

    for label in pending_labels:
        run_id = available_run_ids.get(label)
        if run_id is None:
            plan.append(
                QueuePlanEntry(
                    label=label,
                    status="missing_catalog",
                    reason="no catalog entry available for this checklist label",
                )
            )
            continue

        if run_id in first_label_by_run_id:
            plan.append(
                QueuePlanEntry(
                    label=label,
                    run_id=run_id,
                    status="covered_by_alias",
                    reason=(
                        f"same algorithm already represented by earlier checklist label "
                        f"{first_label_by_run_id[run_id]}"
                    ),
                )
            )
            continue
        first_label_by_run_id[run_id] = label

        existing_state = existing_run_states.get(run_id)
        if existing_state is not None:
            if existing_state == state.STATE_DONE:
                plan.append(
                    QueuePlanEntry(
                        label=label,
                        run_id=run_id,
                        status="stale_checklist",
                        reason="run state is done but checklist is still pending",
                    )
                )
            elif existing_state in state.TERMINAL_STATES:
                plan.append(
                    QueuePlanEntry(
                        label=label,
                        run_id=run_id,
                        status="blocked_existing_run",
                        reason=f"existing run state is {existing_state}",
                    )
                )
            else:
                plan.append(
                    QueuePlanEntry(
                        label=label,
                        run_id=run_id,
                        status="active_existing_run",
                        reason=f"existing run is still active in state {existing_state}",
                    )
                )
            continue

        if run_id in existing_local_branches:
            plan.append(
                QueuePlanEntry(
                    label=label,
                    run_id=run_id,
                    status="blocked_local_branch",
                    reason=f"local branch {run_id} already exists without a matching active run state",
                )
            )
            continue

        if run_id in existing_remote_branches:
            plan.append(
                QueuePlanEntry(
                    label=label,
                    run_id=run_id,
                    status="blocked_remote_branch",
                    reason=f"remote branch {run_id} already exists on origin without a matching active run state",
                )
            )
            continue

        if limit is not None and runnable_count >= limit:
            plan.append(
                QueuePlanEntry(
                    label=label,
                    run_id=run_id,
                    status="deferred_by_limit",
                    reason=f"queue limit {limit} reached before this item",
                )
            )
            continue

        plan.append(
            QueuePlanEntry(
                label=label,
                run_id=run_id,
                status="runnable",
                reason="catalog entry and clean run slot available",
            )
        )
        runnable_count += 1

    return plan


class QueueRunner:
    def __init__(self, repo_root: Path, args: argparse.Namespace) -> None:
        self.repo_root = repo_root
        self.args = args
        self.local_root = Path(self.args.local_root).resolve()
        self.checklist_path = self.local_root / "ALGORITHM_CHECKLIST.md"
        self.catalog_path = (self.repo_root / self.args.catalog).resolve()
        model_env.load_env_defaults(self.repo_root / ".env")
        self.catalog_specs = specs.load_catalog_specs(self.catalog_path)
        self.catalog_specs_by_label = specs.load_catalog_specs_by_label(self.catalog_path)
        self.queue_root = self.local_root / "automation_queue_runs"
        self.worktree_root = self.local_root / "automation_worktrees"
        self.summary_dir = self.queue_root / _utc_stamp()
        self.summary_path = self.summary_dir / "summary.json"

    def run(self) -> int:
        git_ops.ensure_clean_base_branch(
            self.repo_root,
            self.args.base_branch,
            allowed_dirty_roots=[self.local_root],
        )
        inconsistent = checklist.find_inconsistent_labels(self.checklist_path)
        if inconsistent:
            raise RuntimeError(
                "checklist has inconsistent labels that are both checked and unchecked: "
                + ", ".join(inconsistent)
            )

        pending_labels = checklist.list_pending_labels(self.checklist_path)
        available_run_ids = {
            label: spec.run_id
            for label, spec in self.catalog_specs_by_label.items()
        }
        existing_run_states = self._load_existing_run_states()
        existing_local_branches = git_ops.list_local_branches(self.repo_root)
        existing_remote_branches = git_ops.list_remote_branches(self.repo_root)
        plan = build_queue_plan(
            pending_labels,
            available_run_ids=available_run_ids,
            existing_run_states=existing_run_states,
            existing_local_branches=existing_local_branches,
            existing_remote_branches=existing_remote_branches,
            limit=self.args.limit,
        )
        summary = {
            "started_at": datetime.now(tz=timezone.utc).isoformat(timespec="seconds"),
            "base_branch": self.args.base_branch,
            "catalog": str(self.catalog_path),
            "local_root": str(self.local_root),
            "pending_labels": pending_labels,
            "plan": [entry.to_dict() for entry in plan],
            "results": [],
        }
        self._write_summary(summary)

        if self.args.dry_run:
            summary["completed_at"] = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
            self._write_summary(summary)
            return 0

        for entry in plan:
            if entry.status != "runnable":
                continue
            spec = self.catalog_specs_by_label[entry.label]
            result = self._run_single_algorithm(spec)
            summary["results"].append(result)
            self._write_summary(summary)

        summary["completed_at"] = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
        self._write_summary(summary)
        return 0

    def _load_existing_run_states(self) -> dict[str, str]:
        run_root = self.local_root / "automation_runs"
        states_by_run_id: dict[str, str] = {}
        for spec in self.catalog_specs.values():
            state_path = run_root / spec.run_id / "state.json"
            if not state_path.exists():
                continue
            raw = json.loads(state_path.read_text(encoding="utf-8"))
            current_state = raw.get("current_state")
            if isinstance(current_state, str):
                states_by_run_id[spec.run_id] = current_state
        return states_by_run_id

    def _run_single_algorithm(self, spec: specs.AlgorithmSpec) -> dict[str, object]:
        self.worktree_root.mkdir(parents=True, exist_ok=True)
        worktree_path = self.worktree_root / f"{spec.run_id}-{_utc_stamp()}"
        result_payload: dict[str, object] = {
            "algorithm": spec.algorithm_name,
            "branch": spec.branch_name,
            "worktree": str(worktree_path),
            "started_at": datetime.now(tz=timezone.utc).isoformat(timespec="seconds"),
        }
        git_ops.pull_base_ff_only(self.repo_root, self.args.base_branch)
        git_ops.add_detached_worktree(self.repo_root, worktree_path, self.args.base_branch)
        try:
            command = [
                "python3",
                "automation/run_factory.py",
                "--algorithm",
                spec.algorithm_name,
                "--catalog",
                self.args.catalog,
                "--base-branch",
                self.args.base_branch,
                "--ephemeral-worktree",
                "--local-root",
                str(self.local_root),
                "--max-verification-fixes",
                str(self.args.max_verification_fixes),
                "--max-review-fixes",
                str(self.args.max_review_fixes),
                "--poll-interval-seconds",
                str(self.args.poll_interval_seconds),
                "--review-timeout-seconds",
                str(self.args.review_timeout_seconds),
            ]
            if self.args.stop_after:
                command.extend(["--stop-after", self.args.stop_after])
            child = run_command(command, cwd=worktree_path, check=False)
            result_payload["runner_returncode"] = child.returncode
            result_payload["stdout"] = child.stdout.strip()
            result_payload["stderr"] = child.stderr.strip()
            current_state = self._load_run_state(spec.run_id)
            result_payload["final_state"] = current_state
            result_payload["outcome"] = (
                "success" if current_state == state.STATE_DONE else current_state
            )
        finally:
            try:
                git_ops.remove_worktree(self.repo_root, worktree_path, force=True)
            except CommandError as exc:
                result_payload["worktree_remove_error"] = str(exc)
            shutil.rmtree(worktree_path, ignore_errors=True)
            final_state = result_payload.get("final_state")
            if final_state == state.STATE_DONE:
                branch_name = spec.branch_name
                try:
                    git_ops.delete_local_branch(self.repo_root, branch_name)
                except CommandError as exc:
                    result_payload["local_branch_cleanup_error"] = str(exc)
                try:
                    git_ops.delete_remote_branch(self.repo_root, branch_name)
                except CommandError as exc:
                    result_payload["remote_branch_cleanup_error"] = str(exc)

        result_payload["completed_at"] = datetime.now(tz=timezone.utc).isoformat(timespec="seconds")
        return result_payload

    def _load_run_state(self, run_id: str) -> str:
        state_path = self.local_root / "automation_runs" / run_id / "state.json"
        if not state_path.exists():
            raise RuntimeError(f"run state file not found after child run: {state_path}")
        raw = json.loads(state_path.read_text(encoding="utf-8"))
        current_state = raw.get("current_state")
        if not isinstance(current_state, str):
            raise RuntimeError(f"run state file missing current_state: {state_path}")
        return current_state

    def _write_summary(self, payload: dict[str, object]) -> None:
        self.summary_dir.mkdir(parents=True, exist_ok=True)
        self.summary_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def _utc_stamp() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Sequential checklist queue automation")
    parser.add_argument(
        "--catalog",
        default="automation/algorithm_catalog.json",
        help="JSON catalog mapping checklist labels to runnable algorithm specs",
    )
    parser.add_argument("--base-branch", default="main")
    parser.add_argument(
        "--local-root",
        default=".local",
        help="Shared local-state root for checklist and automation manifests",
    )
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
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
    runner = QueueRunner(repo_root, args)
    try:
        return runner.run()
    except Exception as exc:
        print(f"queue automation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
