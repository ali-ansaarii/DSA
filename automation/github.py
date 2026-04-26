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
GENERIC_REVIEW_WRAPPER_RE = re.compile(
    r"here are some automated review suggestions for this pull request",
    re.IGNORECASE,
)
CLEAN_REVIEW_PATTERNS = [
    re.compile(r"^(?:codex review:\s*)?didn['’]?t find any major issues(?:[.!]\s*.*)?$", re.IGNORECASE),
    re.compile(r"^(?:codex review:\s*)?no major issues found(?:[.!]\s*.*)?$", re.IGNORECASE),
    re.compile(r"^(?:codex review:\s*)?no issues found(?:[.!]\s*.*)?$", re.IGNORECASE),
    re.compile(r"^(?:codex review:\s*)?no major concerns(?:[.!]\s*.*)?$", re.IGNORECASE),
    re.compile(r"^(?:codex review:\s*)?nothing major to flag(?: here)?(?:[.!]\s*.*)?$", re.IGNORECASE),
    re.compile(r"^(?:codex review:\s*)?looks good(?: to me)?(?:[.!]\s*.*)?$", re.IGNORECASE),
    re.compile(r"^(?:codex review:\s*)?lgtm(?:[.!]\s*.*)?$", re.IGNORECASE),
]
EYES_REACTION = "eyes"
THUMBS_UP_REACTION = "+1"


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
    latest_bot_review_state: str | None = None
    latest_bot_review_body: str | None = None


@dataclass(frozen=True)
class ReviewRequestComment:
    comment_id: int
    created_at: str | None


@dataclass(frozen=True)
class ReviewRequestReceipt:
    state: str
    seen_at: str | None = None


def _bot_comment_is_clean(body: str | None) -> bool:
    if not body:
        return False
    if GENERIC_REVIEW_WRAPPER_RE.search(body):
        return False
    first_paragraph = body.split("\n\n", 1)[0].strip()
    return any(pattern.match(first_paragraph) for pattern in CLEAN_REVIEW_PATTERNS)


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


def _api_request_json(
    repo_root: Path,
    *,
    method: str,
    path: str,
    payload: dict | None = None,
) -> dict:
    token = get_review_token(repo_root)
    owner, repo = parse_remote_owner_repo(repo_root)
    full_path = path.format(owner=owner, repo=repo)
    if token:
        req = request.Request(
            f"https://api.github.com{full_path}",
            data=(json.dumps(payload).encode("utf-8") if payload is not None else None),
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "dsa-automation-github",
                "Content-Type": "application/json",
            },
            method=method,
        )
        with request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

    command = ["gh", "api", full_path, "--method", method]
    if payload is not None:
        for key, value in payload.items():
            command.extend(["-f", f"{key}={value}"])
    result = run_command(command, cwd=repo_root)
    return json.loads(result.stdout)


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


def request_codex_review(repo_root: Path, pr_number: int) -> ReviewRequestComment:
    payload = _api_request_json(
        repo_root,
        method="POST",
        path="/repos/{owner}/{repo}/issues/" + str(pr_number) + "/comments",
        payload={"body": "@codex review"},
    )
    return ReviewRequestComment(
        comment_id=int(payload["id"]),
        created_at=payload.get("created_at"),
    )


def fetch_review_request_receipt(
    repo_root: Path,
    *,
    comment_id: int,
) -> ReviewRequestReceipt:
    payload = _api_request_json(
        repo_root,
        method="GET",
        path="/repos/{owner}/{repo}/issues/comments/" + str(comment_id) + "/reactions",
    )
    reactions = payload if isinstance(payload, list) else []
    latest_seen_at: str | None = None
    saw_eyes = False
    saw_thumbs_up = False
    for reaction in reactions:
        author = (reaction.get("user") or {}).get("login")
        if author not in BOT_LOGINS:
            continue
        content = reaction.get("content")
        created_at = reaction.get("created_at")
        if created_at and (latest_seen_at is None or created_at > latest_seen_at):
            latest_seen_at = created_at
        if content == EYES_REACTION:
            saw_eyes = True
        elif content == THUMBS_UP_REACTION:
            saw_thumbs_up = True
    if saw_thumbs_up:
        return ReviewRequestReceipt(state="clean", seen_at=latest_seen_at)
    if saw_eyes:
        return ReviewRequestReceipt(state="acknowledged", seen_at=latest_seen_at)
    return ReviewRequestReceipt(state="waiting", seen_at=None)


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
            latest_bot_review_state=latest_bot_review.get("state") if latest_bot_review else None,
            latest_bot_review_body=latest_bot_review.get("body") if latest_bot_review else None,
        )

    if _bot_comment_is_clean(latest_bot_comment):
        return ReviewStatus(
            state="clean",
            actionable_comments=[],
            latest_bot_comment=latest_bot_comment,
            latest_bot_review_state=latest_bot_review.get("state") if latest_bot_review else None,
            latest_bot_review_body=latest_bot_review.get("body") if latest_bot_review else None,
        )

    if latest_bot_review and latest_bot_review.get("state") == "APPROVED":
        return ReviewStatus(
            state="clean",
            actionable_comments=[],
            latest_bot_comment=latest_bot_comment or latest_bot_review.get("body"),
            latest_bot_review_state=latest_bot_review.get("state"),
            latest_bot_review_body=latest_bot_review.get("body"),
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
            latest_bot_review_state=latest_bot_review.get("state"),
            latest_bot_review_body=latest_bot_review.get("body"),
        )

    return ReviewStatus(
        state="waiting",
        actionable_comments=[],
        latest_bot_comment=latest_bot_comment,
        latest_bot_review_state=latest_bot_review.get("state") if latest_bot_review else None,
        latest_bot_review_body=latest_bot_review.get("body") if latest_bot_review else None,
    )
