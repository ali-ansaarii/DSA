from __future__ import annotations

from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Any


BRANCH_SANITIZE_RE = re.compile(r"[^a-z0-9]+")


def slugify_branch_name(value: str) -> str:
    lowered = value.strip().lower()
    lowered = BRANCH_SANITIZE_RE.sub("-", lowered)
    lowered = lowered.strip("-")
    if not lowered:
        raise ValueError("could not derive a valid branch name")
    return lowered


@dataclass(frozen=True)
class AlgorithmSpec:
    algorithm_name: str
    checklist_label: str
    topic_path: str
    display_name: str
    algo_id: str
    binary_name: str
    time_flag: str
    branch_name: str
    pr_title: str
    prompt_notes: str = ""
    benchmark_expected: bool = True

    @property
    def topic_dir_name(self) -> str:
        return Path(self.topic_path).name

    @property
    def run_id(self) -> str:
        return self.branch_name

    @classmethod
    def from_mapping(
        cls,
        *,
        algorithm_name: str,
        mapping: dict[str, Any],
        fallback_algorithm_name: str | None = None,
    ) -> "AlgorithmSpec":
        chosen_name = mapping.get("algorithm_name") or fallback_algorithm_name or algorithm_name
        display_name = mapping["display_name"]
        checklist_label = mapping.get("checklist_label", chosen_name)
        branch_name = mapping.get("branch_name") or slugify_branch_name(chosen_name)
        pr_title = mapping.get("pr_title") or f"Add {display_name}"
        return cls(
            algorithm_name=chosen_name,
            checklist_label=checklist_label,
            topic_path=mapping["topic_path"],
            display_name=display_name,
            algo_id=mapping["algo_id"],
            binary_name=mapping["binary_name"],
            time_flag=mapping["time_flag"],
            branch_name=branch_name,
            pr_title=pr_title,
            prompt_notes=mapping.get("prompt_notes", ""),
            benchmark_expected=bool(mapping.get("benchmark_expected", True)),
        )


def load_spec_from_catalog(catalog_path: Path, algorithm_name: str) -> AlgorithmSpec | None:
    if not catalog_path.exists():
        return None
    raw = json.loads(catalog_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"catalog must be a JSON object: {catalog_path}")
    entry = raw.get(algorithm_name)
    if entry is None:
        return None
    if not isinstance(entry, dict):
        raise ValueError(f"catalog entry must be a JSON object: {algorithm_name}")
    return AlgorithmSpec.from_mapping(
        algorithm_name=algorithm_name,
        mapping=entry,
        fallback_algorithm_name=algorithm_name,
    )


def build_spec_from_args(args: Any) -> AlgorithmSpec:
    required_fields = ["topic_path", "display_name", "algo_id", "binary_name", "time_flag"]
    missing = [field for field in required_fields if not getattr(args, field)]
    if missing:
        missing_joined = ", ".join(sorted(missing))
        raise ValueError(
            "algorithm spec not found in catalog and missing explicit arguments: "
            f"{missing_joined}"
        )

    mapping = {
        "topic_path": args.topic_path,
        "display_name": args.display_name,
        "algo_id": args.algo_id,
        "binary_name": args.binary_name,
        "time_flag": args.time_flag,
        "prompt_notes": args.prompt_notes or "",
        "benchmark_expected": not bool(args.no_benchmarks),
    }
    if args.branch_name:
        mapping["branch_name"] = args.branch_name
    if args.pr_title:
        mapping["pr_title"] = args.pr_title
    if args.checklist_label:
        mapping["checklist_label"] = args.checklist_label
    return AlgorithmSpec.from_mapping(
        algorithm_name=args.algorithm,
        mapping=mapping,
        fallback_algorithm_name=args.algorithm,
    )

