from __future__ import annotations

import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from automation.model import (
    ReviewDecision,
    ResponsesModelClient,
    collect_topic_files,
    load_env_defaults,
    parse_file_bundle_from_response,
    parse_review_decision_from_response,
)


class ModelParsingTests(unittest.TestCase):
    def test_parse_function_call_bundle(self) -> None:
        payload = {
            "output": [
                {
                    "type": "function_call",
                    "name": "emit_file_bundle",
                    "arguments": "{\"summary\":\"generated\",\"files\":[{\"path\":\"topic/PROBLEM.md\",\"content\":\"hello\"}]}",
                }
            ]
        }
        bundle = parse_file_bundle_from_response(payload)
        self.assertEqual(bundle.summary, "generated")
        self.assertEqual(bundle.files[0].path, "topic/PROBLEM.md")
        self.assertEqual(bundle.files[0].content, "hello")

    def test_collect_topic_files_skips_binary_build_artifacts(self) -> None:
        with TemporaryDirectory() as tmp:
            topic_dir = Path(tmp)
            (topic_dir / "PROBLEM.md").write_text("docs", encoding="utf-8")
            build_dir = topic_dir / "cpp" / "build"
            build_dir.mkdir(parents=True)
            (build_dir / "program").write_bytes(b"\xcf\x00\x01binary")
            files = collect_topic_files(topic_dir)
        self.assertEqual(files, [("PROBLEM.md", "docs")])

    def test_request_bundle_retries_on_malformed_tool_arguments(self) -> None:
        client = ResponsesModelClient(
            api_key="test-key",
            malformed_response_retries=1,
        )
        malformed = {
            "output": [
                {
                    "type": "function_call",
                    "name": "emit_file_bundle",
                    "arguments": "{\"summary\":\"generated\",\"files\":[{\"path\":\"topic/PROBLEM.md\",\"content\":\"hello\"}]",
                }
            ]
        }
        valid = {
            "output": [
                {
                    "type": "function_call",
                    "name": "emit_file_bundle",
                    "arguments": "{\"summary\":\"generated\",\"files\":[{\"path\":\"topic/PROBLEM.md\",\"content\":\"hello\"}]}",
                }
            ]
        }
        with patch.object(client, "_post_json", side_effect=[malformed, valid]) as post_mock:
            result = client._request_bundle("prompt")
        self.assertEqual(post_mock.call_count, 2)
        self.assertEqual(result.bundle.summary, "generated")
        self.assertEqual(result.bundle.files[0].path, "topic/PROBLEM.md")

    def test_request_bundle_raises_after_retry_budget_exhausted(self) -> None:
        client = ResponsesModelClient(
            api_key="test-key",
            malformed_response_retries=1,
        )
        malformed = {
            "output": [
                {
                    "type": "function_call",
                    "name": "emit_file_bundle",
                    "arguments": "{\"summary\":\"generated\",\"files\":[{\"path\":\"topic/PROBLEM.md\",\"content\":\"hello\"}]",
                }
            ]
        }
        with patch.object(client, "_post_json", side_effect=[malformed, malformed]) as post_mock:
            with self.assertRaises(RuntimeError) as ctx:
                client._request_bundle("prompt")
        self.assertEqual(post_mock.call_count, 2)
        self.assertIn("malformed file-bundle JSON arguments", str(ctx.exception))

    def test_parse_review_decision_from_response(self) -> None:
        payload = {
            "output": [
                {
                    "type": "function_call",
                    "name": "emit_review_decision",
                    "arguments": "{\"decision\":\"actionable\",\"reason\":\"mixed feedback comment includes a fix request\"}",
                }
            ]
        }
        decision = parse_review_decision_from_response(payload)
        self.assertEqual(
            decision,
            ReviewDecision(
                decision="actionable",
                reason="mixed feedback comment includes a fix request",
            ),
        )

    def test_load_env_defaults_sets_request_timeout_variable(self) -> None:
        with TemporaryDirectory() as tmp:
            env_path = Path(tmp) / ".env"
            env_path.write_text(
                "OPENAI_API_KEY=test-key\nOPENAI_AUTOMATION_REQUEST_TIMEOUT_SECONDS=45\n",
                encoding="utf-8",
            )
            previous_key = os.environ.pop("OPENAI_API_KEY", None)
            previous_timeout = os.environ.pop("OPENAI_AUTOMATION_REQUEST_TIMEOUT_SECONDS", None)
            try:
                load_env_defaults(env_path)
                client = ResponsesModelClient.from_environment(Path(tmp))
            finally:
                if previous_key is None:
                    os.environ.pop("OPENAI_API_KEY", None)
                else:
                    os.environ["OPENAI_API_KEY"] = previous_key
                if previous_timeout is None:
                    os.environ.pop("OPENAI_AUTOMATION_REQUEST_TIMEOUT_SECONDS", None)
                else:
                    os.environ["OPENAI_AUTOMATION_REQUEST_TIMEOUT_SECONDS"] = previous_timeout
        self.assertEqual(client.request_timeout_seconds, 45)


if __name__ == "__main__":
    unittest.main()
