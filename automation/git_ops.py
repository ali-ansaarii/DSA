from __future__ import annotations

from pathlib import Path

from automation.shell import run_command


def current_branch(repo_root: Path) -> str:
    result = run_command(
        ["git", "branch", "--show-current"],
        cwd=repo_root,
    )
    return result.stdout.strip()


def current_commit(repo_root: Path) -> str:
    result = run_command(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
    )
    return result.stdout.strip()


def ensure_clean_base_branch(repo_root: Path, base_branch: str) -> None:
    branch = current_branch(repo_root)
    if branch != base_branch:
        raise RuntimeError(
            f"automation must start from {base_branch}, found branch: {branch}"
        )
    result = run_command(
        ["git", "status", "--porcelain"],
        cwd=repo_root,
    )
    if result.stdout.strip():
        raise RuntimeError("automation requires a clean working tree")


def create_branch(repo_root: Path, branch_name: str) -> None:
    run_command(
        ["git", "checkout", "-b", branch_name],
        cwd=repo_root,
    )


def checkout_branch(repo_root: Path, branch_name: str) -> None:
    run_command(
        ["git", "checkout", branch_name],
        cwd=repo_root,
    )


def checkout_base_branch(repo_root: Path, base_branch: str) -> None:
    checkout_branch(repo_root, base_branch)


def stage_paths(repo_root: Path, paths: list[str]) -> None:
    if not paths:
        raise ValueError("no paths to stage")
    run_command(
        ["git", "add", "--", *paths],
        cwd=repo_root,
    )


def commit(repo_root: Path, message: str) -> None:
    run_command(
        ["git", "commit", "-m", message],
        cwd=repo_root,
    )


def push_new_branch(repo_root: Path, branch_name: str) -> None:
    run_command(
        ["git", "push", "-u", "origin", branch_name],
        cwd=repo_root,
    )


def push_current_branch(repo_root: Path) -> None:
    run_command(
        ["git", "push"],
        cwd=repo_root,
    )


def pull_base_ff_only(repo_root: Path, base_branch: str) -> None:
    run_command(
        ["git", "pull", "--ff-only", "origin", base_branch],
        cwd=repo_root,
    )


def delete_local_branch(repo_root: Path, branch_name: str) -> None:
    run_command(
        ["git", "branch", "-D", branch_name],
        cwd=repo_root,
    )


def add_detached_worktree(repo_root: Path, worktree_path: Path, start_point: str) -> None:
    run_command(
        [
            "git",
            "worktree",
            "add",
            "--detach",
            str(worktree_path),
            start_point,
        ],
        cwd=repo_root,
    )


def remove_worktree(repo_root: Path, worktree_path: Path, *, force: bool = False) -> None:
    args = ["git", "worktree", "remove"]
    if force:
        args.append("--force")
    args.append(str(worktree_path))
    run_command(
        args,
        cwd=repo_root,
    )
