from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from automation.model import collect_topic_files, parse_file_bundle_from_response


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


if __name__ == "__main__":
    unittest.main()
