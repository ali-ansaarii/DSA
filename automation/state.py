from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


STATE_QUEUED = "queued"
STATE_BRANCH_CREATED = "branch_created"
STATE_SCAFFOLDED = "scaffolded"
STATE_GENERATED = "generated"
STATE_VERIFIED = "verified"
STATE_COMMITTED = "committed"
STATE_PUSHED = "pushed"
STATE_PR_OPEN = "pr_open"
STATE_REVIEW_REQUESTED = "review_requested"
STATE_REVIEW_WAITING = "review_waiting"
STATE_REVIEW_FIXING = "review_fixing"
STATE_REVIEW_CLEAN = "review_clean"
STATE_MERGED = "merged"
STATE_CHECKLIST_UPDATED = "checklist_updated"
STATE_DONE = "done"
STATE_FAILED = "failed"
STATE_MANUAL_ATTENTION = "manual_attention"

TERMINAL_STATES = {
    STATE_DONE,
    STATE_FAILED,
    STATE_MANUAL_ATTENTION,
}

ALLOWED_TRANSITIONS = {
    STATE_QUEUED: {
        STATE_BRANCH_CREATED,
        STATE_FAILED,
        STATE_MANUAL_ATTENTION,
    },
    STATE_BRANCH_CREATED: {
        STATE_SCAFFOLDED,
        STATE_FAILED,
        STATE_MANUAL_ATTENTION,
    },
    STATE_SCAFFOLDED: {
        STATE_GENERATED,
        STATE_FAILED,
        STATE_MANUAL_ATTENTION,
    },
    STATE_GENERATED: {
        STATE_GENERATED,
        STATE_VERIFIED,
        STATE_FAILED,
        STATE_MANUAL_ATTENTION,
    },
    STATE_VERIFIED: {
        STATE_COMMITTED,
        STATE_FAILED,
        STATE_MANUAL_ATTENTION,
    },
    STATE_COMMITTED: {
        STATE_PUSHED,
        STATE_FAILED,
        STATE_MANUAL_ATTENTION,
    },
    STATE_PUSHED: {
        STATE_PR_OPEN,
        STATE_REVIEW_REQUESTED,
        STATE_FAILED,
        STATE_MANUAL_ATTENTION,
    },
    STATE_PR_OPEN: {
        STATE_REVIEW_REQUESTED,
        STATE_FAILED,
        STATE_MANUAL_ATTENTION,
    },
    STATE_REVIEW_REQUESTED: {
        STATE_REVIEW_WAITING,
        STATE_FAILED,
        STATE_MANUAL_ATTENTION,
    },
    STATE_REVIEW_WAITING: {
        STATE_REVIEW_REQUESTED,
        STATE_REVIEW_WAITING,
        STATE_REVIEW_FIXING,
        STATE_REVIEW_CLEAN,
        STATE_FAILED,
        STATE_MANUAL_ATTENTION,
    },
    STATE_REVIEW_FIXING: {
        STATE_GENERATED,
        STATE_FAILED,
        STATE_MANUAL_ATTENTION,
    },
    STATE_REVIEW_CLEAN: {
        STATE_MERGED,
        STATE_FAILED,
        STATE_MANUAL_ATTENTION,
    },
    STATE_MERGED: {
        STATE_CHECKLIST_UPDATED,
        STATE_MANUAL_ATTENTION,
        STATE_FAILED,
    },
    STATE_CHECKLIST_UPDATED: {
        STATE_DONE,
        STATE_MANUAL_ATTENTION,
        STATE_FAILED,
    },
    STATE_DONE: set(),
    STATE_FAILED: set(),
    STATE_MANUAL_ATTENTION: set(),
}


def utc_now() -> str:
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


@dataclass
class RunPaths:
    run_dir: Path
    state_path: Path
    progress_path: Path
    generation_log_path: Path
    verification_log_path: Path
    review_log_path: Path
    review_comments_path: Path
    summary_path: Path

    @classmethod
    def create(cls, root: Path, run_id: str) -> "RunPaths":
        run_dir = root / run_id
        return cls(
            run_dir=run_dir,
            state_path=run_dir / "state.json",
            progress_path=run_dir / "progress.json",
            generation_log_path=run_dir / "generation.log",
            verification_log_path=run_dir / "verification.log",
            review_log_path=run_dir / "review.log",
            review_comments_path=run_dir / "review_comments.json",
            summary_path=run_dir / "summary.txt",
        )


