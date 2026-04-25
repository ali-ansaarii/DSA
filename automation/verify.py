from __future__ import annotations

from pathlib import Path

from automation.shell import run_command


def run_verification(
    repo_root: Path,
    topic_path: str,
    *,
    benchmarks: bool,
) -> tuple[str, str]:
    args = ["sh", "scripts/verify_topic.sh", topic_path]
    if benchmarks:
        args.append("--benchmarks")
    result = run_command(
        args,
        cwd=repo_root,
    )
    return result.stdout, result.stderr

