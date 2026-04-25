from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
import os
from pathlib import Path
import re
from urllib import request

from automation.shell import run_command


BOT_LOGINS = {"chatgpt-codex-connector[bot]", "chatgpt-codex-connector"}
CLEAN_REVIEW_RE = re.compile(r"didn['’]?t find any major issues", re.IGNORECASE)


@dataclass(frozen=True)
class ReviewComment:
    path: str | None
    line: int | None
    body: str
    url: str | None
    author: str
    created_at: str | None


@dataclass(frozen=True)
class ReviewStatus:
    state: str
    actionable_comments: list[ReviewComment]
    latest_bot_comment: str | None


def _parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def _is_after_threshold(value: str | None, threshold: str | None) -> bool:
    if threshold is None:
        return True
    observed = _parse_timestamp(value)
    boundary = _parse_timestamp(threshold)
    if observed is None or boundary is None:
        return False
    return observed >= boundary


def _load_env_defaults(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        separator = None
        if "=" in line:
            separator = "="
        elif ":" in line:
            separator = ":"
        if separator is None:
            continue
        key, value = line.split(separator, 1)
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value.strip().strip("\"'")


def get_review_token(repo_root: Path) -> str | None:
    _load_env_defaults(repo_root / ".env")
    return os.environ.get("GITHUB_REVIEW_TOKEN") or os.environ.get("GH_TOKEN")


def parse_remote_owner_repo(repo_root: Path) -> tuple[str, str]:
    result = run_command(
        ["git", "remote", "get-url", "origin"],
        cwd=repo_root,
    )
    remote = result.stdout.strip()
    ssh_match = re.match(r"git@github\.com:(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$", remote)
    https_match = re.match(
        r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$",
        remote,
    )
    match = ssh_match or https_match
    if not match:
        raise RuntimeError(f"could not parse GitHub remote: {remote}")
    return match.group("owner"), match.group("repo")


def create_pr(
    repo_root: Path,
    *,
    title: str,
    body: str,
    base: str,
    head: str,
) -> tuple[int, str]:
    result = run_command(
        [
            "gh",
            "pr",
            "create",
            "--base",
            base,
            "--head",
            head,
            "--title",
            title,
            "--body",
            body,
        ],
        cwd=repo_root,
    )
    pr_reference = result.stdout.strip().splitlines()[-1].strip()
    details = run_command(
        ["gh", "pr", "view", pr_reference, "--json", "number,url"],
        cwd=repo_root,
    )
    payload = json.loads(details.stdout)
    return int(payload["number"]), payload["url"]


def request_codex_review(repo_root: Path, pr_number: int) -> None:
    token = get_review_token(repo_root)
    if token:
        owner, repo = parse_remote_owner_repo(repo_root)
        payload = json.dumps({"body": "@codex review"}).encode("utf-8")
        req = request.Request(
            f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments",
            data=payload,
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "dsa-automation-review-request",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with request.urlopen(req, timeout=20) as response:
            if response.status != 201:
                raise RuntimeError(
                    f"unexpected GitHub comment response status: {response.status}"
                )
        return

    run_command(
        ["gh", "pr", "comment", str(pr_number), "--body", "@codex review"],
        cwd=repo_root,
    )


def merge_pr(repo_root: Path, pr_number: int, *, delete_branch: bool = True) -> None:
    command = ["gh", "pr", "merge", str(pr_number), "--squash"]
    if delete_branch:
        command.append("--delete-branch")
    run_command(command, cwd=repo_root)


def fetch_review_status(
    repo_root: Path,
    pr_number: int,
    *,
    not_before: str | None = None,
) -> ReviewStatus:
    owner, repo = parse_remote_owner_repo(repo_root)
    query = """
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 100) {
        nodes {
          isResolved
          comments(first: 20) {
            nodes {
              author { login }
              body
              path
              line
              url
              createdAt
            }
          }
        }
      }
      comments(last: 20) {
        nodes {
          author { login }
          body
          createdAt
          url
        }
      }
      reviews(last: 20) {
        nodes {
          author { login }
          body
          submittedAt
          state
        }
      }
    }
  }
}
""".strip()
    result = run_command(
        [
            "gh",
            "api",
            "graphql",
            "-f",
            f"query={query}",
            "-F",
            f"owner={owner}",
            "-F",
            f"repo={repo}",
            "-F",
            f"number={pr_number}",
        ],
        cwd=repo_root,
    )
    payload = json.loads(result.stdout)
    return parse_review_payload(payload, not_before=not_before)


def parse_review_payload(payload: dict, *, not_before: str | None = None) -> ReviewStatus:
    pull_request = payload["data"]["repository"]["pullRequest"]
    threads = pull_request["reviewThreads"]["nodes"]
    issue_comments = pull_request["comments"]["nodes"]
    reviews = pull_request["reviews"]["nodes"]

    actionable: list[ReviewComment] = []
    for thread in threads:
        if thread.get("isResolved"):
            continue
        comments = thread["comments"]["nodes"]
        bot_comments = [
            comment
            for comment in comments
            if (
                (comment.get("author") or {}).get("login") in BOT_LOGINS
                and _is_after_threshold(comment.get("createdAt"), not_before)
            )
        ]
        if not bot_comments:
            continue
        latest = bot_comments[-1]
        actionable.append(
            ReviewComment(
                path=latest.get("path"),
                line=latest.get("line"),
                body=latest["body"],
                url=latest.get("url"),
                author=(latest.get("author") or {}).get("login", ""),
                created_at=latest.get("createdAt"),
            )
        )

    bot_issue_comments = [
        comment
        for comment in issue_comments
        if (
            (comment.get("author") or {}).get("login") in BOT_LOGINS
            and _is_after_threshold(comment.get("createdAt"), not_before)
        )
    ]
    latest_bot_comment = bot_issue_comments[-1]["body"] if bot_issue_comments else None
    recent_bot_reviews = [
        review
        for review in reviews
        if (
            (review.get("author") or {}).get("login") in BOT_LOGINS
            and _is_after_threshold(review.get("submittedAt"), not_before)
        )
    ]
    latest_bot_review = recent_bot_reviews[-1] if recent_bot_reviews else None

    if actionable:
        return ReviewStatus(
            state="actionable",
            actionable_comments=actionable,
            latest_bot_comment=latest_bot_comment,
        )

    if latest_bot_comment and CLEAN_REVIEW_RE.search(latest_bot_comment):
        return ReviewStatus(
            state="clean",
            actionable_comments=[],
            latest_bot_comment=latest_bot_comment,
        )

    if latest_bot_review and latest_bot_review.get("state") == "APPROVED":
        return ReviewStatus(
            state="clean",
            actionable_comments=[],
            latest_bot_comment=latest_bot_comment or latest_bot_review.get("body"),
        )

    if latest_bot_review:
        return ReviewStatus(
            state="actionable",
            actionable_comments=[
                ReviewComment(
                    path=None,
                    line=None,
                    body=latest_bot_review.get("body") or "non-clean bot review",
                    url=None,
                    author=(latest_bot_review.get("author") or {}).get("login", ""),
                    created_at=latest_bot_review.get("submittedAt"),
                )
            ],
            latest_bot_comment=latest_bot_comment or latest_bot_review.get("body"),
        )

    return ReviewStatus(
        state="waiting",
        actionable_comments=[],
        latest_bot_comment=latest_bot_comment,
    )
