from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path


CHECKBOX_LINE_RE = re.compile(r"^(\s*-\s*\[)([ xX])(\]\s+)(.*?)(\s*)$")


@dataclass(frozen=True)
class ChecklistLabelStatus:
    label: str
    first_line_number: int
    checked_count: int = 0
    unchecked_count: int = 0

    @property
    def total_count(self) -> int:
        return self.checked_count + self.unchecked_count

    @property
    def is_complete(self) -> bool:
        return self.total_count > 0 and self.unchecked_count == 0

    @property
    def is_pending(self) -> bool:
        return self.unchecked_count > 0

    @property
    def is_inconsistent(self) -> bool:
        return self.checked_count > 0 and self.unchecked_count > 0


def load_label_statuses(checklist_path: Path) -> list[ChecklistLabelStatus]:
    if not checklist_path.exists():
        raise FileNotFoundError(f"checklist not found: {checklist_path}")

    ordered_labels: list[str] = []
    aggregate: dict[str, dict[str, int]] = {}

    for index, line in enumerate(
        checklist_path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        match = CHECKBOX_LINE_RE.match(line)
        if not match:
            continue

        _, checked, _, candidate_label, _ = match.groups()
        if candidate_label not in aggregate:
            aggregate[candidate_label] = {
                "first_line_number": index,
                "checked_count": 0,
                "unchecked_count": 0,
            }
            ordered_labels.append(candidate_label)

        if checked.strip().lower() == "x":
            aggregate[candidate_label]["checked_count"] += 1
        else:
            aggregate[candidate_label]["unchecked_count"] += 1

    statuses: list[ChecklistLabelStatus] = []
    for label in ordered_labels:
        raw = aggregate[label]
        statuses.append(
            ChecklistLabelStatus(
                label=label,
                first_line_number=raw["first_line_number"],
                checked_count=raw["checked_count"],
                unchecked_count=raw["unchecked_count"],
            )
        )
    return statuses


def list_pending_labels(checklist_path: Path) -> list[str]:
    return [status.label for status in load_label_statuses(checklist_path) if status.is_pending]


def find_inconsistent_labels(checklist_path: Path) -> list[str]:
    return [
        status.label
        for status in load_label_statuses(checklist_path)
        if status.is_inconsistent
    ]


def mark_algorithm_done(checklist_path: Path, label: str) -> int:
    return mark_algorithm_labels_done(checklist_path, [label])


def mark_algorithm_labels_done(checklist_path: Path, labels: list[str]) -> int:
    if not checklist_path.exists():
        raise FileNotFoundError(f"checklist not found: {checklist_path}")
    wanted = set(labels)
    if not wanted:
        raise ValueError("no checklist labels provided")

    lines = checklist_path.read_text(encoding="utf-8").splitlines()
    updated_count = 0
    new_lines: list[str] = []

    for line in lines:
        match = CHECKBOX_LINE_RE.match(line)
        if not match:
            new_lines.append(line)
            continue

        prefix, checked, middle, candidate_label, suffix = match.groups()
        if candidate_label in wanted and checked.strip().lower() != "x":
            new_lines.append(f"{prefix}x{middle}{candidate_label}{suffix}")
            updated_count += 1
        else:
            new_lines.append(line)

    if updated_count == 0:
        raise ValueError(
            "checklist labels not found or already complete: " + ", ".join(sorted(wanted))
        )

    checklist_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return updated_count
