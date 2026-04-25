from __future__ import annotations

from pathlib import Path
import re

from automation.shell import run_command
from automation.specs import AlgorithmSpec


NON_IDENTIFIER_RE = re.compile(r"[^A-Za-z0-9_]+")


def rust_module_name(binary_name: str) -> str:
    sanitized = NON_IDENTIFIER_RE.sub("_", binary_name)
    sanitized = sanitized.strip("_")
    if not sanitized:
        return "algorithm"
    if sanitized[0].isdigit():
        sanitized = f"algo_{sanitized}"
    return sanitized


def invoke_scaffold(repo_root: Path, spec: AlgorithmSpec) -> None:
    run_command(
        [
            "python3",
            "scripts/scaffold_topic.py",
            "--topic-path",
            spec.topic_path,
            "--display-name",
            spec.display_name,
            "--algo-id",
            spec.algo_id,
            "--binary-name",
            spec.binary_name,
            "--time-flag",
            spec.time_flag,
        ],
        cwd=repo_root,
    )


def validate_scaffold(repo_root: Path, spec: AlgorithmSpec) -> list[str]:
    topic_dir = repo_root / spec.topic_path
    expected = [
        "Makefile",
        "PROBLEM.md",
        "USAGE.md",
        "inputs/input.txt",
        "inputs/expected_output.txt",
        "inputs/input_large.txt",
        "inputs/input_challenge.txt",
        f"cpp/{spec.algo_id}.cpp",
        f"cpp/{spec.algo_id}.hpp",
        "cpp/main.cpp",
        f"python/{spec.algo_id}.py",
        "python/main.py",
        f"java/{spec.algo_id}.java",
        "java/Main.java",
        "rust/Cargo.toml",
        "rust/src/main.rs",
        f"rust/src/{rust_module_name(spec.binary_name)}.rs",
    ]
    missing = [path for path in expected if not (topic_dir / path).exists()]
    if missing:
        missing_joined = ", ".join(sorted(missing))
        raise RuntimeError(f"scaffold validation failed, missing files: {missing_joined}")
    return expected

