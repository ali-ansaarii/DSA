from __future__ import annotations

import re
from pathlib import Path


CHECKBOX_LINE_RE = re.compile(r"^(\s*-\s*\[)([ xX])(\]\s+)(.*?)(\s*)$")


def mark_algorithm_done(checklist_path: Path, label: str) -> int:
    if not checklist_path.exists():
        raise FileNotFoundError(f"checklist not found: {checklist_path}")

    lines = checklist_path.read_text(encoding="utf-8").splitlines()
    updated_count = 0
    new_lines: list[str] = []

    for line in lines:
        match = CHECKBOX_LINE_RE.match(line)
        if not match:
            new_lines.append(line)
            continue

        prefix, checked, middle, candidate_label, suffix = match.groups()
        if candidate_label == label and checked.strip().lower() != "x":
            new_lines.append(f"{prefix}x{middle}{candidate_label}{suffix}")
            updated_count += 1
        else:
            new_lines.append(line)

    if updated_count == 0:
        raise ValueError(f"checklist label not found or already complete: {label}")

    checklist_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return updated_count

