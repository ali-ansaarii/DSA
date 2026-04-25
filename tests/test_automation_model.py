from __future__ import annotations

import unittest

from automation.model import parse_file_bundle_from_response


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


if __name__ == "__main__":
    unittest.main()