@dataclass
class RunSnapshot:
    run_id: str
    algorithm_name: str
    checklist_label: str
    branch_name: str
    topic_path: str
    display_name: str
    pr_title: str
    current_state: str = STATE_QUEUED
    pr_number: int | None = None
    pr_url: str | None = None
    latest_commit: str | None = None
    generation_attempts: int = 0
    verification_fix_attempts: int = 0
    review_request_attempts: int = 0
    review_request_pickup_retries: int = 0
    review_fix_attempts: int = 0
    review_request_comment_id: int | None = None
    review_request_comment_created_at: str | None = None
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "RunSnapshot":
        return cls(**raw)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProgressEntry:
    step_name: str
    state_before: str
    state_after: str
    start_timestamp: str
    end_timestamp: str
    outcome: str
    evidence: dict[str, Any]
    note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class RunStore:
    def __init__(self, paths: RunPaths) -> None:
        self.paths = paths

    def _ensure_parent_dir(self) -> None:
        self.paths.run_dir.mkdir(parents=True, exist_ok=True)

    def initialize(self, snapshot: RunSnapshot) -> None:
        self._ensure_parent_dir()
        self.save_snapshot(snapshot)
        if not self.paths.progress_path.exists():
            self.paths.progress_path.write_text("[]\n", encoding="utf-8")

    def load_snapshot(self) -> RunSnapshot:
        raw = json.loads(self.paths.state_path.read_text(encoding="utf-8"))
        return RunSnapshot.from_dict(raw)

    def save_snapshot(self, snapshot: RunSnapshot) -> None:
        self._ensure_parent_dir()
        snapshot.updated_at = utc_now()
        self.paths.state_path.write_text(
            json.dumps(snapshot.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def load_progress(self) -> list[dict[str, Any]]:
        if not self.paths.progress_path.exists():
            return []
        return json.loads(self.paths.progress_path.read_text(encoding="utf-8"))

    def append_progress(self, entry: ProgressEntry) -> None:
        self._ensure_parent_dir()
        progress = self.load_progress()
        progress.append(entry.to_dict())
        self.paths.progress_path.write_text(
            json.dumps(progress, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def transition(
        self,
        snapshot: RunSnapshot,
        *,
        step_name: str,
        next_state: str,
        outcome: str = "success",
        note: str = "",
        evidence: dict[str, Any] | None = None,
    ) -> RunSnapshot:
        validate_transition(snapshot.current_state, next_state)
        started_at = utc_now()
        previous_state = snapshot.current_state
        snapshot.current_state = next_state
        self.save_snapshot(snapshot)
        self.append_progress(
            ProgressEntry(
                step_name=step_name,
                state_before=previous_state,
                state_after=next_state,
                start_timestamp=started_at,
                end_timestamp=utc_now(),
                outcome=outcome,
                evidence=evidence or {},
                note=note,
            )
        )
        return snapshot

    def append_summary(self, line: str) -> None:
        self._ensure_parent_dir()
        with self.paths.summary_path.open("a", encoding="utf-8") as handle:
            handle.write(line.rstrip() + "\n")

    def save_review_comments(self, comments: list[dict[str, Any]]) -> None:
        self._ensure_parent_dir()
        self.paths.review_comments_path.write_text(
            json.dumps(comments, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def load_review_comments(self) -> list[dict[str, Any]]:
        if not self.paths.review_comments_path.exists():
            return []
        return json.loads(self.paths.review_comments_path.read_text(encoding="utf-8"))

    def clear_review_comments(self) -> None:
        if self.paths.review_comments_path.exists():
            self.paths.review_comments_path.unlink()


def validate_transition(current_state: str, next_state: str) -> None:
    allowed = ALLOWED_TRANSITIONS.get(current_state)
    if allowed is None:
        raise ValueError(f"unknown current state: {current_state}")
    if next_state not in allowed:
        raise ValueError(f"invalid transition: {current_state} -> {next_state}")
