from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
from string import Template
from typing import Any
from urllib import error, request

from automation.specs import AlgorithmSpec


@dataclass(frozen=True)
class FileWrite:
    path: str
    content: str


@dataclass(frozen=True)
class FileBundle:
    summary: str
    files: list[FileWrite]


@dataclass(frozen=True)
class ModelCallResult:
    prompt: str
    raw_response: dict[str, Any]
    bundle: FileBundle


def load_env_defaults(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value.strip().strip("\"'")


def collect_topic_files(topic_dir: Path) -> list[tuple[str, str]]:
    files: list[tuple[str, str]] = []
    for path in sorted(topic_dir.rglob("*")):
        if path.is_dir():
            continue
        relative = path.relative_to(topic_dir).as_posix()
        files.append((relative, path.read_text(encoding="utf-8")))
    return files


def render_prompt(template_path: Path, variables: dict[str, str]) -> str:
    template = Template(template_path.read_text(encoding="utf-8"))
    return template.safe_substitute(**variables)


def format_file_context(topic_dir: Path) -> str:
    chunks: list[str] = []
    for relative, content in collect_topic_files(topic_dir):
        chunks.append(f"=== FILE: {relative} ===\n{content}")
    return "\n\n".join(chunks)


def format_review_comments(comments: list[Any]) -> str:
    rendered: list[str] = []
    for comment in comments:
        location = ""
        if getattr(comment, "path", None):
            location = f"{comment.path}"
            if getattr(comment, "line", None) is not None:
                location += f":{comment.line}"
        rendered.append(
            f"- {location or 'PR comment'}\n  {comment.body.strip()}"
        )
    return "\n".join(rendered)


class ResponsesModelClient:
    def __init__(
        self,
        *,
        api_key: str,
        model: str = "gpt-5.5",
        base_url: str = "https://api.openai.com/v1/responses",
        reasoning_effort: str = "medium",
        max_output_tokens: int = 12000,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.reasoning_effort = reasoning_effort
        self.max_output_tokens = max_output_tokens

    @classmethod
    def from_environment(cls, repo_root: Path) -> "ResponsesModelClient":
        load_env_defaults(repo_root / ".env")
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required for automation model calls")
        return cls(
            api_key=api_key,
            model=os.environ.get("OPENAI_AUTOMATION_MODEL", "gpt-5.5"),
            base_url=os.environ.get("OPENAI_AUTOMATION_BASE_URL", "https://api.openai.com/v1/responses"),
            reasoning_effort=os.environ.get("OPENAI_AUTOMATION_REASONING_EFFORT", "medium"),
            max_output_tokens=int(os.environ.get("OPENAI_AUTOMATION_MAX_OUTPUT_TOKENS", "12000")),
        )

    def generate_initial_bundle(
        self,
        *,
        repo_root: Path,
        spec: AlgorithmSpec,
    ) -> ModelCallResult:
        prompt = render_prompt(
            repo_root / "automation/prompts/generation.md",
            {
                "algorithm_name": spec.algorithm_name,
                "display_name": spec.display_name,
                "topic_path": spec.topic_path,
                "prompt_notes": spec.prompt_notes or "None.",
                "topic_files": format_file_context(repo_root / spec.topic_path),
                "repo_instructions": (repo_root / "AGENTS.md").read_text(encoding="utf-8"),
            },
        )
        return self._request_bundle(prompt)

    def generate_review_fix_bundle(
        self,
        *,
        repo_root: Path,
        spec: AlgorithmSpec,
        review_comments: list[Any],
    ) -> ModelCallResult:
        prompt = render_prompt(
            repo_root / "automation/prompts/review_fix.md",
            {
                "algorithm_name": spec.algorithm_name,
                "display_name": spec.display_name,
                "topic_path": spec.topic_path,
                "review_comments": format_review_comments(review_comments),
                "topic_files": format_file_context(repo_root / spec.topic_path),
                "repo_instructions": (repo_root / "AGENTS.md").read_text(encoding="utf-8"),
            },
        )
        return self._request_bundle(prompt)

    def generate_verification_fix_bundle(
        self,
        *,
        repo_root: Path,
        spec: AlgorithmSpec,
        verification_output: str,
    ) -> ModelCallResult:
        prompt = render_prompt(
            repo_root / "automation/prompts/verification_fix.md",
            {
                "algorithm_name": spec.algorithm_name,
                "display_name": spec.display_name,
                "topic_path": spec.topic_path,
                "verification_output": verification_output,
                "topic_files": format_file_context(repo_root / spec.topic_path),
                "repo_instructions": (repo_root / "AGENTS.md").read_text(encoding="utf-8"),
            },
        )
        return self._request_bundle(prompt)

    def _request_bundle(self, prompt: str) -> ModelCallResult:
        body = {
            "model": self.model,
            "reasoning": {"effort": self.reasoning_effort},
            "max_output_tokens": self.max_output_tokens,
            "input": [
                {
                    "role": "developer",
                    "content": "You are generating repository files. Always use the provided function tool to return file writes.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "tools": [
                {
                    "type": "function",
                    "name": "emit_file_bundle",
                    "description": "Return the file writes required for the current automation step.",
                    "strict": True,
                    "parameters": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "summary": {"type": "string"},
                            "files": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "additionalProperties": False,
                                    "properties": {
                                        "path": {"type": "string"},
                                        "content": {"type": "string"},
                                    },
                                    "required": ["path", "content"],
                                },
                            },
                        },
                        "required": ["summary", "files"],
                    },
                }
            ],
            "tool_choice": "required",
        }
        response = self._post_json(body)
        return ModelCallResult(
            prompt=prompt,
            raw_response=response,
            bundle=parse_file_bundle_from_response(response),
        )

    def _post_json(self, body: dict[str, Any]) -> dict[str, Any]:
        payload = json.dumps(body).encode("utf-8")
        req = request.Request(
            self.base_url,
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with request.urlopen(req) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:  # pragma: no cover - exercised only with live network
            body_text = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI API request failed: {exc.code} {body_text}") from exc


def parse_file_bundle_from_response(payload: dict[str, Any]) -> FileBundle:
    outputs = payload.get("output", [])
    for item in outputs:
        if item.get("type") == "function_call" and item.get("name") == "emit_file_bundle":
            arguments = json.loads(item["arguments"])
            files = [
                FileWrite(path=entry["path"], content=entry["content"])
                for entry in arguments["files"]
            ]
            return FileBundle(summary=arguments["summary"], files=files)

    refusal_texts: list[str] = []
    for item in outputs:
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "refusal":
                refusal_texts.append(content.get("refusal", ""))
    if refusal_texts:
        raise RuntimeError("model refused request: " + " | ".join(refusal_texts))

    raise RuntimeError("model response did not contain the expected file bundle tool call")
